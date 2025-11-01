# attendance-report-analyzer

##1. התקן Python 3.7+  
2. התקן את התלויות:

 ```bash

 pip install -r requirements.txt
 ```

3. התקן את Tesseract מהמדריך כאן:  
https://github.com/tesseract-ocr/tesseract

## שימוש

1. שים קובץ PDF בשם `input.pdf` בתיקייה הראשית.
2. הרץ:
```bash

python main.py
```

3. יווצר קובץ `output.pdf` עם וריאציה תקינה.

## הסבר

- הקוד ממיר את ה-PDF לתמונות, מבצע OCR, מזהה את סוג הדוח, בונה טבלה, ומייצר ואריאציה.
- אם ה-OCR לא מצליח, נסה לשפר את איכות הסריקה או להשתמש ב-DPI גבוה יותר.
- תתאים את פונקציות `extract_table` לפי תבנית ה-OCR בפועל.
