import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import load_expenses
from utils.calculations import calculate_summary


st.title("Dashboard")
st.caption("Your financial overview")


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

try:

    df = load_expenses()
    summary = calculate_summary(df)

except Exception as e:

    st.error("Unable to load dashboard data.")
    st.exception(e)
    st.stop()


if df.empty:

    st.info(
        "No transactions found yet. "
        "Add your first transaction to see your dashboard."
    )

    st.stop()


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

total_income = summary["total_income"]
total_expenses = summary["total_expenses"]
balance = summary["balance"]
savings_percentage = summary["savings_percentage"]


# ---------------------------------------------------------
# Custom dashboard CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .finance-card {
        padding: 1.15rem 1.25rem;
        border-radius: 14px;
        min-height: 125px;
        border: 1px solid rgba(0, 0, 0, 0.06);
        box-shadow: 0 3px 12px rgba(20, 25, 40, 0.06);
    }

    .finance-card-title {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.45rem;
    }

    .finance-card-value {
        font-size: 1.65rem;
        font-weight: 750;
        line-height: 1.2;
    }

    .income-card {
        background: #eaf7ef;
        border-left: 5px solid #2e9d5b;
    }

    .income-card .finance-card-title {
        color: #267a48;
    }

    .income-card .finance-card-value {
        color: #176b3b;
    }

    .expense-card {
        background: #fff0f0;
        border-left: 5px solid #d9534f;
    }

    .expense-card .finance-card-title {
        color: #a94442;
    }

    .expense-card .finance-card-value {
        color: #a52f2f;
    }

    .balance-card {
        background: #edf4ff;
        border-left: 5px solid #3978d3;
    }

    .balance-card .finance-card-title {
        color: #315f9f;
    }

    .balance-card .finance-card-value {
        color: #245ca8;
    }

    .savings-card {
        background: #f3edff;
        border-left: 5px solid #7a52c7;
    }

    .savings-card .finance-card-title {
        color: #6540a8;
    }

    .savings-card .finance-card-value {
        color: #5834a0;
    }

    .insight-card {
        padding: 1rem 1.15rem;
        border-radius: 12px;
        margin-top: 0.5rem;
        border: 1px solid #e4e6ec;
        background: #ffffff;
    }

    .insight-title {
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .insight-text {
        color: #555b68;
        line-height: 1.55;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Financial overview
# ---------------------------------------------------------

st.subheader("Financial Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="finance-card income-card">
            <div class="finance-card-title">
                Total Income
            </div>
            <div class="finance-card-value">
                ₹{total_income:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        f"""
        <div class="finance-card expense-card">
            <div class="finance-card-title">
                Total Expenses
            </div>
            <div class="finance-card-value">
                ₹{total_expenses:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:

    st.markdown(
        f"""
        <div class="finance-card balance-card">
            <div class="finance-card-title">
                Balance
            </div>
            <div class="finance-card-value">
                ₹{balance:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col4:

    st.markdown(
        f"""
        <div class="finance-card savings-card">
            <div class="finance-card-title">
                Savings Rate
            </div>
            <div class="finance-card-value">
                {savings_percentage:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Monthly overview
# ---------------------------------------------------------

st.divider()

st.subheader("Monthly Overview")


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
    "Year",
    available_years,
    label_visibility="collapsed",
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
)


monthly_chart.update_layout(
    xaxis_title="",
    yaxis_title="Amount (₹)",
    legend_title="",
    margin=dict(
        l=10,
        r=10,
        t=20,
        b=10,
    ),
    hovermode="x unified",
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


# ---------------------------------------------------------
# Recent transactions
# ---------------------------------------------------------

st.divider()

st.subheader("Recent Transactions")


recent_transactions = (
    df.sort
