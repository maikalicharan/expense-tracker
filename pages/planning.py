import streamlit as st
import pandas as pd
from datetime import date

from utils.data import load_expenses
from utils.sheets import get_google_sheet


st.set_page_config(
    page_title="Planning",
    layout="wide",
)


st.title("Planning")
st.caption(
    "Plan your spending, savings and financial goals"
)


# ==================================================
# LOAD DATA
# ==================================================

try:

    df = load_expenses()
    worksheet = get_google_sheet()
    spreadsheet = worksheet.spreadsheet

except Exception as e:

    st.error(
        "Unable to load financial planning data."
    )

    st.exception(e)

    st.stop()


if df.empty:

    st.info(
        "Add some income and expense transactions "
        "before creating a financial plan."
    )

    st.stop()


df = df.copy()

df = df.dropna(
    subset=["Date"]
)


df["Year"] = (
    df["Date"]
    .dt.year
)


df["Month Period"] = (
    df["Date"]
    .dt.to_period("M")
)


# ==================================================
# GET OR CREATE BUDGET SHEET
# ==================================================

try:

    try:

        budget_worksheet = spreadsheet.worksheet(
            "Budget_Plans"
        )

    except Exception:

        budget_worksheet = spreadsheet.add_worksheet(
            title="Budget_Plans",
            rows=1000,
            cols=6,
        )

        budget_worksheet.append_row(
            [
                "Year",
                "Needs %",
                "Investment %",
                "Lifestyle %",
                "Goal Name",
                "Goal Amount",
            ]
        )

except Exception as e:

    st.error(
        "Unable to prepare Budget_Plans worksheet."
    )

    st.exception(e)

    st.stop()


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
    "Planning Year",
    available_years,
)


year_df = df[
    df["Year"] == selected_year
].copy()


# ==================================================
# LOAD SAVED PLAN
# ==================================================

try:

    budget_records = (
        budget_worksheet.get_all_records()
    )

except Exception as e:

    st.error(
        "Unable to load saved planning settings."
    )

    st.exception(e)

    st.stop()


saved_plan = None


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
# DEFAULT / SAVED VALUES
# ==================================================

if saved_plan:

    default_needs = float(
        saved_plan.get(
            "Needs %",
            50,
        )
        or 50
    )

    default_investment = float(
        saved_plan.get(
            "Investment %",
            20,
        )
        or 20
    )

    default_lifestyle = float(
        saved_plan.get(
            "Lifestyle %",
            30,
        )
        or 30
    )

    default_goal_name = str(
        saved_plan.get(
            "Goal Name",
            "",
        )
        or ""
    )

    default_goal_amount = float(
        saved_plan.get(
            "Goal Amount",
            0,
        )
        or 0
    )

else:

    default_needs = 50.0
    default_investment = 20.0
    default_lifestyle = 30.0

    default_goal_name = ""
    default_goal_amount = 0.0


# ==================================================
# ACTUAL FINANCIAL POSITION
# ==================================================

total_income = year_df.loc[
    year_df["Type"] == "Income",
    "Amount",
].sum()


total_expenses = year_df.loc[
    year_df["Type"] == "Expense",
    "Expense Amount",
].sum()


actual_savings = (
    total_income
    - total_expenses
)


# ==================================================
# PLANNING SETTINGS
# ==================================================

st.divider()

st.subheader(
    "Budget Allocation"
)


st.caption(
    "Set how you want to divide your income "
    "between Needs, Investments and Lifestyle."
)


col1, col2, col3 = st.columns(3)


with col1:

    needs_percent = st.number_input(
        "Needs %",
        min_value=0.0,
        max_value=100.0,
        value=default_needs,
        step=1.0,
    )


with col2:

    investment_percent = st.number_input(
        "Investment %",
        min_value=0.0,
        max_value=100.0,
        value=default_investment,
        step=1.0,
    )


with col3:

    lifestyle_percent = st.number_input(
        "Lifestyle %",
        min_value=0.0,
        max_value=100.0,
        value=default_lifestyle,
        step=1.0,
    )


total_percentage = (
    needs_percent
    + investment_percent
    + lifestyle_percent
)


if total_percentage != 100:

    st.warning(
        f"Your allocation currently totals "
        f"{total_percentage:.1f}%. "
        "It should total 100%."
    )


