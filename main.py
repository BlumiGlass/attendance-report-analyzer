import pdfplumber
from report_type1 import handle_report_type1, is_report_type1
from report_type2 import handle_report_type2, is_report_type2

def extract_tables(pdf_path):
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables.extend(page.extract_tables())
    except Exception as e:
        print(f"שגיאה בקריאת הקובץ: {e}")
        return []
    return tables

def identify_report_type(tables):
    if not tables or not tables[0]:
        print("לא נמצאו טבלאות בקובץ ה-PDF. ודא שהקובץ מכיל טבלה שניתן לחלץ ממנה נתונים.")
        return None
    headers = tables[0][0]
    if is_report_type1(headers):
        return 'type1'
    elif is_report_type2(headers):
        return 'type2'
    else:
        print("הקובץ לא תואם לאף אחד מהפורמטים המוכרים.")
        return None

def main():
    input_path = "input.pdf"
    output_path = "output.pdf"
    tables = extract_tables(input_path)

    if not tables or not tables[0]:
        print("שגיאה: לא נמצאו טבלאות לשימוש. נסה קובץ אחר או ודא שה-PDF אינו תמונה בלבד.")
        return

    report_type = identify_report_type(tables)
    if report_type == 'type1':
        print("זוהה דוח מסוג 1. מתחיל יצירת וריאציה...")
        handle_report_type1(tables, output_path)
        print(f"הדו\"ח החדש נשמר בשם {output_path}")
    elif report_type == 'type2':
        print("זוהה דוח מסוג 2. מתחיל יצירת וריאציה...")
        handle_report_type2(tables, output_path)
        print(f"הדו\"ח החדש נשמר בשם {output_path}")
    else:
        print("לא זוהה פורמט דוח מתאים. אין פעולה לביצוע.")

if __name__ == "__main__":
    main()