import os
import time
import img2pdf
import re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from natsort import natsorted

# Directory for persistent browser session data
USER_DATA_DIR = os.path.join(os.getcwd(), "user_data")

def get_issue_number(name):
    """Simple extraction of numbers for the range filter."""
    match = re.search(r'(\d+)', name)
    return int(match.group(1)) if match else 0

def check_for_captcha(page):
    """Checks for security challenges like Cloudflare."""
    selectors = ["text='Verify you are human'", "#challenge-form", "iframe[src*='cloudflare']"]
    for s in selectors:
        if page.query_selector(s):
            return True
    return False

def run():
    print("Ensure you have your series link ready to go!")
    series_url = input("Paste the series link: ").strip()
    
    # Extract base domain so links work regardless of the mirror used
    parsed_url = urlparse(series_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    print(f"\nTargeting: {base_url}")
    print("Which type would you like to download?  [1] Single Issue  [2] Range  [3] All Issues")
    mode = input("Select mode (1/2/3): ").strip()
    
    selection = ""
    if mode == "1":
        selection = input("Enter specific issue number: ").strip()
    elif mode == "2":
        selection = input("Enter range (e.g. 1-10): ").strip()

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            no_viewport=True
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(context)

        print(f"\nFetching series list...")
        page.goto(series_url, wait_until="domcontentloaded")
        
        if check_for_captcha(page):
            print("Please solve the CAPTCHA in the browser, then press ENTER...")
            input()

        issue_elements = page.query_selector_all("table.listing a")
        all_issues = [{"name": e.inner_text().strip(), "url": e.get_attribute("href")} for e in issue_elements][::-1]

        # Filter Logic
        targets = []
        if mode == "1":
            targets = [i for i in all_issues if get_issue_number(i['name']) == int(selection)]
        elif mode == "2":
            start, end = selection.lower().split('-')
            start_num = int(start)
            targets = [i for i in all_issues if get_issue_number(i['name']) >= start_num]
            if end != "all":
                targets = [i for i in targets if get_issue_number(i['name']) <= int(end)]
        else:
            targets = all_issues

        print(f"\nReady to process {len(targets)} files.")

        for issue in targets:
            connector = "&" if "?" in issue['url'] else "?"
            full_url = f"{base_url}{issue['url']}{connector}readType=1"
            
            temp_folder = "temp_capture"
            os.makedirs(temp_folder, exist_ok=True)
            
            print(f"\n>>> Processing: {issue['name']}")
            page.goto(full_url)
            
            time.sleep(2) 
            if check_for_captcha(page) or not page.query_selector("#divImage"):
                print("Security check triggered. Resolve it manually, then press ENTER...")
                input()

            # Scroll to load images
            for _ in range(5):
                page.mouse.wheel(0, 3000)
                time.sleep(0.8)

            imgs = page.query_selector_all("#divImage img, .divImage img")
            for i, img in enumerate(imgs):
                img.scroll_into_view_if_needed()
                time.sleep(0.3)
                save_path = f"{temp_folder}/{i:03}.jpg"
                img.screenshot(path=save_path)
                
                # Basic check for failed screenshots
                if os.path.getsize(save_path) < 1000:
                    time.sleep(1.5)
                    img.screenshot(path=save_path)

            # --- SIMPLE NAMING (NO REGEX) ---
            # Just cleans characters that Windows/Mac don't like in filenames
            clean_name = re.sub(r'[\\/*?:"<>|]', "", issue['name'])
            pdf_name = f"{clean_name}.pdf"

            # Compile PDF
            valid_imgs = natsorted([os.path.join(temp_folder, f) for f in os.listdir(temp_folder) if f.endswith(".jpg")])
            
            if valid_imgs:
                with open(pdf_name, "wb") as f:
                    f.write(img2pdf.convert(valid_imgs))
                print(f"SUCCESS: Created {pdf_name}")
                
                # Wipe temporary JPGs
                for f in valid_imgs: os.remove(f)
            else:
                print(f"Error: No valid images found for {issue['name']}")

        print("\n Done, Enjoy reading! ")
        context.close()

if __name__ == "__main__":
    run()