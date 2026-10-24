import pandas as pd


def calculate_summary(df):
    total_income = df.loc[df["Type"] == "Income", "Amount"].sum()

    total_expenses = df.loc[
        df["Type"] == "Expense", "Expense Amount"
    ].sum()

    balance = total_income - total_expenses

    if total_income > 0:
        savings_percentage = (balance / total_income) * 100
    else:
        savings_percentage = 0

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "savings_percentage": savings_percentage,
    }