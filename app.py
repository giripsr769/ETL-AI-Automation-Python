import pandas as pd
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

input_csv_path = "student_enrollment_raw.csv"

# Read all columns as string to prevent scientific notation (e.g. 9.19E+11)
df = pd.read_csv(input_csv_path, dtype=str)
df = df.fillna("")

print(f"Total rows loaded: {len(df)}")

def clean_row_data(row_dict):
    """
    Takes 1 row of data (as Dictionary) and returns cleaned JSON output with STRICT ETL logic.
    """
    prompt = f"""
    You are an ETL data cleaning engine. Clean and normalize this record:
    {row_dict}
    
    STRICT DATA CLEANING RULES:
    1. KEEP EXACT SAME KEYS/COLUMN NAMES as the input dictionary ({list(row_dict.keys())}). DO NOT change key casing or rename keys.
    
    2. Mobile / Phone Number Validation:
       - Standardize phone numbers into plain digits string.
       - If the cleaned mobile number digit length is LESS THAN 10 digits, set the value to "Invalid".
       
    3. Email Validation:
       - Check if email follows a valid format (e.g., contains '@' and a domain like '.com', '.org').
       - If the email is NOT in a valid email format or is missing, set the value to "invalid mail".
       
    4. Fees Paid Validation:
       - If Fee_Paid / fees paid is 'yes' or 'YES', convert the value to boolean true.
       - If Fee_Paid / fees paid is 'no' or 'NO' (or 'No'), convert the value to boolean false.
       
    5. Formatting & Clean up:
       - Fix name casing (Title Case).
       - Standardize dates to standard YYYY-MM-DD format.
       - Normalize Course names (e.g., 'ML' to 'Machine Learning').
    
    Return ONLY a single valid JSON object containing the cleaned attributes with exact input keys.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You output strictly valid JSON with exact input keys based on specified rules."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        cleaned_data = json.loads(response.choices[0].message.content)
        return cleaned_data
    except Exception as e:
        print(f"Error cleaning row: {e}")
        return row_dict

# Process rows
cleaned_rows = []
for index, row in df.iterrows():
    raw_row_dict = row.to_dict()
    cleaned_dict = clean_row_data(raw_row_dict)
    cleaned_rows.append(cleaned_dict)
    print(f"Cleaned row {index + 1}/{len(df)}")

# Convert back to DataFrame
cleaned_df = pd.DataFrame(cleaned_rows)

# Guarantee column order matches original input file
cleaned_df = cleaned_df[df.columns]

# Save cleanly formatted CSV
output_csv_path = "cleaned_data.csv"
cleaned_df.to_csv(output_csv_path, index=False)

print(f"\nETL process finished cleanly! File saved to {output_csv_path}")