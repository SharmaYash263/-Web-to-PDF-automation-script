import os
import time
import img2pdf
import re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from natsort import natsorted

# Configuration - Your browser session is saved in this folder
USER_DATA_DIR = os.path.join(os.getcwd(), "user_data")

def get_issue_number(name):
    """Extracts digits after '#' or 'Issue' to help with range filtering."""
    match = re.search(r'(?:#|Issue\s*)(\d+)', name)
    return int(match.group(1)) if match else 0

def check_for_captcha(page):
    """Checks if security challenges like Cloudflare are visible."""
    selectors = ["text='Verify you are human'", "#challenge-form", "iframe[src*='cloudflare']"]
    for s in selectors:
        if page.query_selector(s):
            return True
    return False

def run():
    print("=== DYNAMIC WEB-TO-PDF FRAMEWORK ===")
    series_url = input("Paste the comic series link: ").strip()
    
    # --- DYNAMIC URL PARSING ---
    # Automatically extracts 'https://readcomiconline.li' or any other domain
    parsed_url = urlparse(series_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    print(f"\nDetected Base Domain: {base_url}")
    print("Modes: [1] Single Issue  [2] Range (e.g. 1-10)  [3] All Issues")
    mode = input("Select mode (1/2/3): ").strip()
    
    selection = ""
    if mode == "1":
        selection = input("Enter the specific issue number (e.g. 5): ").strip()
    elif mode == "2":
        selection = input("Enter range (e.g. 12-24 or 12-all): ").strip()

    with sync_playwright() as p:
        # Launching with persistent context to save your 'Solved' captcha state
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            no_viewport=True
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(context)

        # 1. Fetch Series List
        print(f"\nLoading series metadata...")
        page.goto(series_url, wait_until="domcontentloaded")
        
        if check_for_captcha(page):
            print("Action Required: Solve the CAPTCHA in the browser, then press ENTER...")
            input()

        issue_elements = page.query_selector_all("table.listing a")
        all_issues = [{"name": e.inner_text().strip(), "url": e.get_attribute("href")} for e in issue_elements][::-1]

        # 2. Filter Issues based on Selection
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

        print(f"\nReady to process {len(targets)} items.")

        # 3. Processing Loop
        for issue in targets:
            connector = "&" if "?" in issue['url'] else "?"
            # Dynamically uses the base_url we extracted at the start
            full_url = f"{base_url}{issue['url']}{connector}readType=1"
            
            temp_folder = "temp_capture"
            os.makedirs(temp_folder, exist_ok=True)
            
            print(f"\n>>> Current Task: {issue['name']}")
            page.goto(full_url)
            
            # Security wait and smart check
            time.sleep(2) 
            if check_for_captcha(page) or not page.query_selector("#divImage"):
                print("Security check triggered. Resolve it, then press ENTER...")
                input()

            # 4. Scroll and Capture Logic
            print("Capturing pages...")
            for _ in range(5):
                page.mouse.wheel(0, 3000)
                time.sleep(0.8)

            imgs = page.query_selector_all("#divImage img, .divImage img")
            for i, img in enumerate(imgs):
                img.scroll_into_view_if_needed()
                time.sleep(0.3)
                save_path = f"{temp_folder}/{i:03}.jpg"
                img.screenshot(path=save_path)
                
                # Placeholder Check: Retry if screenshot is too small (blank)
                if os.path.getsize(save_path) < 5000:
                    time.sleep(1.5)
                    img.screenshot(path=save_path)

            # 5. Dynamic Renaming: Title (Year) - Issue XX.pdf
            match = re.search(r"(.*)\s\((\d{4})\)\sIssue\s#?(\d+)", issue['name'])
            if match:
                title, year, num = match.group(1).strip(), match.group(2), match.group(3).zfill(2)
                pdf_name = f"{title} ({year}) - Issue {num}.pdf"
            else:
                pdf_name = f"{issue['name'].replace('/', '-')}.pdf"

            # 6. Compile and Cleanup
            valid_imgs = natsorted([os.path.join(temp_folder, f) for f in os.listdir(temp_folder) if f.endswith(".jpg") and os.path.getsize(os.path.join(temp_folder, f)) > 5000])
            
            if valid_imgs:
                with open(pdf_name, "wb") as f:
                    f.write(img2pdf.convert(valid_imgs))
                print(f"SUCCESS: Created {pdf_name}")
                
                # Wipe temporary JPGs to save storage space
                for f in valid_imgs: os.remove(f)
            else:
                print(f"FAILED: No valid images found for {issue['name']}")

        print("\n--- ALL TASKS COMPLETED SUCCESSFULLY ---")
        context.close()

if __name__ == "__main__":
    run()