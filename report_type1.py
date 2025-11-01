import random
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

def is_report_type1(headers):
    return "מקום עבודה" in headers and "כניסה" in headers and "100%" in headers

def random_time(hour_from=7, hour_to=10):
    hour = random.randint(hour_from, hour_to)
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02d}:{minute:02d}"

def time_diff(start, end):
    h1, m1 = map(int, start.split(":"))
    h2, m2 = map(int, end.split(":"))
    return ((h2*60 + m2) - (h1*60 + m1)) / 60

def calc_row(day_name):
    if day_name == "שבת":
        # דוגמה: כל השעות בשבת
        enter, exit = "09:00", "17:00"
        total = time_diff(enter, exit)
        return [enter, exit, "00:30", "0.00", "0.00", "0.00", f"{total:.2f}"]
    else:
        enter = random_time()
        exit_hour = int(enter[:2]) + random.randint(7, 9)
        exit = f"{exit_hour:02d}:{enter[3:5]}"
        break_time = "00:30"
        total = time_diff(enter, exit) - 0.5
        h100 = min(total, 8.0)
        h125 = max(0, min(total - 8, 2))
        h150 = max(0, total - 10)
        return [enter, exit, break_time, f"{total:.2f}", f"{h100:.2f}", f"{h125:.2f}", f"{h150:.2f}"]

def handle_report_type1(tables, output_path):
    # שליפת כותרות
    headers = tables[0][0]
    data_rows = tables[0][1:-1]  # כל השורות חוץ מסכום
    summary_row = tables[0][-1]

    # יצירת נתונים חדשים
    new_rows = []
    for row in data_rows:
        date, day, place, *_ = row
        if day.startswith("יום "):
            day_name = day[4:]
        else:
            day_name = day
        times = calc_row(day_name)
        new_row = [date, day, place] + times
        # הוספת עמודות שבת (רק אם שבת)
        if day_name == "שבת":
            new_row += ["0.00", "0.00", f"{float(times[-1]):.2f}"]
        else:
            new_row += [times[4], times[5], times[6], "0.00"]
        new_rows.append(new_row)

    # סכימות לעמודות
    sums = [0.0] * 7
    for row in new_rows:
        for i in range(3, 10):
            sums[i-3] += float(row[i])
    # שורת סיכום
    sum_row = [""] * 3 + [f"{s:.2f}" for s in sums]
    sum_row[0] = "סה\"כ"
    # מספר ימים מתחת לעמודת תאריך
    sum_row[1] = str(len(new_rows))

    # טבלת סיכום שנייה (שורות)
    table2_titles = [
        "ימים", "סה\"כ שעות", "שעות 100%", "שעות 125%", "שעות 150%", "שבת 150%", "בונוס", "נסיעות"
    ]
    table2_values = [
        str(len(new_rows)),
        f"{sums[0]:.2f}", f"{sums[1]:.2f}", f"{sums[2]:.2f}", f"{sums[3]:.2f}", f"{sums[4]:.2f}",
        f"{random.randint(0,200)}", f"{random.randint(0,300)}"
    ]
    summary_table = [[t, v] for t, v in zip(table2_titles, table2_values)]

    # יצירת PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("שם חברה: דוגמה", styles['Normal']))
    elements.append(Paragraph("שם עובד: דוגמה", styles['Normal']))
    elements.append(Spacer(1, 12))
    main_table = Table([headers] + new_rows + [sum_row])
    main_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey)
    ]))
    elements.append(main_table)
    elements.append(Spacer(1, 24))
    summary_table_obj = Table(summary_table)
    summary_table_obj.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black)
    ]))
    elements.append(summary_table_obj)
    doc.build(elements)