import random
import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_variation(rows):
    # rows: כולל כותרות
    new_rows = []
    for row in rows[1:]:
        if not row or len(row) < 6:
            continue
        date, weekday, *_ = row[:6]
        start = random.randint(7, 9)
        end = start + random.randint(7, 9)
        enter = f"{start:02d}:00"
        exit = f"{end:02d}:00"
        total = float(end - start)
        note = ""
        if date.startswith("01/"):
            note = "ראש השנה"
        new_row = [date, weekday, enter, exit, f"{total:.2f}", note]
        new_rows.append(new_row)
    return new_rows

def handle_type2(tables, output_pdf):
    # headers, rows
    headers = tables[0][0]
    rows = tables[0][1:]
    var_rows = generate_variation([headers] + rows)
    num_days = len(var_rows)
    total_hours = sum(float(row[4]) for row in var_rows)
    hourly_rate = random.uniform(30, 60)
    total_pay = hourly_rate * total_hours
    month_str = datetime.datetime.now().strftime("%b-%y")

    table1 = [
        ["שם העובד:", "דוגמה"],
        ["", ""],
        ["סה\"כ: ימי עבודה לחודש", str(num_days)],
        ["סה\"כ: שעות חודשיות", f"{total_hours:.2f}"],
        ["מחיר לשעה", f"{hourly_rate:.2f}"],
        ["סה\"כ לתשלום", f"{total_pay:.2f}"]
    ]
    table2 = [["כרטיס עובד לחודש:", month_str]]

    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [
        Table(table1, style=[("GRID", (0,0), (-1,-1), 0.5, colors.black)]),
        Spacer(1, 12),
        Table(table2, style=[("GRID", (0,0), (-1,-1), 0.5, colors.black)]),
        Spacer(1, 12),
        Table([headers] + var_rows,
              style=[
                  ("GRID", (0,0), (-1,-1), 0.5, colors.black),
                  ("BACKGROUND", (0,0), (-1,0), colors.lightgrey)
              ])
    ]
    doc.build(elements)