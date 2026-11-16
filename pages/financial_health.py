import streamlit as st
import pandas as pd

from utils.data import load_expenses
from utils.sheets import get_google_sheet
from utils.planning import (
    calculate_budget_actuals,
    calculate_planned_amounts,
)
from utils.financial_health import (
    calculate_financial_health,
    generate_financial_insights,
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Financial Health",
    layout="wide",
)


# ==================================================
# LOAD DATA
# ==================================================

try:
    df = load_expenses()

except Exception as e:
    st.error("Unable to load financial data.")
    st.exception(e)
    st.stop()


if df.empty:
    st.info(
        "Add some transactions first to calculate your Financial Health."
    )
    st.stop()


df = df.copy()

df = df.dropna(
    subset=["Date"]
)

df["Year"] = df["Date"].dt.year


# ==================================================
# HEADER
# ==================================================

st.title("Financial Health")

st.caption(
    "A simple view of your financial strength, spending behaviour and progress."
)


# ==================================================
# YEAR
# ==================================================

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


if year_df.empty:
    st.info(
        "No transactions found for the selected year."
    )
    st.stop()


# ==================================================
# CORE FINANCIAL VALUES
# ==================================================

total_income = year_df.loc[
    year_df["Type"] == "Income",
    "Amount",
].sum()


total_expenses = year_df.loc[
    year_df["Type"] == "Expense",
    "Expense Amount",
].sum()


net_savings = (
    total_income
    - total_expenses
)


if total_income > 0:

    savings_rate = (
        net_savings
        / total_income
        * 100
    )

    expense_ratio = (
        total_expenses
        / total_income
        * 100
    )

else:

    savings_rate = 0.0
    expense_ratio = 100.0


# ==================================================
# GOOGLE SHEETS
# ==================================================

try:

    spreadsheet = (
        get_google_sheet()
        .spreadsheet
    )

except Exception:

    spreadsheet = None


# ==================================================
# LOAD BUDGET PLAN
# ==================================================

saved_plan = None


if spreadsheet is not None:

    try:

        budget_worksheet = spreadsheet.worksheet(
            "Budget_Plans"
        )

        budget_records = (
            budget_worksheet
            .get_all_records()
        )

    except Exception:

        budget_records = []

else:

    budget_records = []


for record in budget_records:

    try:

        record_year = int(
            float(
                record.get(
                    "Year",
                    0,
                )
            )
        )

    except (
        ValueError,
        TypeError,
    ):

        continue


    if record_year == selected_year:

        saved_plan = record
        break


# ==================================================
# BUDGET PERCENTAGES
# ==================================================

if saved_plan is not None:

    try:

        needs_percent = float(
            saved_plan.get(
                "Needs %",
                50,
            )
            or 50
        )

    except (
        ValueError,
        TypeError,
    ):

        needs_percent = 50.0


    try:

        investment_percent = float(
            saved_plan.get(
                "Investment %",
                20,
            )
            or 20
        )

    except (
        ValueError,
        TypeError,
    ):

        investment_percent = 20.0


    try:

        lifestyle_percent = float(
            saved_plan.get(
                "Lifestyle %",
                30,
            )
            or 30
        )

    except (
        ValueError,
        TypeError,
    ):

        lifestyle_percent = 30.0

else:

    needs_percent = 50.0
    investment_percent = 20.0
    lifestyle_percent = 30.0


# ==================================================
# CATEGORY MAPPING
# ==================================================

category_mapping = {}


if spreadsheet is not None:

    try:

        category_worksheet = spreadsheet.worksheet(
            "Budget_Categories"
        )

        category_records = (
            category_worksheet
            .get_all_records()
        )

    except Exception:

        category_records = []


    for record in category_records:

        category = str(
            record.get(
                "Category",
                "",
            )
        ).strip()


        bucket = str(
            record.get(
                "Planning Bucket",
                "",
            )
        ).strip()


        if category and bucket:

            category_mapping[category] = bucket


# ==================================================
# ACTUAL BUDGET SPENDING
# ==================================================

expense_df = year_df[
    year_df["Type"] == "Expense"
].copy()


actual = calculate_budget_actuals(
    expense_df,
    category_mapping,
)


# ==================================================
# PLANNED AMOUNTS
# ==================================================

planned = calculate_planned_amounts(
    total_income,
    needs_percent,
    investment_percent,
    lifestyle_percent,
)


