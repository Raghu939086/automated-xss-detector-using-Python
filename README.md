# XSS Scanner (Python Security Assignment)

This project is a **Python-based automated XSS Scanner** developed as part of the VipraTech assignment.  
The tool scans a given URL, injects multiple XSS payloads into each parameter, sends HTTP requests,  
and analyzes the server’s response to detect potential **Reflected XSS vulnerabilities**.

---

## Features

✔ Takes a URL with query parameters  
✔ Injects multiple XSS payloads  
✔ Uses `requests` to send HTTP requests  
✔ Parses HTML responses using BeautifulSoup  
✔ Compares original vs modified responses  
✔ Detects reflected XSS payloads  
✔ Logs all scan activity  
✔ Generates a detailed CSV report  
✔ Includes unit tests  
✔ Clean and modular code structure  
✔ Works fully from command line


##  How the Scanner Works (Simple Explanation)

1. **You provide a target URL**  
   Example:https://example.com/search?name=test&id=10

2. The scanner extracts all parameters: name, id

3. For each parameter, it injects payloads like:
   "><script>alert(1)</script>
   "><img src=x onerror=alert(1)>
   <svg/onload=confirm(1)>
  

4. It sends the request to the website.

5. It compares:
- Original page response  
- Injected payload response  

6. If the payload appears in the HTML response → **XSS vulnerability detected**

7. Generates:
- **Console output**
- **CSV report** (`report.csv`)
- **Log file** (`scan.log`)

git clone https://github.com/
<your-username>/xss_scanner.git
cd xss_scanner

### 2. Create Virtual Environment (optional but recommended)
python -m venv venv
Activate:venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

##  How to Run the Scanner

Run from project root:python -m src.main --url "https://httpbin.org/get?name=test&age=20" --payloads payloads.txt --output report.csv

### Example Command:
python -m src.main --url "https://testphp.vulnweb.com/search.php?test=1" --payloads payloads.txt --output results.csv


## Example Output (Console)

[VULNERABLE] param=name payload='"><script>alert(1)</script>' sim=0.842
Notes: payload reflected in raw HTML (maybe attribute)

[NOT VULNERABLE] param=age payload='<svg/onload=confirm(1)>' sim=0.991

##  report.csv Example

param,payload,vulnerable,similarity,notes
name,"><script>alert(1)</script>",True,0.82,payload reflected in raw HTML
age,"><img src=x onerror=alert(1)>",False,0.99,

##  Logging (scan.log)
2025-11-27 16:19:42 - INFO - Scanner initialized...
2025-11-27 16:19:45 - INFO - Testing payload on param name
2025-11-27 16:20:02 - ERROR - Request timed out
2025-11-27 16:20:25 - INFO - Scan complete.

## Running Tests

Run unit tests: python -m unittest discover -s tests

## 🛠 Tools & Libraries Used

- **Python 3**
- `requests` — for HTTP requests  
- `BeautifulSoup4` — for HTML parsing  
- `difflib` — for response comparison  
- `argparse` — for CLI handling  
- `unittest` — for test cases  


# Thank You!