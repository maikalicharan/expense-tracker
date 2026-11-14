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


st.markdown(
    """
    <style>

    /* Dashboard metric cards */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e5ec;
        border-radius: 12px;
        padding: 0.9rem 1rem;
        min-height: 105px;
        box-shadow: 0 2px 8px rgba(20, 25, 40, 0.04);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: #606776 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-weight: 750 !important;
        color: #252a34 !important;
    }

    /* Income */

    .income-metric [data-testid="stMetric"] {
        background: #eef9f2;
        border-left: 4px solid #35a765;
    }

    .income-metric [data-testid="stMetricLabel"] {
        color: #26794a !important;
    }

    .income-metric [data-testid="stMetricValue"] {
        color: #176b3b !important;
    }


    /* Expense */

    .expense-metric [data-testid="stMetric"] {
        background: #fff3f2;
        border-left: 4px solid #df625d;
    }

    .expense-metric [data-testid="stMetricLabel"] {
        color: #a44845 !important;
    }

    .expense-metric [data-testid="stMetricValue"] {
        color: #a52f2f !important;
    }


    /* Balance */

    .balance-metric [data-testid="stMetric"] {
        background: #eef5ff;
        border-left: 4px solid #4b82d5;
    }

    .balance-metric [data-testid="stMetricLabel"] {
        color: #315f9f !important;
    }

    .balance-metric [data-testid="stMetricValue"] {
        color: #245ca8 !important;
    }


    /* Savings */

    .savings-metric [data-testid="stMetric"] {
        background: #f5f0ff;
        border-left: 4px solid #8060c9;
    }

    .savings-metric [data-testid="stMetricLabel"] {
        color: #6540a8 !important;
    }

    .savings-metric [data-testid="stMetricValue"] {
        color: #5834a0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        '<div class="income-metric">',
        unsafe_allow_html=True,
    )

    st.metric(
        "Total Income",
        f"₹{total_income:,.2f}",
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        '<div class="expense-metric">',
        unsafe_allow_html=True,
    )

    st.metric(
        "Total Expenses",
        f"₹{total_expenses:,.2f}",
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


with col3:

    if balance >= 0:
        balance_class = "balance-metric"
        balance_label = "Current Balance"
    else:
        balance_class = "expense-metric"
        balance_label = "Negative Balance"

    st.markdown(
        f'<div class="{balance_class}">',
        unsafe_allow_html=True,
    )

    st.metric(
        balance_label,
        f"₹{balance:,.2f}",
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


with col4:

    if savings_percentage >= 20:
        savings_class = "income-metric"
    else:
        savings_class = "savings-metric"

    st.markdown(
        f'<div class="{savings_class}">',
        unsafe_allow_html=True,
    )

    st.metric(
        "Savings Rate",
        f"{savings_percentage:.1f}%",
    )

    st.markdown(
        "</div>",
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

    insight_type = "warning"


elif balance < 0:

    insight_title = "Spending Is Higher Than Income"

    insight_text = (
        "Your current expenses are higher than your income. "
        "Review your spending and use Planning to create "
        "a structured budget."
    )

    insight_type = "error"


elif savings_percentage >= 30:

    insight_title = "Strong Savings Rate"

    insight_text = (
        "You are currently saving 30% or more of your income. "
        "Continue building your long-term financial goals."
    )

    insight_type = "success"


elif savings_percentage >= 20:

    insight_title = "Good Savings Progress"

    insight_text = (
        "Your current savings rate is above 20%. "
        "Continue tracking expenses and gradually "
        "increase savings where possible."
    )

    insight_type = "info"


else:

    insight_title = "Room to Improve"

    insight_text = (
        "You are saving some money, but there may be room "
        "to improve your savings rate. Use Planning to "
        "set a structured budget."
    )

    insight_type = "info"


if insight_type == "success":

    st.success(
        f"**{insight_title}**\n\n"
        f"{insight_text}"
    )

elif insight_type == "error":

    st.error(
        f"**{insight_title}**\n\n"
        f"{insight_text}"
    )

elif insight_type == "warning":

    st.warning(
        f"**{insight_title}**\n\n"
        f"{insight_text}"
    )

else:

    st.info(
        f"**{insight_title}**\n\n"
        f"{insight_text}"
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
