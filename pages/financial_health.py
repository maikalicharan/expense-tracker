import streamlit as st
import pandas as pd

from utils.data import load_expenses
from utils.sheets import get_google_sheet


st.set_page_config(
    page_title="Financial Health",
    layout="wide",
)


st.title("Financial Health")
st.caption(
    "Understand your income, spending, savings and financial goals"
)


# ==================================================
# LOAD TRANSACTION DATA
# ==================================================

try:

    df = load_expenses()

except Exception as e:

    st.error("Unable to load financial data.")
    st.exception(e)
    st.stop()


if df.empty:

    st.info(
        "Add some income and expense transactions "
        "to start analysing your financial health."
    )

    st.stop()


df = df.copy()

df = df.dropna(
    subset=["Date"]
)


# ==================================================
# YEAR DATA
# ==================================================

df["Year"] = (
    df["Date"]
    .dt.year
)


df["Month Period"] = (
    df["Date"]
    .dt.to_period("M")
)


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
# BASIC FINANCIAL CALCULATIONS
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
    ) * 100

    expense_ratio = (
        total_expenses
        / total_income
    ) * 100

else:

    savings_rate = 0
    expense_ratio = 0


# ==================================================
# MONTHLY ANALYSIS
# ==================================================

monthly_income = (
    year_df[
        year_df["Type"] == "Income"
    ]
    .groupby("Month Period")[
        "Amount"
    ]
    .sum()
)


monthly_expenses = (
    year_df[
        year_df["Type"] == "Expense"
    ]
    .groupby("Month Period")[
        "Expense Amount"
    ]
    .sum()
)


monthly_analysis = pd.DataFrame(
    {
        "Income": monthly_income,
        "Expenses": monthly_expenses,
    }
).fillna(0)


monthly_analysis["Savings"] = (
    monthly_analysis["Income"]
    - monthly_analysis["Expenses"]
)


number_of_months = len(
    monthly_analysis
)


if number_of_months > 0:

    average_monthly_income = (
        monthly_analysis["Income"].mean()
    )

    average_monthly_expenses = (
        monthly_analysis["Expenses"].mean()
    )

    average_monthly_savings = (
        monthly_analysis["Savings"].mean()
    )

else:

    average_monthly_income = 0
    average_monthly_expenses = 0
    average_monthly_savings = 0


positive_months = (
    monthly_analysis["Savings"] > 0
).sum()


negative_months = (
    monthly_analysis["Savings"] < 0
).sum()


zero_months = (
    monthly_analysis["Savings"] == 0
).sum()


# ==================================================
# FINANCIAL OVERVIEW
# ==================================================

st.divider()

st.subheader("Financial Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Savings Rate",
        f"{savings_rate:.1f}%",
    )


with col2:

    st.metric(
        "Expense Ratio",
        f"{expense_ratio:.1f}%",
    )


with col3:

    st.metric(
        "Net Savings",
        f"₹{net_savings:,.2f}",
    )


with col4:

    st.metric(
        "Months Analysed",
        number_of_months,
    )


# ==================================================
# MONTHLY AVERAGES
# ==================================================

st.divider()

st.subheader("Monthly Averages")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Monthly Income",
        f"₹{average_monthly_income:,.2f}",
    )


with col2:

    st.metric(
        "Average Monthly Expenses",
        f"₹{average_monthly_expenses:,.2f}",
    )


with col3:

    st.metric(
        "Average Monthly Savings",
        f"₹{average_monthly_savings:,.2f}",
    )


# ==================================================
# FINANCIAL STABILITY
# ==================================================

st.divider()

st.subheader("Financial Stability")


if total_income <= 0:

    stability = "Needs Attention"

    stability_text = (
        "There is not enough income data to evaluate "
        "your financial stability."
    )

elif net_savings < 0:

    stability = "Needs Attention"

    stability_text = (
        "Your expenses are higher than your income "
        "for the selected year."
    )

elif savings_rate >= 30:

    stability = "Strong"

    stability_text = (
        "You are maintaining a strong savings rate "
        "relative to your income."
    )

elif savings_rate >= 20:

    stability = "Good"

    stability_text = (
        "Your savings rate is in a healthy range. "
        "Continue monitoring your spending."
    )

elif savings_rate >= 10:

    stability = "Moderate"

    stability_text = (
        "You are saving money, but there is room "
        "to improve your savings rate."
    )

else:

    stability = "Needs Improvement"

    stability_text = (
        "Your current savings rate is low. "
        "Review your expenses and planning targets."
    )


if stability == "Strong":

    st.success(
        f"**{stability}** — {stability_text}"
    )

elif stability == "Good":

    st.info(
        f"**{stability}** — {stability_text}"
    )

elif stability == "Moderate":

    st.warning(
        f"**{stability}** — {stability_text}"
    )

else:

    st.error(
        f"**{stability}** — {stability_text}"
    )


# ==================================================
# GOALS ANALYSIS
# ==================================================

st.divider()

st.subheader("Goals Progress")


try:

    spreadsheet = get_google_sheet().spreadsheet

    try:

        goals_worksheet = (
            spreadsheet.worksheet(
                "Financial_Goals"
            )
        )

        goals_records = (
            goals_worksheet.get_all_records()
        )

        goals_df = pd.DataFrame(
            goals_records
        )

    except Exception:

        goals_df = pd.DataFrame()


except Exception:

    goals_df = pd.DataFrame()


