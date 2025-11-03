import random
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# רישום גופן Arial בעברית
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

hebrew_style = ParagraphStyle(
    'hebrew_style',
    fontName='Arial',
    fontSize=11,
    alignment=2,
    rightIndent=0,
)

def fix_hebrew(s):
    # אופציונלי: הופך רק אם מדובר במחרוזת עברית
    if s and any('\u0590' <= c <= '\u05EA' for c in s):
        return s[::-1]
    return s

def rtl_row(row):
    return [Paragraph(fix_hebrew(cell), hebrew_style) for cell in row[::-1]]

def generate_variation(rows):
    new_rows = []
    for row in rows[1:]:
        if not row or len(row) < 11:
            continue
        date, day, place, *_ = row[:11]
        if day.strip() == "שבת":
            enter, exit = "09:00", "17:00"
            total = 8.0
        else:
            start = random.randint(7, 9)
            end = start + random.randint(7, 9)
            enter = f"{start:02d}:00"
            exit = f"{end:02d}:00"
            total = (end - start) - 0.5
        total = max(total, 0)
        h100 = min(total, 8.0)
        h125 = max(0, min(total-8, 2))
        h150 = max(0, total-10)
        shabbat = total if day.strip() == "שבת" else 0.0
        new_row = [
            date, day, place, enter, exit, "00:30",
            f"{total:.2f}", f"{h100:.2f}", f"{h125:.2f}", f"{h150:.2f}", f"{shabbat:.2f}"
        ]
        new_rows.append(new_row)
    return new_rows

def sum_columns(rows):
    sums = [0.0] * 5
    for row in rows:
        for idx, col in enumerate(row[6:11]):
            try:
                sums[idx] += float(col)
            except:
                pass
    return sums

def handle_type1(tables, output_pdf):
    headers = tables[0][0]
    rows = tables[0][1:]

    var_rows = generate_variation([headers] + rows)
    sums = sum_columns(var_rows)
    sum_row = ["סה\"כ", "", ""] + [""]*3 + [f"{s:.2f}" for s in sums]

    summary_titles = [
        "ימים", "סה\"כ שעות", "שעות 100%", "שעות 125%", "שעות 150%",
        "שבת 150%", "בונוס", "נסיעות"
    ]
    summary_values = [
        str(len(var_rows)),
        f"{sums[0]:.2f}", f"{sums[1]:.2f}", f"{sums[2]:.2f}", f"{sums[3]:.2f}", f"{sums[4]:.2f}",
        str(random.randint(0, 200)), str(random.randint(0, 300))
    ]
    summary_table = [
        [Paragraph(fix_hebrew(t), hebrew_style), Paragraph(str(v), hebrew_style)]
        for t, v in zip(summary_titles, summary_values)
    ]

    doc = SimpleDocTemplate(output_pdf, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=30)

    # בניית הטבלה החדשה בסדר עמודות הפוך!
    table_data = [rtl_row(headers)]
    table_data += [rtl_row(row) for row in var_rows]
    table_data.append(rtl_row(sum_row))

    elements = [
        Paragraph(fix_hebrew("שם חברה: דוגמה"), hebrew_style),
        Paragraph(fix_hebrew("שם עובד: דוגמה"), hebrew_style),
        Spacer(1, 12),
        Table(table_data, style=[
                ("GRID", (0,0), (-1,-1), 0.5, colors.black),
                ("BACKGROUND", (0,0), (-1,0), colors.lightgrey)
            ]),
        Spacer(1, 24),
        Table(summary_table, style=[
            ("GRID", (0,0), (-1,-1), 0.5, colors.black)
        ])
    ]
    doc.build(elements)