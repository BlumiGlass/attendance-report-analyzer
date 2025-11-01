import pdfplumber
from report_type1 import handle_report_type1, is_report_type1
from report_type2 import handle_report_type2, is_report_type2

def identify_report_type(tables):
    # מזהה את סוג הדוח על פי שמות העמודות בטבלה הראשונה
    headers = tables[0][0]
    if is_report_type1(headers):
        return 'type1'
    elif is_report_type2(headers):
        return 'type2'
    else:
        return None

def extract_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    return tables

def main():
    input_path = "input.pdf"
    output_path = "output.pdf"
    tables = extract_tables(input_path)
    report_type = identify_report_type(tables)
    if report_type == 'type1':
        handle_report_type1(tables, output_path)
    elif report_type == 'type2':
        handle_report_type2(tables, output_path)
    else:
        print("לא זוהה פורמט דוח מתאים.")

if __name__ == "__main__":
    main()