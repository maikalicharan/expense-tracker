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
# FINANCIAL OVERVIEW
# =========================================================

st.subheader("Financial Overview")


st.markdown(
    """
    <style>

    /* Base card */

    [data-testid="stMetric"] {
        border-radius: 12px;
        padding: 0.9rem 1rem;
        min-height: 105px;

        border: 1px solid;

        box-shadow:
            0 2px 8px rgba(20, 25, 40, 0.05);
    }


    /* Income */

    .st-key-income_card [data-testid="stMetric"] {
        background-color: #e8f7ee !important;
        border-color: #b9e5c9 !important;
    }

    .st-key-income_card [data-testid="stMetricLabel"] {
        color: #237346 !important;
    }

    .st-key-income_card [data-testid="stMetricValue"] {
        color: #176b3b !important;
    }


    /* Expenses */

    .st-key-expense_card [data-testid="stMetric"] {
        background-color: #fff0ef !important;
        border-color: #f0c4c1 !important;
    }

    .st-key-expense_card [data-testid="stMetricLabel"] {
        color: #a54845 !important;
    }

    .st-key-expense_card [data-testid="stMetricValue"] {
        color: #a52f2f !important;
    }


    /* Balance */

    .st-key-balance_card [data-testid="stMetric"] {
        background-color: #eaf2ff !important;
        border-color: #c4d7f5 !important;
    }

    .st-key-balance_card [data-testid="stMetricLabel"] {
        color: #315f9f !important;
    }

    .st-key-balance_card [data-testid="stMetricValue"] {
        color: #245ca8 !important;
    }


    /* Savings */

    .st-key-savings_card [data-testid="stMetric"] {
        background-color: #f3edff !important;
        border-color: #d7c8f2 !important;
    }

    .st-key-savings_card [data-testid="stMetricLabel"] {
        color: #6540a8 !important;
    }

    .st-key-savings_card [data-testid="stMetricValue"] {
        color: #5834a0 !important;
    }


    /* Text */

    [data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        font-weight: 750 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    with st.container(key="income_card"):

        st.metric(
            "Total Income",
            f"₹{total_income:,.2f}",
        )


with col2:

    with st.container(key="expense_card"):

        st.metric(
            "Total Expenses",
            f"₹{total_expenses:,.2f}",
        )


with col3:

    with st.container(key="balance_card"):

        st.metric(
            "Current Balance",
            f"₹{balance:,.2f}",
        )


with col4:

    with st.container(key="savings_card"):

        st.metric(
            "Savings Rate",
            f"{savings_percentage:.1f}%",
        )

# =========================================================
# MONTHLY OVERVIEW
# =========================================================

st.divider()

st.subheader("Monthly Overview")

st.caption("Income and expenses by month")


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


theme = st.session_state.get("theme", "Light")

if theme == "Dark":

    chart_background = "#0f172a"
    chart_grid = "#334155"
    chart_text = "#cbd5e1"

else:

    chart_background = "white"
    chart_grid = "#eef0f4"
    chart_text = "#555c69"


monthly_chart.update_layout(
    height=390,

    plot_bgcolor=chart_background,
    paper_bgcolor=chart_background,

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
        color=chart_text,
    ),

    xaxis=dict(
        showgrid=False,
        tickfont=dict(
            size=11,
            color=chart_text,
        ),
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor=chart_grid,
        tickfont=dict(
            size=11,
            color=chart_text,
        ),
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

st.caption("Your latest five transactions")


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
