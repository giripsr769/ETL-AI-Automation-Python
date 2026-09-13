# Student Enrollment ETL Data Cleaning Pipeline

A Python-based ETL pipeline that uses OpenAI's `gpt-4o-mini` model to validate, clean, and normalize raw student enrollment data from CSV files.

---

## 📌 Features & Data Cleaning Rules

- **Exact Key Preservation**: Retains the exact column names and key order from the input raw CSV.
- **Mobile Number Standardization**:
  - Converts phone numbers into plain digit strings.
  - Flags numbers shorter than 10 digits as `"Invalid"`.
- **Email Validation**:
  - Validates email structures (ensures presence of `@` and proper domain suffixes like `.com`, `.org`).
  - Sets invalid or missing email entries to `"invalid mail"`.
- **Fee Status Conversion**:
  - Normalizes `'yes'` / `'YES'` values to boolean `true`.
  - Normalizes `'no'` / `'NO'` values to boolean `false`.
- **Data Standardization**:
  - Applies Title Case formatting to student names.
  - Standardizes date formats to `YYYY-MM-DD`.
  - Normalizes course abbreviations (e.g., converts `'ML'` to `'Machine Learning'`).

---

## 🛠️ Prerequisites & Installation

Ensure you have **Python 3.8+** installed. Install the required dependencies using `pip`:

```bash
pip install pandas openai python-dotenv
```

---

## 🔑 Environment Setup

1. Create a `.env` file in the root directory of your project.
2. Add your OpenAI API Key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 📁 Data Input Requirements

- Place your raw CSV file named `student_enrollment_raw.csv` in the root directory alongside `app.py`.
- Ensure all numeric IDs or phone numbers are handled cleanly (the script automatically parses fields as strings to prevent scientific notation formatting).

---

## 🚀 How to Run

Execute the main script:

```bash
python app.py
```

---

## 📤 Output

After processing all rows through the ETL pipeline, the script outputs a cleaned CSV file named `cleaned_data.csv` with columns matching the original input schema.
