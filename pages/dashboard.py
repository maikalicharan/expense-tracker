import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import load_expenses
from utils.calculations import calculate_summary


st.title("Dashboard")
st.caption("Your financial overview")


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


total_income = summary["total_income"]
total_expenses = summary["total_expenses"]
balance = summary["balance"]
savings_percentage = summary["savings_percentage"]


# ---------------------------------------------------------
# Dashboard styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .finance-card {
        padding: 1.15rem 1.25rem;
        border-radius: 14px;
        min-height: 115px;
        border: 1px solid rgba(0, 0, 0, 0.06);
        box-shadow: 0 3px 12px rgba(20, 25, 40, 0.06);
    }

    .finance-card-title {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.45rem;
    }

    .finance-card-value {
        font-size: 1.6rem;
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
    df.sort_values(
        "Date",
        ascending=False,
    )
    .head(5)
    .copy()
)


if recent_transactions.empty:

    st.info(
        "No transactions available."
    )

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


# ---------------------------------------------------------
# Financial insight
# ---------------------------------------------------------

st.divider()

st.subheader("Financial Insight")


if total_income <= 0:

    insight_title = "Income Required"

    insight_text = (
        "Add your income transactions to start "
        "tracking your savings and financial health."
    )

    insight_class = "expense-card"


elif balance < 0:

    insight_title = "Spending Is Higher Than Income"

    insight_text = (
        "Your current expenses are higher than your income. "
        "Review your recent spending and consider using "
        "the Planning section to create a budget."
    )

    insight_class = "expense-card"


elif savings_percentage >= 30:

    insight_title = "Strong Savings Rate"

    insight_text = (
        "You are currently saving 30% or more of your income. "
        "That is a strong position to build long-term financial goals."
    )

    insight_class = "income-card"


elif savings_percentage >= 20:

    insight_title = "Good Savings Progress"

    insight_text = (
        "Your current savings rate is above 20%. "
        "Continue tracking your expenses and gradually "
        "increase your savings where possible."
    )

    insight_class = "balance-card"


elif savings_percentage >= 0:

    insight_title = "Room to Improve"

    insight_text = (
        "You are saving some money, but there may be room "
        "to improve your savings rate. Use Planning to "
        "set a structured budget."
    )

    insight_class = "balance-card"


else:

    insight_title = "Review Your Spending"

    insight_text = (
        "Your expenses are currently higher than your income. "
        "Review Account History and identify areas where "
        "spending can be reduced."
    )

    insight_class = "expense-card"


st.markdown(
    f"""
    <div class="insight-card {insight_class}">
        <div class="insight-title">
            {insight_title}
        </div>
        <div class="insight-text">
            {insight_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
