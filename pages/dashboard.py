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


# =========================================================
# DASHBOARD CARD STYLES
# =========================================================

st.markdown(
    """
    <style>

    .dashboard-card {
        position: relative;
        padding: 1rem 1.1rem;
        min-height: 108px;
        border-radius: 12px;

        border: 1px solid #e1e5ec;

        box-shadow:
            0 2px 8px rgba(20, 25, 40, 0.04);

        overflow: hidden;
    }


    .dashboard-card-label {
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.55rem;
    }


    .dashboard-card-value {
        font-size: 1.45rem;
        font-weight: 750;
        line-height: 1.2;
    }


    .dashboard-card-income {
        background: #eef9f2;
        border-left: 4px solid #35a765;
    }

    .dashboard-card-income
    .dashboard-card-label {
        color: #26794a;
    }

    .dashboard-card-income
    .dashboard-card-value {
        color: #176b3b;
    }


    .dashboard-card-expense {
        background: #fff3f2;
        border-left: 4px solid #df625d;
    }

    .dashboard-card-expense
    .dashboard-card-label {
        color: #a44845;
    }

    .dashboard-card-expense
    .dashboard-card-value {
        color: #a52f2f;
    }


    .dashboard-card-balance {
        background: #eef5ff;
        border-left: 4px solid #4b82d5;
    }

    .dashboard-card-balance
    .dashboard-card-label {
        color: #315f9f;
    }

    .dashboard-card-balance
    .dashboard-card-value {
        color: #245ca8;
    }


    .dashboard-card-savings {
        background: #f5f0ff;
        border-left: 4px solid #8060c9;
    }

    .dashboard-card-savings
    .dashboard-card-label {
        color: #6540a8;
    }

    .dashboard-card-savings
    .dashboard-card-value {
        color: #5834a0;
    }


    .dashboard-section-note {
        color: #737986;
        font-size: 0.82rem;
        margin-top: -0.25rem;
        margin-bottom: 0.75rem;
    }


    .dashboard-insight {
        padding: 1rem 1.15rem;
        border-radius: 11px;
        border: 1px solid #e1e5ec;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(20, 25, 40, 0.03);
    }


    .dashboard-insight-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #252a34;
        margin-bottom: 0.3rem;
    }


    .dashboard-insight-text {
        color: #5d6470;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FINANCIAL OVERVIEW
# =========================================================

st.subheader("Financial Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        f"""
        <div class="dashboard-card dashboard-card-income">

            <div class="dashboard-card-label">
                Total Income
            </div>

            <div class="dashboard-card-value">
                ₹{total_income:,.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:
    st.markdown(
        f"""
        <div class="dashboard-card dashboard-card-expense">

            <div class="dashboard-card-label">
                Total Expenses
            </div>

            <div class="dashboard-card-value">
                ₹{total_expenses:,.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:
    balance_class = (
        "dashboard-card-income"
        if balance >= 0
        else "dashboard-card-expense"
    )

    balance_label = (
        "Current Balance"
        if balance >= 0
        else "Negative Balance"
    )

    st.markdown(
        f"""
        <div class="dashboard-card {balance_class}">

            <div class="dashboard-card-label">
                {balance_label}
            </div>

            <div class="dashboard-card-value">
                ₹{balance:,.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col4:
    savings_class = (
        "dashboard-card-income"
        if savings_percentage >= 20
        else "dashboard-card-savings"
    )

    st.markdown(
        f"""
        <div class="dashboard-card {savings_class}">

            <div class="dashboard-card-label">
                Savings Rate
            </div>

            <div class="dashboard-card-value">
                {savings_percentage:.1f}%
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MONTHLY OVERVIEW
# =========================================================

st.divider()

st.subheader("Monthly Overview")

st.markdown(
    '<div class="dashboard-section-note">'
    'Income and expenses by month'
    '</div>',
    unsafe_allow_html=True,
)


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
    height=390,

    plot_bgcolor="white",
    paper_bgcolor="white",

    xaxis_title="",
    yaxis_title="Amount",

    legend_title="",

    margin=dict(
        l=10,
        r=10,
        t=20,
        b=10,
    ),

    hovermode="x unified",

    font=dict(
        size=12,
    ),

    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=11),
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor="#eef0f4",
        tickprefix="₹",
        tickfont=dict(size=11),
    ),
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


# =========================================================
# RECENT TRANSACTIONS
# =========================================================

st.divider()

st.subheader("Recent Transactions")

st.markdown(
    '<div class="dashboard-section-note">'
    'Your latest five transactions'
    '</div>',
    unsafe_allow_html=True,
)


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
        column_config={
            "Date": "Date",
            "Description": "Description",
            "Category": "Category",
            "Amount": st.column_config.NumberColumn(
                "Amount",
                format="₹%.2f",
            ),
            "Type": "Type",
            "Paid to or received from": (
                "Paid to / Received from"
            ),
        },
    )


# =========================================================
# FINANCIAL INSIGHT
# =========================================================

st.divider()

st.subheader("Financial Insight")


if total_income <= 0:

    insight_title = "Income Required"

    insight_text = (
        "Add your income transactions to start "
        "tracking your savings and financial health."
    )

    insight_class = "dashboard-card-expense"


elif balance < 0:

    insight_title = "Spending Is Higher Than Income"

    insight_text = (
        "Your current expenses are higher than your income. "
        "Review your spending and use Planning to create "
        "a structured budget."
    )

    insight_class = "dashboard-card-expense"


elif savings_percentage >= 30:

    insight_title = "Strong Savings Rate"

    insight_text = (
        "You are currently saving 30% or more of your income. "
        "Continue building your long-term financial goals."
    )

    insight_class = "dashboard-card-income"


elif savings_percentage >= 20:

    insight_title = "Good Savings Progress"

    insight_text = (
        "Your current savings rate is above 20%. "
        "Continue tracking expenses and gradually "
        "increase savings where possible."
    )

    insight_class = "dashboard-card-balance"


elif savings_percentage >= 0:

    insight_title = "Room to Improve"

    insight_text = (
        "You are saving some money, but there may be room "
        "to improve your savings rate. Use Planning to "
        "set a structured budget."
    )

    insight_class = "dashboard-card-savings"


else:

    insight_title = "Review Your Spending"

    insight_text = (
        "Your expenses are currently higher than your income. "
        "Review Account History and identify areas where "
        "spending can be reduced."
    )

    insight_class = "dashboard-card-expense"


st.markdown(
    f"""
    <div class="dashboard-insight">

        <div class="dashboard-insight-title">
            {insight_title}
        </div>

        <div class="dashboard-insight-text">
            {insight_text}
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
