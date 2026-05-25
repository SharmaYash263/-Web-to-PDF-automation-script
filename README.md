This project was developed to address the poor user interface and excessive advertisements found on digital content sites like readcomiconline.li

**Technical Components**
Browser Automation: Utilizes Playwright and Playwright-Stealth to handle JavaScript-heavy sites and navigate security challenges like Cloudflare.

Data Extraction: Employs Regex to identify titles, years, and issue numbers to ensure files are named and sorted correctly for library management (e.g., Title (Year) - Issue 01.pdf).

Quality Assurance: Includes logic to detect blank image placeholders and retry captures, ensuring the final PDF has no missing pages.

System Efficiency: Automatically deletes temporary image files once the PDF is successfully generated to save local storage space.

**Setup and Requirements**
playwright
playwright-stealth
img2pdf
natsort

**Installation:**
 pip install -r requirements.txt

 python -m playwright install chromium
**To Run**

Python Comic.py in Command Prompt or Git Bash

Paste Link

Select download type [ Full, Single, Ranged ] 
Enter and allow run

 LEGAL DISCLAIMER
1. Educational and Research Purpose Only.
This software framework is provided strictly for educational and research purposes concerning browser automation, system integrity, and data analysis. It is intended as a technical demonstration of the author’s proficiency in Python and Playwright, developed during his graduate studies at Texas State University.

2. No Warranty (Provided "AS IS").
The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author, Yash Sharma, be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

3. User Responsibility and Compliance.
The user of this software assumes all responsibility for compliance with local, state, federal, and international laws, including but not limited to copyright and intellectual property statutes. The author does not condone, support, or encourage the use of this software for the unauthorized distribution or acquisition of copyrighted material

4. Indemnification.
By using this software, you agree to indemnify and hold harmless the author from any and all claims, losses, liabilities, and expenses (including legal fees) arising from your use of the software or your violation of these terms.
