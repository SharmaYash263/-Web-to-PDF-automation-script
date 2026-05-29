# Web-to-PDF Automation Pipeline

I built this framework to solve a specific problem: the poor user interface and overwhelming number of advertisements on digital reading sites. When trying to read digital content, reference art, or comics on legacy hosting platforms, the experience is often completely disrupted by intrusive pop-ups, broken image placeholders, and clunky navigation. This tool bypasses that messy web environment and automatically extracts and compiles the content into clean, high-resolution, offline PDFs.

Beyond improving the reading experience, this project serves as a technical case study in handling unstructured web data. It demonstrates how to orchestrate persistent browser sessions, navigate automated security roadblocks, and ensure data integrity from the first web request to the final compiled document.

### Technical Components
* **Browser Automation:** Utilizes Playwright and Playwright-Stealth to handle JavaScript-heavy sites and smoothly navigate security challenges like Cloudflare without dropping the session.
* **Data Sanitization:** Dynamically adapts to different URL mirrors and strictly sanitizes web text, stripping out illegal operating system characters to ensure stable, error-free file generation.
* **Quality Assurance:** Includes active data-integrity logic to detect blank image placeholders (highly compressed or failed network streams) and retry captures, ensuring the final PDF has zero missing pages.
* **System Efficiency:** Automatically clears and deletes temporary image caches the moment a PDF is successfully compiled to save local storage space and prevent data contamination between runs.

### Setup and Requirements
The following Python libraries are required:
* `playwright`
* `playwright-stealth`
* `img2pdf`
* `natsort`

**Installation:**
pip install -r requirements.txt
python -m playwright install chromium
To Run
Run python Comic.py in Command Prompt

Paste Link

Select download type [ Full, Single, Ranged ]

Enter and allow run

LEGAL DISCLAIMER
Educational and Research Purpose Only. This software framework is provided strictly for educational and research purposes concerning browser automation, system integrity, and data analysis. It is intended as a technical demonstration of the author’s proficiency in Python and Playwright, developed during his graduate studies at Texas State University.

No Warranty (Provided "AS IS"). The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author, Yash Sharma, be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

User Responsibility and Compliance. The user of this software assumes all responsibility for compliance with local, state, federal, and international laws, including but not limited to copyright and intellectual property statutes. The author does not condone, support, or encourage the use of this software for the unauthorized distribution or acquisition of copyrighted material.

Indemnification. By using this software, you agree to indemnify and hold harmless the author from any and all claims, losses, liabilities, and expenses (including legal fees) arising from your use of the software or your violation of these terms.
