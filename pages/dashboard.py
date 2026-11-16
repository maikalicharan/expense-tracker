import streamlit as st
import pandas as pd

from utils.data import load_expenses
from utils.sheets import get_google_sheet

from utils.planning import (
    calculate_budget_actuals,
    calculate_planned_amounts,
)

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
)


# ==================================================
# LOAD TRANSACTION DATA
# ==================================================

try:
    df = load_expenses()

except Exception as e:
    st.error("Unable to load dashboard data.")
    st.exception(e)
    st.stop()


if df.empty:
    st.info(
        "No transactions available yet. "
        "Add your first transaction from Add Transaction."
    )
    st.stop()


df = df.copy()

df = df.dropna(
    subset=["Date"]
)

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month Period"] = df["Date"].dt.to_period("M")


# ==================================================
# HEADER
# ==================================================

st.title("Dashboard")
st.caption(
    "Your financial overview and planning summary"
)


# ==================================================
# YEAR SELECTION
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
# CORE FINANCIAL NUMBERS
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
else:
    savings_rate = 0


# ==================================================
# FINANCIAL OVERVIEW
# ==================================================

st.divider()

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
        "Savings Rate",
        f"{savings_rate:.1f}%",
    )


# ==================================================
# MONTHLY CASH FLOW
# ==================================================

st.divider()

st.subheader(
    f"Monthly Cash Flow — {selected_year}"
)


monthly_income = (
    year_df[
        year_df["Type"] == "Income"
    ]
    .groupby("Month")["Amount"]
    .sum()
)


monthly_expenses = (
    year_df[
        year_df["Type"] == "Expense"
    ]
    .groupby("Month")["Expense Amount"]
    .sum()
)


month_labels = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


monthly_chart = pd.DataFrame(
    {
        "Received": [
            monthly_income.get(
                month,
                0,
            )
            for month in range(1, 13)
        ],
        "Spent": [
            monthly_expenses.get(
                month,
                0,
            )
            for month in range(1, 13)
        ],
    },
    index=month_labels,
)


st.bar_chart(
    monthly_chart,
)


# ==================================================
# BUDGET SUMMARY
# ==================================================

st.divider()

st.subheader("Budget Status")


try:
    category_worksheet = (
        get_google_sheet()
        .spreadsheet
        .worksheet("Budget_Categories")
    )

    category_records = (
        category_worksheet
        .get_all_records()
    )

except Exception:
    category_records = []


category_mapping = {}

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


expense_df = year_df[
    year_df["Type"] == "Expense"
].copy()


actual = calculate_budget_actuals(
    expense_df,
    category_mapping,
)


