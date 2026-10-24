import streamlit as st

from utils.data import load_expenses
from utils.calculations import calculate_summary


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
)


st.title("💰 Expense Tracker")
st.caption("Your personal finance dashboard")


# Load data from Google Sheets
try:
    df = load_expenses()
    summary = calculate_summary(df)

except Exception as e:
    st.error("Unable to load expense data.")
    st.exception(e)
    st.stop()


# Summary values
total_income = summary["total_income"]
total_expenses = summary["total_expenses"]
balance = summary["balance"]
savings_percentage = summary["savings_percentage"]


# Dashboard cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💵 Total Income",
        f"₹{total_income:,.2f}",
    )

with col2:
    st.metric(
        "💸 Total Expenses",
        f"₹{total_expenses:,.2f}",
    )

with col3:
    st.metric(
        "💰 Balance",
        f"₹{balance:,.2f}",
    )

with col4:
    st.metric(
        "📊 Savings",
        f"{savings_percentage:,.2f}%",
    )


st.divider()

st.subheader("Recent Transactions")

# Show the latest 10 transactions
recent_transactions = df.sort_values(
    "Date",
    ascending=False,
).head(10)

st.dataframe(
    recent_transactions[
        [
            "Date",
            "Description",
            "Category",
            "Amount",
            "Type",
            "Paid to or received from",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)