from sheets import get_google_sheet

try:
    worksheet = get_google_sheet()

    print("SUCCESS: Connected to Google Sheets!")
    print(f"Worksheet: {worksheet.title}")
    print(f"Rows found: {worksheet.row_count}")

except Exception as e:
    print("CONNECTION FAILED")
    print(type(e).__name__)
    print(str(e))