planned = calculate_planned_amounts(
    total_income,
    needs_percent,
    investment_percent,
    lifestyle_percent,
)


    def classify_category(category):

        category = str(
            category
        ).strip().lower()


        investment_keywords = [
            "investment",
            "investments",
            "sip",
            "mutual fund",
            "mutual funds",
            "stocks",
            "shares",
            "equity",
            "ppf",
            "pf",
            "epf",
            "nps",
            "fd",
            "fixed deposit",
            "rd",
            "recurring deposit",
        ]


        lifestyle_keywords = [
            "shopping",
            "entertainment",
            "travel",
            "restaurant",
            "dining",
            "food",
            "movies",
            "hobbies",
            "luxury",
            "subscription",
            "subscriptions",
            "leisure",
            "gaming",
        ]


        for keyword in investment_keywords:

            if keyword in category:
                return "Investment"


        for keyword in lifestyle_keywords:

            if keyword in category:
                return "Lifestyle"


        return "Needs"


    expense_df = year_df[
        year_df["Type"] == "Expense"
    ].copy()


    if not expense_df.empty:

        expense_df["Planning Bucket"] = (
            expense_df["Category"]
            .apply(
                classify_category
            )
        )


    actual_needs = expense_df.loc[
        expense_df["Planning Bucket"]
        == "Needs",
        "Expense Amount",
    ].sum()


    actual_investment = expense_df.loc[
        expense_df["Planning Bucket"]
        == "Investment",
        "Expense Amount",
    ].sum()


    actual_lifestyle = expense_df.loc[
        expense_df["Planning Bucket"]
        == "Lifestyle",
        "Expense Amount",
    ].sum()


    budget_data = pd.DataFrame(
        {
            "Planned": [
                planned_needs,
                planned_investment,
                planned_lifestyle,
            ],
            "Actual": [
                actual_needs,
                actual_investment,
                actual_lifestyle,
            ],
        },
        index=[
            "Needs",
            "Investment",
            "Lifestyle",
        ],
    )


    st.bar_chart(
        budget_data,
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        difference = (
            planned_needs
            - actual_needs
        )

        if difference >= 0:

            st.success(
                f"Needs\n\n"
                f"₹{difference:,.2f} remaining"
            )

        else:

            st.warning(
                f"Needs\n\n"
                f"₹{abs(difference):,.2f} over budget"
            )


    with col2:

        difference = (
            planned_investment
            - actual_investment
        )

        if difference >= 0:

            st.success(
                f"Investment\n\n"
                f"₹{difference:,.2f} remaining"
            )

        else:

            st.warning(
                f"Investment\n\n"
                f"₹{abs(difference):,.2f} over budget"
            )


    with col3:

        difference = (
            planned_lifestyle
            - actual_lifestyle
        )

        if difference >= 0:

            st.success(
                f"Lifestyle\n\n"
                f"₹{difference:,.2f} remaining"
            )

        else:

            st.warning(
                f"Lifestyle\n\n"
                f"₹{abs(difference):,.2f} over budget"
            )


# ==================================================
# GOALS SUMMARY
# ==================================================

st.divider()

st.subheader("Goals")


try:

    spreadsheet = get_google_sheet().spreadsheet

    goals_worksheet = (
        spreadsheet
        .worksheet("Financial_Goals")
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


if goals_df.empty:

    st.info(
        "No financial goals created yet. "
        "Create your first goal from Goals."
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


    goals_df["Remaining"] = (
        goals_df["Target Amount"]
        - goals_df["Current Saved"]
    ).clip(
        lower=0
    )


    goals_df["Progress"] = 0.0


    valid_targets = (
        goals_df["Target Amount"]
        > 0
    )


    goals_df.loc[
        valid_targets,
        "Progress",
    ] = (
        goals_df.loc[
            valid_targets,
            "Current Saved",
        ]
        /
        goals_df.loc[
            valid_targets,
            "Target Amount",
        ]
    )


    goals_df["Progress"] = (
        goals_df["Progress"]
        .clip(
            lower=0,
            upper=1,
        )
    )


    active_goals = goals_df[
        goals_df["Remaining"] > 0
    ].copy()


    completed_goals = goals_df[
        goals_df["Remaining"] <= 0
    ].copy()


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
            active_goals["Remaining"]
            .sum()
        )

        st.metric(
            "Total Remaining",
            f"₹{total_remaining:,.2f}",
        )


    if not active_goals.empty:

        for _, goal in active_goals.iterrows():

            goal_name = str(
                goal["Goal Name"]
            )

            current_saved = float(
                goal["Current Saved"]
            )

            target_amount = float(
                goal["Target Amount"]
            )

            remaining = float(
                goal["Remaining"]
            )

            progress = float(
                goal["Progress"]
            )


            st.write(
                f"**{goal_name}**"
            )


            st.progress(
                progress
            )


            st.caption(
                f"₹{current_saved:,.2f} saved "
                f"of ₹{target_amount:,.2f} "
                f"• ₹{remaining:,.2f} remaining "
                f"• {progress * 100:.1f}%"
            )


# ==================================================
# FINANCIAL HEALTH SUMMARY
# ==================================================

st.divider()

st.subheader("Financial Health")


if total_income <= 0:

    st.error(
        "Needs Attention"
    )

    st.caption(
        "Add income transactions to analyse "
        "your financial health."
    )

elif net_savings < 0:

    st.error(
        "Needs Attention"
    )

    st.caption(
        "Your expenses are currently higher "
        "than your income."
    )

elif savings_rate >= 30:

    st.success(
        "Strong"
    )

    st.caption(
        "You are maintaining a strong savings rate."
    )

elif savings_rate >= 20:

    st.info(
        "Good"
    )

    st.caption(
        "Your savings rate is in a healthy range."
    )

elif savings_rate >= 10:

    st.warning(
        "Moderate"
    )

    st.caption(
        "There is room to improve your savings rate."
    )

else:

    st.warning(
        "Needs Improvement"
    )

    st.caption(
        "Consider reviewing your spending and "
        "budget allocation."
    )


# ==================================================
# RECENT TRANSACTIONS
# ==================================================

st.divider()

st.subheader("Recent Activity")


recent_df = (
    year_df
    .sort_values(
        "Date",
        ascending=False,
    )
    .head(5)
    .copy()
)


recent_df["Date"] = (
    recent_df["Date"]
    .dt.strftime(
        "%d/%m/%Y"
    )
)


recent_df["Amount"] = (
    recent_df["Amount"]
    .abs()
)


recent_df = recent_df[
    [
        "Date",
        "Description",
        "Category",
        "Amount",
        "Type",
    ]
]


st.dataframe(
    recent_df,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Date": st.column_config.TextColumn(
            "Date",
        ),

        "Description": st.column_config.TextColumn(
            "Description",
        ),

        "Category": st.column_config.TextColumn(
            "Category",
        ),

        "Amount": st.column_config.NumberColumn(
            "Amount",
            format="₹%.2f",
        ),

        "Type": st.column_config.TextColumn(
            "Type",
        ),
    },
)


# ==================================================
# QUICK INSIGHT
# ==================================================

st.divider()

st.subheader("Quick Insight")


if total_income <= 0:

    st.info(
        "Start by adding your income transactions."
    )

elif net_savings < 0:

    st.warning(
        f"For {selected_year}, your spending is "
        f"₹{abs(net_savings):,.2f} higher than "
        "your income."
    )

elif savings_rate < 10:

    st.warning(
        f"You saved ₹{net_savings:,.2f} during "
        f"{selected_year}. Increasing your savings "
        "rate could strengthen your financial position."
    )

elif savings_rate < 20:

    st.info(
        f"You saved ₹{net_savings:,.2f} during "
        f"{selected_year}. There is room to gradually "
        "increase your savings rate."
    )

else:

    st.success(
        f"You saved ₹{net_savings:,.2f} during "
        f"{selected_year}, giving you a "
        f"{savings_rate:.1f}% savings rate."
    )
