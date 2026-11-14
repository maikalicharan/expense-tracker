import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import load_expenses
from utils.calculations import calculate_summary


st.title("🏠 Dashboard")
st.caption("Your financial overview")


# -----------------------------
# Load Data
# -----------------------------

try:
    df = load_expenses()
    summary = calculate_summary(df)

except Exception as e:
    st.error("Unable to load dashboard data.")
    st.exception(e)
    st.stop()


# -----------------------------
# Empty Data Check
# -----------------------------

if df.empty:

    st.info(
        "No transactions found yet. "
        "Add your first transaction to see your dashboard."
    )

    st.stop()


# -----------------------------
# Financial Summary
# -----------------------------

total_income = summary["total_income"]
total_expenses = summary["total_expenses"]
balance = summary["balance"]
savings_percentage = summary["savings_percentage"]


st.subheader("💰 Financial Overview")


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
        "📈 Savings",
        f"{savings_percentage:.1f}%",
    )


st.divider()


# -----------------------------
# Monthly Overview
# -----------------------------

st.subheader("📊 Monthly Overview")


month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


available_years = sorted(
    df["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist(),
    reverse=True,
)


selected_year = st.selectbox(
    "Select Year",
    available_years,
)


year_df = df[
    df["Year"] == selected_year
].copy()


all_month_values = [
    f"{selected_year}-{month:02d}"
    for month in range(1, 13)
]


monthly_income = (
    year_df[
        year_df["Type"] == "Income"
    ]
    .groupby("Month")["Amount"]
    .sum()
    .reindex(
        all_month_values,
        fill_value=0,
    )
)


monthly_expenses = (
    year_df[
        year_df["Type"] == "Expense"
    ]
    .groupby("Month")["Expense Amount"]
    .sum()
    .reindex(
        all_month_values,
        fill_value=0,
    )
)


monthly_overview = pd.DataFrame(
    {
        "Month": month_names,
        "Income": monthly_income.values,
        "Expenses": monthly_expenses.values,
    }
)


monthly_chart = px.bar(
    monthly_overview,
    x="Month",
    y=["Income", "Expenses"],
    barmode="group",
    text_auto=".2s",
)


monthly_chart.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount (₹)",
    legend_title="",
)


monthly_chart.update_traces(
    hovertemplate=(
        "<b>%{x}</b>"
        "<br>₹%{y:,.2f}"
        "<extra></extra>"
    )
)


st.plotly_chart(
    monthly_chart,
    use_container_width=True,
)


st.divider()


# -----------------------------
# Recent Transactions
# -----------------------------

st.subheader("🧾 Recent Transactions")


recent_transactions = (
    df.sort_values(
        "Date",
        ascending=False,
    )
    .head(5)
    .copy()
)


if recent_transactions.empty:

    st.info("No transactions available.")

else:

    recent_transactions["Date"] = (
        recent_transactions["Date"]
        .dt.strftime("%d/%m/%Y")
    )


    recent_display = recent_transactions[
        [
            "Date",
            "Description",
            "Category",
            "Amount",
            "Type",
            "Paid to or received from",
        ]
    ].copy()


    st.dataframe(
        recent_display,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# -----------------------------
# Quick Financial Insight
# -----------------------------

st.subheader("💡 Financial Insight")


if total_income <= 0:

    st.info(
        "Add your income transactions to start "
        "tracking your savings and financial health."
    )

elif balance < 0:

    st.warning(
        "Your total expenses are currently higher "
        "than your total income."
    )

elif savings_percentage >= 30:

    st.success(
        "Great! You are currently saving 30% or more "
        "of your income. Keep it up! 🎉"
    )

elif savings_percentage >= 20:

    st.success(
        "Good progress! Your current savings rate "
        "is above 20%."
    )

elif savings_percentage >= 0:

    st.info(
        "You are saving some money. "
        "You can use the Planning section to improve "
        "your savings strategy."
    )

else:

    st.warning(
        "Your current expenses are higher than your income. "
        "Consider reviewing your spending in Account History."
    )
