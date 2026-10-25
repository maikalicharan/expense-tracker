import streamlit as st
import plotly.express as px

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
col1, col2 = st.columns(2)

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


col3, col4 = st.columns(2)

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

# Dashboard year filter
available_years = sorted(
    df["Year"].dropna().astype(int).unique().tolist(),
    reverse=True,
)

selected_year = st.selectbox(
    "📅 Year",
    available_years,
)

# Monthly income and expense data

filtered_df = df[df["Year"] == selected_year]
available_months = sorted(
    filtered_df["Month"].dropna().unique().tolist()
)
selected_month = st.selectbox(
    "📅 Month",
    ["All Months"] + available_months,
)

if selected_month != "All Months":
    filtered_df = filtered_df[
        filtered_df["Month"] == selected_month
    ]
    
monthly_data = (
    filtered_df.groupby(["Month", "Type"])["Amount"]
    .sum()
    .reset_index()
)

monthly_data["Amount"] = monthly_data.apply(
    lambda row: (
        abs(row["Amount"])
        if row["Type"] == "Expense"
        else row["Amount"]
    ),
    axis=1,
)

st.subheader("📈 Monthly Income vs Expenses")

# Category-wise expense data
category_expenses = (
    filtered_df[filtered_df["Type"] == "Expense"]
    .groupby("Category")["Expense Amount"]
    .sum()
    .reset_index()
)

monthly_chart = px.line(
    monthly_data,
    x="Month",
    y="Amount",
    color="Type",
    markers=True,
)

monthly_chart.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount (₹)",
    legend_title="",
)

st.plotly_chart(
    monthly_chart,
    use_container_width=True,
)

st.subheader("🍕 Expenses by Category")

category_chart = px.pie(
    category_expenses,
    names="Category",
    values="Expense Amount",
    hole=0.4,
)

category_chart.update_layout(
    legend_title="Category",
)

st.plotly_chart(
    category_chart,
    use_container_width=True,
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