# ==================================================
# EMERGENCY FUND
# ==================================================

monthly_needs = 0.0


if not expense_df.empty:

    mapped_categories = (
        expense_df["Category"]
        .fillna("")
        .astype(str)
        .str.strip()
        .map(category_mapping)
        .fillna("Needs")
    )

    needs_expenses = expense_df[
        mapped_categories == "Needs"
    ].copy()


    if not needs_expenses.empty:

        monthly_needs = (
            needs_expenses
            .groupby(
                needs_expenses["Date"].dt.to_period("M")
            )["Expense Amount"]
            .sum()
            .mean()
        )


if pd.isna(monthly_needs):

    monthly_needs = 0.0


# ==================================================
# AVAILABLE SAVINGS
# ==================================================

available_savings = max(
    net_savings,
    0,
)


if monthly_needs > 0:

    emergency_months = (
        available_savings
        / monthly_needs
    )

else:

    emergency_months = 0.0


# ==================================================
# GOALS
# ==================================================

goals_df = pd.DataFrame()


if spreadsheet is not None:

    try:

        goals_worksheet = spreadsheet.worksheet(
            "Financial_Goals"
        )

        goals_records = (
            goals_worksheet
            .get_all_records()
        )

        goals_df = pd.DataFrame(
            goals_records
        )

    except Exception:

        goals_df = pd.DataFrame()


# ==================================================
# GOAL PROGRESS
# ==================================================

goal_progress = 0.0


if not goals_df.empty:

    goals_df["Target Amount"] = pd.to_numeric(
        goals_df.get(
            "Target Amount",
            0,
        ),
        errors="coerce",
    ).fillna(0)


    goals_df["Current Saved"] = pd.to_numeric(
        goals_df.get(
            "Current Saved",
            0,
        ),
        errors="coerce",
    ).fillna(0)


    valid_goals = goals_df[
        goals_df["Target Amount"] > 0
    ].copy()


    if not valid_goals.empty:

        goal_progress = (
            valid_goals["Current Saved"]
            /
            valid_goals["Target Amount"]
        ).clip(
            lower=0,
            upper=1,
        ).mean()


# ==================================================
# INVESTMENT
# ==================================================

investment_amount = actual.get(
    "Investment",
    0,
)


if total_income > 0:

    investment_rate = (
        investment_amount
        / total_income
        * 100
    )

else:

    investment_rate = 0.0


# ==================================================
# FINANCIAL HEALTH SCORE
# ==================================================

health = calculate_financial_health(
    savings_rate=savings_rate,
    expense_ratio=expense_ratio,
    planned=planned,
    actual=actual,
    available_savings=available_savings,
    monthly_needs=monthly_needs,
    goals_df=goals_df,
    income=total_income,
    investment_amount=investment_amount,
)


# ==================================================
# INSIGHTS
# ==================================================

insights = generate_financial_insights(
    savings_rate=savings_rate,
    expense_ratio=expense_ratio,
    emergency_months=emergency_months,
    goal_progress=goal_progress,
    investment_rate=investment_rate,
    budget_score=health["budget_score"],
)


# ==================================================
# SCORE HEADER
# ==================================================

st.divider()

score_col, status_col = st.columns(
    [1, 2]
)


with score_col:

    st.metric(
        "Financial Health Score",
        f"{health['total_score']} / 100",
    )


with status_col:

    status = health["status"]


    if status == "Excellent":

        st.success(
            "Excellent"
        )

    elif status == "Healthy":

        st.success(
            "Healthy"
        )

    elif status == "Moderate":

        st.info(
            "Moderate"
        )

    elif status == "Needs Improvement":

        st.warning(
            "Needs Improvement"
        )

    else:

        st.error(
            "Needs Attention"
        )


# Score progress

st.progress(
    health["total_score"] / 100
)


# Short explanation

if status == "Excellent":

    st.caption(
        "Your financial position is strong. Keep maintaining these habits."
    )

elif status == "Healthy":

    st.caption(
        "Your finances are in a healthy range. A few improvements can make them stronger."
    )

elif status == "Moderate":

    st.caption(
        "Your financial position is moderate. There are several areas where you can improve."
    )

elif status == "Needs Improvement":

    st.caption(
        "Your finances need some attention. Focus on the areas highlighted below."
    )