# ==================================================
# PLANNED RUPEE ALLOCATION
# ==================================================

st.divider()

st.subheader(
    "Planned Budget"
)


planned_needs = (
    total_income
    * needs_percent
    / 100
)


planned_investment = (
    total_income
    * investment_percent
    / 100
)


planned_lifestyle = (
    total_income
    * lifestyle_percent
    / 100
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Planned Needs",
        f"₹{planned_needs:,.2f}",
    )


with col2:

    st.metric(
        "Planned Investments",
        f"₹{planned_investment:,.2f}",
    )


with col3:

    st.metric(
        "Planned Lifestyle",
        f"₹{planned_lifestyle:,.2f}",
    )


# ==================================================
# CATEGORY CLASSIFICATION
# ==================================================

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


# ==================================================
# ACTUAL PLANNING BUCKETS
# ==================================================

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

else:

    expense_df["Planning Bucket"] = []


actual_needs = expense_df.loc[
    expense_df["Planning Bucket"]
    == "Needs",
    "Expense Amount",
].sum()


actual_investments = expense_df.loc[
    expense_df["Planning Bucket"]
    == "Investment",
    "Expense Amount",
].sum()


actual_lifestyle = expense_df.loc[
    expense_df["Planning Bucket"]
    == "Lifestyle",
    "Expense Amount",
].sum()


# ==================================================
# ACTUAL VS PLANNED
# ==================================================

st.divider()

st.subheader(
    "Actual vs Planned"
)


comparison_df = pd.DataFrame(
    {
        "Category": [
            "Needs",
            "Investments",
            "Lifestyle",
        ],
        "Planned": [
            planned_needs,
            planned_investment,
            planned_lifestyle,
        ],
        "Actual": [
            actual_needs,
            actual_investments,
            actual_lifestyle,
        ],
    }
)


comparison_df["Difference"] = (
    comparison_df["Planned"]
    - comparison_df["Actual"]
)


st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Category": "Category",

        "Planned": st.column_config.NumberColumn(
            "Planned",
            format="₹%.2f",
        ),

        "Actual": st.column_config.NumberColumn(
            "Actual",
            format="₹%.2f",
        ),

        "Difference": st.column_config.NumberColumn(
            "Remaining",
            format="₹%.2f",
        ),
    },
)


# ==================================================
# BUDGET STATUS
# ==================================================

st.subheader(
    "Budget Status"
)


budget_items = [
    (
        "Needs",
        planned_needs,
        actual_needs,
    ),
    (
        "Investments",
        planned_investment,
        actual_investments,
    ),
    (
        "Lifestyle",
        planned_lifestyle,
        actual_lifestyle,
    ),
]


for name, planned, actual in budget_items:

    difference = (
        planned
        - actual
    )


    if difference >= 0:

        st.success(
            f"{name}: ₹{difference:,.2f} "
            "remaining in planned allocation."
        )

    else:

        st.warning(
            f"{name}: ₹{abs(difference):,.2f} "
            "over planned allocation."
        )


# ==================================================
# SAVINGS POSITION
# ==================================================

st.divider()

st.subheader(
    "Savings Position"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Actual Income",
        f"₹{total_income:,.2f}",
    )


with col2:

    st.metric(
        "Actual Expenses",
        f"₹{total_expenses:,.2f}",
    )


with col3:

    st.metric(
        "Actual Savings",
        f"₹{actual_savings:,.2f}",
    )


# ==================================================
# GOAL PLANNING
# ==================================================

st.divider()

st.subheader(
    "Savings Goal"
)


goal_name = st.text_input(
    "Goal Name",
    value=default_goal_name,
    placeholder="Example: Emergency Fund",
)


goal_amount = st.number_input(
    "Goal Amount",
    min_value=0.0,
    value=default_goal_amount,
    step=1000.0,
    format="%.2f",
)


goal_target_date = st.date_input(
    "Goal Target Date",
    value=date.today(),
)


# ==================================================
# GOAL CALCULATION
# ==================================================

required_monthly_saving = 0.0


if goal_amount > 0:

    today = pd.Timestamp.today().normalize()

    target_timestamp = pd.Timestamp(
        goal_target_date
    )


    months_remaining = (
        (
            target_timestamp.year
            - today.year
        )
        * 12
        +
        (
            target_timestamp.month
            - today.month
        )
    )


    if months_remaining <= 0:

        months_remaining = 1


    required_monthly_saving = (
        goal_amount
        / months_remaining
    )


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Goal Amount",
        f"₹{goal_amount:,.2f}",
    )


