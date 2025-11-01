import random
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

def is_report_type2(headers):
    return "הערות" in headers and "יום בשבוע" in headers

def random_time(hour_from=7, hour_to=10):
    hour = random.randint(hour_from, hour_to)
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02d}:{minute:02d}"

def time_diff(start, end):
    h1, m1 = map(int, start.split(":"))
    h2, m2 = map(int, end.split(":"))
    return ((h2*60 + m2) - (h1*60 + m1)) / 60

def handle_report_type2(tables, output_path):
    # טבלה ראשית: ימי עבודה
    headers = tables[0][0]
    day_rows = tables[0][1:]

    # יצירת שורות חדשות
    new_rows = []
    for row in day_rows:
        date, weekday, *_ = row
        enter = random_time()
        exit_hour = int(enter[:2]) + random.randint(7, 9)
        exit = f"{exit_hour:02d}:{enter[3:5]}"
        total = time_diff(enter, exit)
        note = ""
        # דוגמה: הערה ב-1 לחודש
        if date.startswith("01/"):
            note = "ראש השנה"
        new_rows.append([
            date, weekday, enter, exit, f"{total:.2f}", note
        ])

    # טבלה ראשונה (שורות)
    num_days = len(new_rows)
    total_hours = sum(float(row[4]) for row in new_rows)
    hourly_rate = random.uniform(30, 60)
    total_pay = hourly_rate * total_hours

    table1 = [
        ["שם העובד:", "דוגמה"],
        ["", ""],
        ["סה\"כ: ימי עבודה לחודש", str(num_days)],
        ["סה\"כ: שעות חודשיות", f"{total_hours:.2f}"],
        ["מחיר לשעה", f"{hourly_rate:.2f}"],
        ["סה\"כ לתשלום", f"{total_pay:.2f}"]
    ]
    # טבלה שניה
    month_str = datetime.datetime.now().strftime("%b-%y")
    table2 = [["כרטיס עובד לחודש:", month_str]]

    # יצירת PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    # טבלה ראשונה
    t1 = Table(table1)
    t1.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.black)]))
    elements.append(t1)
    elements.append(Spacer(1, 12))
    # טבלה שניה
    t2 = Table(table2)
    t2.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.black)]))
    elements.append(t2)
    elements.append(Spacer(1, 12))
    # טבלת ימי עבודה
    t3 = Table([headers] + new_rows)
    t3.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey)
    ]))
    elements.append(t3)
    doc.build(elements)