if goals_df.empty:

    st.info(
        "No financial goals have been created yet. "
        "Create goals from the Goals section."
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
    ).clip(lower=0)


    goals_df["Progress"] = 0.0


    positive_target = (
        goals_df["Target Amount"] > 0
    )


    goals_df.loc[
        positive_target,
        "Progress"
    ] = (
        goals_df.loc[
            positive_target,
            "Current Saved"
        ]
        /
        goals_df.loc[
            positive_target,
            "Target Amount"
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


    total_goal_target = (
        goals_df["Target Amount"].sum()
    )


    total_goal_saved = (
        goals_df["Current Saved"].sum()
    )


    total_goal_remaining = (
        active_goals["Remaining"].sum()
    )


    col1, col2, col3, col4 = st.columns(4)


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

        st.metric(
            "Goal Amount",
            f"₹{total_goal_target:,.2f}",
        )


    with col4:

        st.metric(
            "Goal Remaining",
            f"₹{total_goal_remaining:,.2f}",
        )


    if not active_goals.empty:

        st.markdown(
            "### Active Goal Funding"
        )


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
                f"Saved ₹{current_saved:,.2f} "
                f"of ₹{target_amount:,.2f} "
                f"• Remaining ₹{remaining:,.2f}"
            )


# ==================================================
# GOAL FUNDING VS SAVINGS
# ==================================================

st.divider()

st.subheader("Goal Funding Capacity")


if not goals_df.empty and not active_goals.empty:

    monthly_goal_requirement = 0.0


    if "Target Date" in active_goals.columns:

        today = pd.Timestamp.today().normalize()


        for _, goal in active_goals.iterrows():

            target_date = pd.to_datetime(
                goal["Target Date"],
                errors="coerce",
            )


            remaining = float(
                goal["Remaining"]
            )


            if pd.isna(target_date):

                continue


            months_remaining = (
                (
                    target_date.year
                    - today.year
                )
                * 12
                +
                (
                    target_date.month
                    - today.month
                )
            )


            if months_remaining <= 0:

                months_remaining = 1


            monthly_goal_requirement += (
                remaining
                / months_remaining
            )


    if monthly_goal_requirement > 0:

        st.metric(
            "Estimated Monthly Goal Saving Needed",
            f"₹{monthly_goal_requirement:,.2f}",
        )


        if average_monthly_savings >= (
            monthly_goal_requirement
        ):

            st.success(
                "Your average monthly savings are "
                "currently sufficient to cover the "
                "estimated goal funding requirement."
            )

        else:

            shortfall = (
                monthly_goal_requirement
                - average_monthly_savings
            )


            st.warning(
                f"Your average monthly savings are "
                f"approximately ₹{shortfall:,.2f} "
                "below the estimated goal funding requirement."
            )

    else:

        st.info(
            "Goal target dates are not available, "
            "so monthly goal funding cannot be estimated."
        )

else:

    st.info(
        "Create an active financial goal with a target date "
        "to analyse goal funding capacity."
    )


# ==================================================
# MONTHLY CASH FLOW
# ==================================================

st.divider()

st.subheader("Monthly Cash Flow")


monthly_display = (
    monthly_analysis
    .reset_index()
)


monthly_display["Month"] = (
    monthly_display[
        "Month Period"
    ]
    .astype(str)
)


monthly_display = monthly_display[
    [
        "Month",
        "Income",
        "Expenses",
        "Savings",
    ]
].copy()


# Show all amounts as positive where appropriate.
# Savings remains signed because it represents
# positive/negative cash flow.


st.dataframe(
    monthly_display,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Month": "Month",

        "Income": st.column_config.NumberColumn(
            "Income",
            format="₹%.2f",
        ),

        "Expenses": st.column_config.NumberColumn(
            "Expenses",
            format="₹%.2f",
        ),

        "Savings": st.column_config.NumberColumn(
            "Savings",
            format="₹%.2f",
        ),
    },
)


# ==================================================
# CASH FLOW CONSISTENCY
# ==================================================

st.divider()

st.subheader("Cash Flow Consistency")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Positive Months",
        positive_months,
    )


with col2:

    st.metric(
        "Negative Months",
        negative_months,
    )


with col3:

    st.metric(
        "Break-even Months",
        zero_months,
    )


# ==================================================
# FINANCIAL INSIGHTS
# ==================================================

st.divider()

st.subheader("Financial Insights")


if total_income <= 0:

    st.warning(
        "Add income transactions to get meaningful "
        "financial health insights."
    )

else:

    if savings_rate >= 30:

        st.success(
            "Your savings rate is strong. "
            "Continue maintaining your current savings habit."
        )

    elif savings_rate >= 20:

        st.info(
            "Your savings rate is good. "
            "You can gradually work toward a higher savings rate."
        )

    elif savings_rate >= 10:

        st.warning(
            "Your savings rate has room for improvement. "
            "Planning can help you control spending."
        )

    else:

        st.error(
            "Your savings rate is low. "
            "Review your expenses and create a structured budget."
        )


    if expense_ratio > 90:

        st.warning(
            "More than 90% of your income is currently "
            "being used for expenses."
        )


    if negative_months > 0:

        st.warning(
            f"You had {negative_months} month(s) where "
            "expenses exceeded income."
        )


    if positive_months == number_of_months:

        st.success(
            "Your cash flow was positive in every "
            "analysed month."
        )


    if (
        not goals_df.empty
        and
        total_goal_remaining > 0
        and
        average_monthly_savings <= 0
    ):

        st.error(
            "Your current average monthly savings are not "
            "positive enough to fund your active goals. "
            "Review spending or adjust goal timelines."
        )
