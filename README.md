# attendance-report-analyzer

מערכת חכמה לחילוץ, עיבוד והפקת דוחות נוכחות בעברית מקובצי PDF סרוקים או דוחות ויזואלים.

## התקנה
נדרש Python 3.8+ וספריות:
- pdf2image
- requests
- reportlab
- Pillow
- poppler (להמרת PDF לתמונה, יש להוריד ולהגדיר את הפת' ל-bin במערכת)

התקנת הספריות:
```sh
pip install -r requirements.txt
```
או:

```bash
pip install pdf2image requests Pillow reportlab
```
הגדרת המפתח (Google Vision API)
יש לשמור את מפתח ה-API בקובץ בשם config.cfg במבנה:

Code
API_KEY=your_google_api_key_here
אל תעלו מפתח גישה למאגרים פומביים!

שימוש
הרץ:

```bash
py main.py path/to/input.pdf
```
או

```bash
python main.py input.pdf
```
הפלט יווצר כקובץ PDF נוסף, עם סיומת _output.pdf בשם הקלט, לדוג'

Code
`input.pdf`  →  `input_output.pdf`
קבצים עיקריים:
`main.py` - קובץ השליטה העיקרי.
`report_type1.py` - טיפול בדוחות מסוג טבלה רגילה.
`report_type2.py` - טיפול בדוחות עם טבלאות טקסט חופשיות/מבנה בעייתי.
`config.cfg` - מכיל מפתח גישה ל-Google API.
הגדרות נוספות:
יש לשנות את הנתיב ל-Poppler בקובץ `main.py` עבור סביבת Windows שלך.
תמיכת עברית מלאה דורשת קובץ Arial מהמערכת, שבד"כ קיים בנתיב: C:\Windows\Fonts\arial.ttf.