else:

    st.caption(
        "Your current financial position needs attention. Start with the most important actions below."
    )


# ==================================================
# SCORE BREAKDOWN
# ==================================================

st.divider()

st.subheader(
    "Score Breakdown"
)


score_cards = [
    (
        "Savings Rate",
        health["savings_score"],
        25,
        f"{savings_rate:.1f}% of income saved",
    ),
    (
        "Expense Control",
        health["expense_score"],
        20,
        f"{expense_ratio:.1f}% of income spent",
    ),
    (
        "Budget Discipline",
        health["budget_score"],
        20,
        "Planned vs actual spending",
    ),
    (
        "Emergency Fund",
        health["emergency_score"],
        15,
        f"{emergency_months:.1f} months covered",
    ),
    (
        "Financial Goals",
        health["goal_score"],
        10,
        f"{goal_progress * 100:.1f}% average progress",
    ),
    (
        "Investment Allocation",
        health["investment_score"],
        10,
        f"{investment_rate:.1f}% allocated",
    ),
]


for row_start in range(
    0,
    len(score_cards),
    3,
):

    columns = st.columns(3)


    for column, card in zip(
        columns,
        score_cards[row_start:row_start + 3],
    ):

        title, score, maximum, caption = card


        with column:

            st.metric(
                title,
                f"{score} / {maximum}",
            )

            st.caption(
                caption
            )


# ==================================================
# FINANCIAL POSITION
# ==================================================

st.divider()

st.subheader(
    "Financial Position"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Received",
        f"₹{total_income:,.2f}",
    )


with col2:

    st.metric(
        "Total Spent",
        f"₹{total_expenses:,.2f}",
    )


with col3:

    st.metric(
        "Net Savings",
        f"₹{net_savings:,.2f}",
    )


with col4:

    st.metric(
        "Emergency Coverage",
        f"{emergency_months:.1f} months",
    )


# ==================================================
# BUDGET POSITION
# ==================================================

st.divider()

st.subheader(
    "Budget Position"
)

st.caption(
    "Planned allocation compared with actual spending."
)


budget_data = pd.DataFrame(
    {
        "Planned": [
            planned["Needs"],
            planned["Investment"],
            planned["Lifestyle"],
        ],
        "Actual": [
            actual["Needs"],
            actual["Investment"],
            actual["Lifestyle"],
        ],
    },
    index=[
        "Needs",
        "Investment",
        "Lifestyle",
    ],
)


st.bar_chart(
    budget_data
)


# ==================================================
# INSIGHTS
# ==================================================

st.divider()

st.subheader(
    "Financial Insights"
)


if insights["strengths"]:

    st.markdown(
        "#### Strong Areas"
    )

    for item in insights["strengths"]:

        st.success(
            item
        )


if insights["attention"]:

    st.markdown(
        "#### Needs Attention"
    )

    for item in insights["attention"]:

        st.warning(
            item
        )


if insights["actions"]:

    st.markdown(
        "#### Recommended Actions"
    )

    for index, item in enumerate(
        insights["actions"],
        start=1,
    ):

        st.write(
            f"{index}. {item}"
        )


# ==================================================
# GOALS PROGRESS
# ==================================================

st.divider()

st.subheader(
    "Goals Progress"
)


if goals_df.empty:

    st.info(
        "No financial goals have been created yet."
    )

else:

    display_goals = goals_df.copy()


    display_goals["Progress"] = (
        display_goals["Current Saved"]
        /
        display_goals["Target Amount"]
    ).replace(
        [float("inf")],
        0,
    ).fillna(0).clip(
        lower=0,
        upper=1,
    )


    for _, goal in display_goals.iterrows():

        goal_name = str(
            goal.get(
                "Goal Name",
                "Goal",
            )
        )


        current_saved = float(
            goal.get(
                "Current Saved",
                0,
            )
        )


        target_amount = float(
            goal.get(
                "Target Amount",
                0,
            )
        )


        progress = float(
            goal["Progress"]
        )


        st.markdown(
            f"**{goal_name}**"
        )


        st.caption(
            f"₹{current_saved:,.2f} "
            f"of ₹{target_amount:,.2f} "
            f"• {progress * 100:.1f}%"
        )


        st.progress(
            progress
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    f"Financial Health for {selected_year} • "
    "Based on transactions, budget planning, "
    "category mapping and financial goals."
)
