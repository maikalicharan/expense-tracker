import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import load_expenses
from utils.calculations import calculate_summary


# =========================================================
# PAGE
# =========================================================

st.title("Dashboard")
st.caption("Your financial overview")


# =========================================================
# LOAD DATA
# =========================================================

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
# CURRENT THEME
# =========================================================

theme = st.session_state.get(
    "theme",
    "Light",
)

is_dark = theme == "Dark"


# =========================================================
# DASHBOARD STYLES
# =========================================================

if is_dark:

    st.markdown(
        """
        <style>

        /* =================================================
           DARK DASHBOARD
        ================================================= */

        .dashboard-section {
            color: #f3f4f6;
        }


        /* =================================================
           METRIC CARDS
        ================================================= */

        .st-key-income_card [data-testid="stMetric"] {
            background-color: #123b27 !important;
            border: 1px solid #2e8b57 !important;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
        }

        .st-key-income_card [data-testid="stMetricLabel"] {
            color: #8ee0ad !important;
        }

        .st-key-income_card [data-testid="stMetricValue"] {
            color: #b8f2cb !important;
        }


        .st-key-expense_card [data-testid="stMetric"] {
            background-color: #421f24 !important;
            border: 1px solid #a84450 !important;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
        }

        .st-key-expense_card [data-testid="stMetricLabel"] {
            color: #f09aa2 !important;
        }

        .st-key-expense_card [data-testid="stMetricValue"] {
            color: #ffc0c6 !important;
        }


        .st-key-balance_card [data-testid="stMetric"] {
            background-color: #172f52 !important;
            border: 1px solid #3978c5 !important;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
        }

        .st-key-balance_card [data-testid="stMetricLabel"] {
            color: #8eb9ed !important;
        }

        .st-key-balance_card [data-testid="stMetricValue"] {
            color: #b9d8ff !important;
        }


        .st-key-savings_card [data-testid="stMetric"] {
            background-color: #30214f !important;
            border: 1px solid #7955b8 !important;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
        }

        .st-key-savings_card [data-testid="stMetricLabel"] {
            color: #c3a9f2 !important;
        }

        .st-key-savings_card [data-testid="stMetricValue"] {
            color: #dfccff !important;
        }


        /* =================================================
           TABLE CONTAINER
        ================================================= */

        .st-key-recent_transactions {
            background-color: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 10px;
            padding: 0.35rem;
        }


        /* =================================================
           INSIGHT
        ================================================= */

        .st-key-financial_insight {
            background-color: #172033 !important;
            border: 1px solid #34445f !important;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            color: #e5e7eb !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

else:

    st.markdown(
        """
        <style>

        /* =================================================
           LIGHT DASHBOARD
        ================================================= */

        .st-key-income_card [data-testid="stMetric"] {
            background-color: #e8f7ee !important;
            border: 1px solid #b9e5c9 !important;
            box-shadow: 0 3px 12px rgba(20, 25, 40, 0.05);
        }

        .st-key-income_card [data-testid="stMetricLabel"] {
            color: #237346 !important;
        }

        .st-key-income_card [data-testid="stMetricValue"] {
            color: #176b3b !important;
        }


        .st-key-expense_card [data-testid="stMetric"] {
            background-color: #fff0ef !important;
            border: 1px solid #f0c4c1 !important;
            box-shadow: 0 3px 12px rgba(20, 25, 40, 0.05);
        }

        .st-key-expense_card [data-testid="stMetricLabel"] {
            color: #a54845 !important;
        }

        .st-key-expense_card [data-testid="stMetricValue"] {
            color: #a52f2f !important;
        }


        .st-key-balance_card [data-testid="stMetric"] {
            background-color: #eaf2ff !important;
            border: 1px solid #c4d7f5 !important;
            box-shadow: 0 3px 12px rgba(20, 25, 40, 0.05);
        }

        .st-key-balance_card [data-testid="stMetricLabel"] {
            color: #315f9f !important;
        }

        .st-key-balance_card [data-testid="stMetricValue"] {
            color: #245ca8 !important;
        }


        .st-key-savings_card [data-testid="stMetric"] {
            background-color: #f3edff !important;
            border: 1px solid #d7c8f2 !important;
            box-shadow: 0 3px 12px rgba(20, 25, 40, 0.05);
        }

        .st-key-savings_card [data-testid="stMetricLabel"] {
            color: #6540a8 !important;
        }

        .st-key-savings_card [data-testid="stMetricValue"] {
            color: #5834a0 !important;
        }


        .st-key-recent_transactions {
            background-color: #ffffff !important;
            border: 1px solid #e3e6ec !important;
            border-radius: 10px;
            padding: 0.35rem;
        }


        .st-key-financial_insight {
            background-color: #ffffff !important;
            border: 1px solid #e2e5eb !important;
            border-radius: 12px;
            padding: 1rem 1.1rem;
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


# =========================================================
# CHART COLORS
# =========================================================

income_bar_color = "#35B96F"
expense_bar_color = "#E45B61"


monthly_chart.update_traces(
    marker_line_width=0,
)


monthly_chart.update_traces(
    marker_color=income_bar_color,
    selector={"name": "Income"},
)


monthly_chart.update_traces(
    marker_color=expense_bar_color,
    selector={"name": "Expenses"},
)


# =========================================================
# CHART THEME
# =========================================================

if is_dark:

    chart_background = "#0f172a"
    chart_text = "#d1d5db"
    chart_grid = "#334155"

else:

    chart_background = "#ffffff"
    chart_text = "#555c69"
    chart_grid = "#eef0f4"


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

    legend=dict(
        font=dict(
            color=chart_text,
        ),
    ),

    xaxis=dict(
        showgrid=False,
        tickfont=dict(
            size=11,
            color=chart_text,
        ),
        linecolor=chart_grid,
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor=chart_grid,
        tickfont=dict(
            size=11,
            color=chart_text,
        ),
        linecolor=chart_grid,
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


    # =====================================================
    # TABLE COLORS
    # =====================================================

    if is_dark:

        table_background = "#111827"
        table_text = "#e5e7eb"
        table_header = "#1e293b"
        table_border = "#334155"

    else:

        table_background = "#ffffff"
        table_text = "#303642"
        table_header = "#f3f5f8"
        table_border = "#e3e6ec"


    styled_table = (
        recent_display.style
        .set_properties(
            **{
                "background-color": table_background,
                "color": table_text,
                "border-color": table_border,
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        (
                            "background-color",
                            table_header,
                        ),
                        (
                            "color",
                            table_text,
                        ),
                        (
                            "font-weight",
                            "600",
                        ),
                        (
                            "border-color",
                            table_border,
                        ),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        (
                            "border-color",
                            table_border,
                        ),
                    ],
                },
            ]
        )
    )


    with st.container(
        key="recent_transactions"
    ):

        st.dataframe(
            styled_table,
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


# =========================================================
# INSIGHT CARD
# =========================================================

with st.container(
    key="financial_insight"
):

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

# --------------------------------------------------
# FINANCIAL GOALS
# --------------------------------------------------

st.divider()

st.subheader("Financial Goals")


try:

    expenses_worksheet = get_google_sheet()

    spreadsheet = expenses_worksheet.spreadsheet

    goals_worksheet = spreadsheet.worksheet(
        "Financial_Goals"
    )

    goal_records = goals_worksheet.get_all_records()

    goals_df = pd.DataFrame(goal_records)

except Exception:

    goals_df = pd.DataFrame()


if goals_df.empty:

    st.info(
        "No financial goals created yet. "
        "Create a goal from the Goals section."
    )

else:

    goals_df["Target Amount"] = pd.to_numeric(
        goals_df["Target Amount"],
        errors="coerce",
    ).fillna(0)

    goals_df["Current Saved"] = pd.to_numeric(
        goals_df["Current Saved"],
        errors="coerce",
    ).fillna(0)


    active_goals = goals_df[
        goals_df["Current Saved"]
        < goals_df["Target Amount"]
    ].copy()


    completed_goals = goals_df[
        goals_df["Current Saved"]
        >= goals_df["Target Amount"]
    ].copy()


    # ----------------------------------------------
    # GOAL SUMMARY
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Active Goals",
            len(active_goals),
        )


    with col2:

        st.metric(
            "Completed Goals",
            len(completed_goals),
        )


    with col3:

        total_remaining = (
            active_goals["Target Amount"]
            - active_goals["Current Saved"]
        ).clip(lower=0).sum()

        st.metric(
            "Total Remaining",
            f"₹{total_remaining:,.2f}",
        )


    st.divider()


    # ----------------------------------------------
    # SHOW ACTIVE GOALS
    # ----------------------------------------------

    if active_goals.empty:

        st.success(
            "🎉 All your financial goals are completed!"
        )

    else:

        for _, goal in active_goals.iterrows():

            goal_name = str(
                goal["Goal Name"]
            )

            target_amount = float(
                goal["Target Amount"]
            )

            current_saved = float(
                goal["Current Saved"]
            )

            remaining_amount = max(
                target_amount - current_saved,
                0,
            )


            if target_amount > 0:

                progress = (
                    current_saved
                    / target_amount
                )

                progress = min(
                    max(progress, 0),
                    1,
                )

            else:

                progress = 0


            st.markdown(
                f"**{goal_name}**"
            )


            st.progress(
                progress,
                text=f"{progress * 100:.1f}% completed",
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.caption("Saved")

                st.write(
                    f"₹{current_saved:,.2f}"
                )


            with col2:

                st.caption("Target")

                st.write(
                    f"₹{target_amount:,.2f}"
                )


            with col3:

                st.caption("Remaining")

                st.write(
                    f"₹{remaining_amount:,.2f}"
                )


            target_date_text = str(
                goal["Target Date"]
            )


            try:

                target_date = pd.to_datetime(
                    target_date_text,
                    dayfirst=True,
                ).date()


                today = date.today()

                days_remaining = (
                    target_date - today
                ).days


                if days_remaining > 0:

                    months_remaining = max(
                        days_remaining / 30.44,
                        1,
                    )


                    required_monthly_saving = (
                        remaining_amount
                        / months_remaining
                    )


                    st.caption(
                        f"Target: {target_date.strftime('%d/%m/%Y')} "
                        f"• {days_remaining} days remaining "
                        f"• Required monthly saving: "
                        f"₹{required_monthly_saving:,.2f}"
                    )

                else:

                    st.warning(
                        "Target date has passed."
                    )

            except Exception:

                st.caption(
                    f"Target: {target_date_text}"
                )


            st.divider()