with col2:

    st.metric(
        "Required Monthly Saving",
        f"₹{required_monthly_saving:,.2f}",
    )


# ==================================================
# GOAL FUNDING CAPACITY
# ==================================================

if goal_amount > 0:

    average_monthly_savings = (
        year_df
        .assign(
            MonthPeriod=
            year_df["Date"].dt.to_period("M")
        )
        .groupby("MonthPeriod")
        .apply(
            lambda group:
            group.loc[
                group["Type"] == "Income",
                "Amount",
            ].sum()
            -
            group.loc[
                group["Type"] == "Expense",
                "Expense Amount",
            ].sum(),
            include_groups=False,
        )
    )


    if not average_monthly_savings.empty:

        average_monthly_saving = (
            average_monthly_savings.mean()
        )

    else:

        average_monthly_saving = 0.0


    st.metric(
        "Average Monthly Saving",
        f"₹{average_monthly_saving:,.2f}",
    )


    if (
        average_monthly_saving
        >= required_monthly_saving
    ):

        st.success(
            "Your current average monthly savings "
            "are sufficient for this goal timeline."
        )

    else:

        shortfall = (
            required_monthly_saving
            - average_monthly_saving
        )


        st.warning(
            f"You need approximately "
            f"₹{shortfall:,.2f} more monthly savings "
            "to meet this goal timeline."
        )


# ==================================================
# SAVE PLANNING
# ==================================================

st.divider()

st.subheader(
    "Save Planning"
)


if st.button(
    "Save / Update Planning",
    type="primary",
    use_container_width=True,
):

    if abs(
        total_percentage - 100
    ) > 0.001:

        st.error(
            "Needs, Investment and Lifestyle "
            "percentages must total exactly 100%."
        )

        st.stop()


    if goal_amount < 0:

        st.error(
            "Goal amount cannot be negative."
        )

        st.stop()


    try:

        records = (
            budget_worksheet
            .get_all_records()
        )


        existing_row_number = None


        for row_number, record in enumerate(
            records,
            start=2,
        ):

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

                existing_row_number = (
                    row_number
                )

                break


        row_values = [
            selected_year,
            float(needs_percent),
            float(investment_percent),
            float(lifestyle_percent),
            goal_name.strip(),
            float(goal_amount),
        ]


        if existing_row_number is None:

            budget_worksheet.append_row(
                row_values
            )

            st.success(
                f"Planning for {selected_year} "
                "saved successfully!"
            )

        else:

            budget_worksheet.update(
                f"A{existing_row_number}:F{existing_row_number}",
                [row_values],
            )

            st.success(
                f"Planning for {selected_year} "
                "updated successfully!"
            )


        st.rerun()


    except Exception as e:

        st.error(
            "Unable to save planning settings."
        )

        st.exception(e)


# ==================================================
# PLANNING INSIGHTS
# ==================================================

st.divider()

st.subheader(
    "Planning Insights"
)


if total_income <= 0:

    st.warning(
        "Add income transactions to create a "
        "meaningful financial plan."
    )

else:

    if actual_savings > 0:

        st.success(
            f"You currently have "
            f"₹{actual_savings:,.2f} of net savings "
            f"for {selected_year}."
        )

    else:

        st.warning(
            "Your current expenses are equal to or "
            "higher than your income."
        )


    if actual_lifestyle > planned_lifestyle:

        st.warning(
            "Lifestyle spending is currently above "
            "your planned allocation."
        )


    if actual_needs > planned_needs:

        st.warning(
            "Needs spending is currently above "
            "your planned allocation."
        )


    if actual_investments < planned_investment:

        st.info(
            "Your actual investment-related spending "
            "is below your planned investment allocation."
        )


    if (
        goal_amount > 0
        and
        required_monthly_saving > 0
    ):

        if (
            average_monthly_saving
            >= required_monthly_saving
        ):

            st.success(
                "Your current savings pattern supports "
                "your planned goal timeline."
            )

        else:

            st.warning(
                "Your current savings pattern may require "
                "higher monthly savings or a longer goal timeline."
            )
