import pandas as pd

from utils.sheets import get_google_sheet


def load_expenses():
    worksheet = get_google_sheet()

    records = worksheet.get_all_records()

    df = pd.DataFrame(records)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert ID and Amount to numeric values
    df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
        errors="coerce",
    )

    # Make blank descriptions easier to work with
    df["Description"] = df["Description"].fillna("").astype(str)

    # Determine whether each transaction is income or expense
    df["Type"] = df["Amount"].apply(
        lambda amount: "Income" if amount > 0 else "Expense"
    )

    # Useful time columns for analytics
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    df["Year"] = df["Date"].dt.year

    # Positive value for expense calculations
    df["Expense Amount"] = df["Amount"].abs()

    return df