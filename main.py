import base64
import requests
from pdf2image import convert_from_path
from report_type1 import handle_type1
from report_type2 import handle_type2
import re
import sys
import os

if len(sys.argv) < 2:
    print("השתמש: py main.py קובץ_קלט.pdf")
    sys.exit(1)

PDF_PATH = sys.argv[1]
POPPLER_PATH = r"C:\\poppler\\Library\\bin"
IMG_PATH = "page1.png"

def read_api_key(config_path="config.cfg"):
    with open(config_path, encoding="utf8") as f:
        lines = f.readlines()
    for line in lines:
        if line.strip().startswith("API_KEY="):
            return line.strip().split("=", 1)[1]
    raise ValueError("API_KEY not found in config file")

API_KEY = read_api_key()

# שם קובץ פלט דומה לקלט
def make_output_name(input_pdf, suffix="_output.pdf"):
    iname, ext = os.path.splitext(os.path.basename(input_pdf))
    return iname + suffix

# 1. המרת PDF לתמונה (עמוד ראשון)
pages = convert_from_path(PDF_PATH, dpi=300, poppler_path=POPPLER_PATH)
pages[0].save(IMG_PATH, "PNG")

# 2. שלח את התמונה ל-Google Vision API
with open(IMG_PATH, "rb") as img:
    content = base64.b64encode(img.read()).decode("utf-8")
endpoint = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
body = {
    "requests": [{
        "image": { "content": content },
        "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
    }]
}
res = requests.post(endpoint, json=body)
result_json = res.json()

if "error" in result_json.get("responses", [{}])[0]:
    print("שגיאת OCR ב-Google:", result_json["responses"][0]["error"])
    exit(1)

text = result_json["responses"][0]["fullTextAnnotation"]["text"]
print("פלט גולמי מה-OCR:\n", text)

# --- פונקציות TYPE1 ---

def extract_table_from_google_ocr(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    col_headers_keywords = ["תאריך", "כניסה", "יציאה", "מקום", "100%", "סה\"כ"]
    table = []
    start_idx = None
    for i, line in enumerate(lines):
        if any(header in line for header in col_headers_keywords):
            start_idx = i
            break
    if start_idx is None:
        print("❌ לא נמצאה שורת כותרת בטבלה.")
        return []
    lines = lines[start_idx:]
    for line in lines:
        cells = [cell.strip() for cell in re.split(r"[|\t]| {2,}", line)]
        if (len(cells) > 3 
            and not re.fullmatch(r'^[0-9]+$', cells[0]) 
            and "סה\"כ" not in cells[0] 
            and "ימים" not in cells[0]):
            table.append(cells)
    return table

def split_joined_headers(headers_row):
    res = []
    for item in headers_row:
        if item == "מקום עם כניסה":
            res += ["מקום עבודה", "כניסה"]
        elif item == "יציאה הפסקה":
            res += ["יציאה", "הפסקה"]
        elif item == "100% 125% 150%":
            res += ["100%", "125%", "150%"]
        else:
            res.append(item)
    return res

def fix_headers(raw_headers):
    expected_headers = [
        "תאריך", "יום", "מקום עבודה", "כניסה", "יציאה", "הפסקה",
        "סה\"כ", "100%", "125%", "150%", "שבת"
    ]
    join_line = " ".join(raw_headers)
    splits = []
    for h in expected_headers:
        if h in join_line:
            splits.append(h)
            join_line = join_line.replace(h, "|", 1)
    if splits and "|" in join_line:
        fixed = [h.strip() for h in join_line.split('|') if h.strip()]
        if len(fixed) >= 4:
            return fixed
    return raw_headers

def detect_report_type(headers):
    headers_str = " ".join(headers).replace(" ", "")
    if "מקוםעבודה" in headers_str and "כניסה" in headers_str and "100%" in headers_str:
        return "type1"
    if "יום" in headers_str and "הערות" in headers_str:
        return "type2"
    return None

# --- TYPE2: חילוץ טבלה חכם ממבנה free text ---

def extract_table_type2(text):
    date_regex = r'\d{1,2}/\d{1,2}/\d{2,4}'
    day_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    table = []
    headers = ["תאריך", "יום", "כניסה", "יציאה", "שעות", "הערות"]
    current_row = []
    for idx, line in enumerate(lines):
        if re.match(date_regex, line):  # מתחילה שורה חדשה של טבלה
            if len(current_row) >= 3:
                table.append(current_row)
            current_row = [line]
        elif any(day in line for day in day_names):
            current_row.append(line)
        elif re.match(r'\d{1,2}:\d{2}', line):
            current_row.append(line)
        elif re.match(r'^\d+\.\d{1,2}$', line):
            current_row.append(line)
        elif len(current_row) > 0 and len(line) < 12:
            current_row.append(line)
    if len(current_row) >= 3:
        table.append(current_row)
    if len(table) > 1:
        final_table = [headers[:max(len(r) for r in table)]]
        for row in table:
            final_table.append(row[:len(final_table[0])])
        return final_table
    return []

# --- שילוב חכם ---

output_name = make_output_name(PDF_PATH, '_output.pdf')

table = extract_table_from_google_ocr(text)
report_type = None
if table and len(table[0]) >= 3:
    print("כותרות גולמיות:", [x for x in table[0]])
    table[0] = split_joined_headers(table[0])
    print("כותרות לאחר פיצול:", [x for x in table[0]])
    report_type = detect_report_type(table[0])

if report_type == "type1":
    handle_type1([table], output_name)
    print(f"יצירת וריאציה לדוח 1 הסתיימה! נשמר: {output_name}")
elif report_type == "type2":
    handle_type2([table], output_name)
    print(f"יצירת וריאציה לדוח 2 הסתיימה! נשמר: {output_name}")
else:
    table2 = extract_table_type2(text)
    if table2 and len(table2) > 1:
        print("טבלה אוטומטית type2:")
        for row in table2:
            print(row)
        handle_type2([table2], output_name)
        print(f"יצירת וריאציה לדוח 2 הסתיימה! נשמר: {output_name}")
    else:
        print("❌ לא זוהתה טבלה מספקת מה-OCR, בדוק איכות/מבנה הקובץ.")
