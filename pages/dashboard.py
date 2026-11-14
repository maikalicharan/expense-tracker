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

    /* =================================================
       ALL METRIC CARDS
    ================================================= */

    [data-testid="stMetric"] {
        border-radius: 12px;
        padding: 0.9rem 1rem;
        min-height: 105px;

        box-shadow:
            0 2px 8px rgba(20, 25, 40, 0.05);

        border: 1px solid;
    }


    /* =================================================
       INCOME - GREEN
    ================================================= */

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(1)
    [data-testid="stMetric"] {
        background-color: #e8f7ee !important;
        border-color: #b9e5c9 !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(1)
    [data-testid="stMetricLabel"] {
        color: #237346 !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(1)
    [data-testid="stMetricValue"] {
        color: #176b3b !important;
    }


    /* =================================================
       EXPENSES - RED
    ================================================= */

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(2)
    [data-testid="stMetric"] {
        background-color: #fff0ef !important;
        border-color: #f0c4c1 !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(2)
    [data-testid="stMetricLabel"] {
        color: #a54845 !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(2)
    [data-testid="stMetricValue"] {
        color: #a52f2f !important;
    }


    /* =================================================
       BALANCE - BLUE
    ================================================= */

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(3)
    [data-testid="stMetric"] {
        background-color: #eaf2ff !important;
        border-color: #c4d7f5 !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(3)
    [data-testid="stMetricLabel"] {
        color: #315f9f !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(3)
    [data-testid="stMetricValue"] {
        color: #245ca8 !important;
    }


    /* =================================================
       SAVINGS - PURPLE
    ================================================= */

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(4)
    [data-testid="stMetric"] {
        background-color: #f3edff !important;
        border-color: #d7c8f2 !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(4)
    [data-testid="stMetricLabel"] {
        color: #6540a8 !important;
    }

    [data-testid="stHorizontalBlock"]
    > [data-testid="column"]:nth-child(4)
    [data-testid="stMetricValue"] {
        color: #5834a0 !important;
    }


    /* =================================================
       TEXT SIZE
    ================================================= */

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
    st.metric(
        "Total Income",
        f"₹{total_income:,.2f}",
    )


with col2:
    st.metric(
        "Total Expenses",
        f"₹{total_expenses:,.2f}",
    )


with col3:
    st.metric(
        "Current Balance",
        f"₹{balance:,.2f}",
    )


with col4:
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
