import streamlit as st
import pandas as pd

from utils.data import load_expenses
from utils.sheets import get_google_sheet


st.title("📊 Planning")
st.caption("Plan your income, spending and savings")


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

try:

    df = load_expenses()
    expenses_worksheet = get_google_sheet()

except Exception as e:

    st.error("Unable to load planning data.")
    st.exception(e)
    st.stop()


# ---------------------------------------------------------
# Get or create Budget_Plans worksheet
# ---------------------------------------------------------

try:

    spreadsheet = expenses_worksheet.spreadsheet

    try:

        budget_worksheet = spreadsheet.worksheet(
            "Budget_Plans"
        )

    except Exception:

        budget_worksheet = spreadsheet.add_worksheet(
            title="Budget_Plans",
            rows=100,
            cols=10,
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
        "Unable to access the Budget_Plans worksheet."
    )
    st.exception(e)
    st.stop()


# ---------------------------------------------------------
# Basic data check
# ---------------------------------------------------------

if df.empty:

    st.info(
        "Add some transactions first to start planning your finances."
    )

    st.stop()


available_years = sorted(
    df["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist(),
    reverse=True,
)


if not available_years:

    st.warning("No transaction years available.")

    st.stop()


selected_year = st.selectbox(
    "Select Year",
    available_years,
)


year_df = df[
    df["Year"] == selected_year
].copy()


# ---------------------------------------------------------
# Current financial position
# ---------------------------------------------------------

total_income = year_df.loc[
    year_df["Type"] == "Income",
    "Amount",
].sum()


total_expenses = year_df.loc[
    year_df["Type"] == "Expense",
    "Expense Amount",
].sum()


current_savings = total_income - total_expenses


st.divider()

st.subheader("💰 Current Financial Position")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "💵 Income",
        f"₹{total_income:,.2f}",
    )


with col2:

    st.metric(
        "💸 Expenses",
        f"₹{total_expenses:,.2f}",
    )


with col3:

    st.metric(
        "💰 Savings",
        f"₹{current_savings:,.2f}",
    )


# ---------------------------------------------------------
# Load saved plan
# ---------------------------------------------------------

saved_plan = None

try:

    budget_records = budget_worksheet.get_all_records()

    for record in budget_records:

        try:

            record_year = int(
                float(record.get("Year", 0))
            )

        except (ValueError, TypeError):

            continue

        if record_year == selected_year:

            saved_plan = record
            break

except Exception as e:

    st.warning(
        "Unable to load saved planning settings."
    )


# ---------------------------------------------------------
# Default values
# ---------------------------------------------------------

if saved_plan:

    try:
        default_needs = float(
            saved_plan.get("Needs %", 50)
        )
    except (ValueError, TypeError):
        default_needs = 50

    try:
        default_investment = float(
            saved_plan.get("Investment %", 20)
        )
    except (ValueError, TypeError):
        default_investment = 20

    try:
        default_lifestyle = float(
            saved_plan.get("Lifestyle %", 30)
        )
    except (ValueError, TypeError):
        default_lifestyle = 30

    default_goal_name = str(
        saved_plan.get(
            "Goal Name",
            "Emergency Fund",
        )
    )

    try:
        default_goal_amount = float(
            saved_plan.get(
                "Goal Amount",
                0,
            )
        )
    except (ValueError, TypeError):
        default_goal_amount = 0

else:

    default_needs = 50
    default_investment = 20
    default_lifestyle = 30

    default_goal_name = "Emergency Fund"
    default_goal_amount = 0


# ---------------------------------------------------------
# Budget percentages
# ---------------------------------------------------------

st.divider()

st.subheader("📋 Budget Plan")

st.caption(
    "Set how you want to divide your income."
)


col1, col2, col3 = st.columns(3)


with col1:

    needs_percentage = st.number_input(
        "Needs %",
        min_value=0.0,
        max_value=100.0,
        value=float(default_needs),
        step=1.0,
    )


with col2:

    investment_percentage = st.number_input(
        "Investments %",
        min_value=0.0,
        max_value=100.0,
        value=float(default_investment),
        step=1.0,
    )


with col3:

    lifestyle_percentage = st.number_input(
        "Lifestyle %",
        min_value=0.0,
        max_value=100.0,
        value=float(default_lifestyle),
        step=1.0,
    )


total_percentage = (
    needs_percentage
    + investment_percentage
    + lifestyle_percentage
)


if abs(total_percentage - 100) < 0.01:

    st.success(
        "✅ Budget allocation is exactly 100%."
    )

else:

    st.warning(
        f"⚠️ Current allocation is "
        f"{total_percentage:.1f}%. "
        "It should equal 100%."
    )


# ---------------------------------------------------------
# Planned amounts
# ---------------------------------------------------------

st.subheader("💵 Planned Budget")


planned_needs = (
    total_income
    * needs_percentage
    / 100
)


planned_investment = (
    total_income
    * investment_percentage
    / 100
)


planned_lifestyle = (
    total_income
    * lifestyle_percentage
    / 100
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🏠 Needs",
        f"₹{planned_needs:,.2f}",
    )


with col2:

    st.metric(
        "📈 Investments",
        f"₹{planned_investment:,.2f}",
    )


with col3:

    st.metric(
        "🎉 Lifestyle",
        f"₹{planned_lifestyle:,.2f}",
    )


# ---------------------------------------------------------
# Actual spending by budget group
# ---------------------------------------------------------

st.divider()

st.subheader("📊 Actual vs Planned")


st.caption(
    "Actual values are estimated from your transaction categories."
)


def calculate_actual_by_keywords(
    transaction_df,
    keywords,
):

    if transaction_df.empty:

        return 0.0

    mask = (
        transaction_df["Category"]
        .fillna("")
        .astype(str)
        .str.lower()
        .apply(
            lambda category: any(
                keyword in category
                for keyword in keywords
            )
        )
    )

    return transaction_df.loc[
        mask & (transaction_df["Type"] == "Expense"),
        "Expense Amount",
    ].sum()


needs_keywords = [
    "food",
    "grocery",
    "groceries",
    "rent",
    "housing",
    "electric",
    "electricity",
    "water",
    "gas",
    "utility",
    "utilities",
    "medical",
    "health",
    "education",
    "school",
    "transport",
    "transportation",
    "fuel",
    "petrol",
    "diesel",
]


investment_keywords = [
    "investment",
    "investments",
    "sip",
    "mutual fund",
    "mutual funds",
    "stock",
    "stocks",
    "share",
    "shares",
    "ppf",
    "pf",
    "epf",
    "fd",
    "fixed deposit",
    "rd",
    "recurring deposit",
]


actual_needs = calculate_actual_by_keywords(
    year_df,
    needs_keywords,
)


actual_investment = calculate_actual_by_keywords(
    year_df,
    investment_keywords,
)


actual_lifestyle = max(
    total_expenses
    - actual_needs
    - actual_investment,
    0,
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
            actual_investment,
            actual_lifestyle,
        ],
    }
)


display_comparison = comparison_df.copy()

display_comparison["Planned"] = (
    display_comparison["Planned"]
    .apply(lambda x: f"₹{x:,.2f}")
)

display_comparison["Actual"] = (
    display_comparison["Actual"]
    .apply(lambda x: f"₹{x:,.2f}")
)


st.dataframe(
    display_comparison,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# Savings goal
# ---------------------------------------------------------

st.divider()

st.subheader("🎯 Savings Goal")


col1, col2 = st.columns(2)


with col1:

    goal_name = st.text_input(
        "Goal Name",
        value=default_goal_name,
        placeholder="Example: Emergency Fund",
    )


with col2:

    goal_amount = st.number_input(
        "Target Amount",
        min_value=0.0,
        value=float(default_goal_amount),
        step=1000.0,
        format="%.2f",
    )


current_saved_for_goal = max(
    current_savings,
    0,
)


st.metric(
    "💰 Current Available Savings",
    f"₹{current_saved_for_goal:,.2f}",
)


remaining_goal = max(
    goal_amount - current_saved_for_goal,
    0,
)


if goal_amount > 0:

    if remaining_goal <= 0:

        st.success(
            f"🎉 Your goal '{goal_name}' "
            "has been reached based on your current savings."
        )

        target_monthly_saving = 0

    else:

        target_months = st.number_input(
            "Target Timeline (Months)",
            min_value=1,
            max_value=600,
            value=12,
            step=1,
        )

        target_monthly_saving = (
            remaining_goal
            / target_months
        )

        st.metric(
            "🎯 Required Monthly Saving",
            f"₹{target_monthly_saving:,.2f}",
        )

else:

    target_monthly_saving = 0

    st.info(
        "Enter a target amount to calculate "
        "your required monthly saving."
    )


# ---------------------------------------------------------
# Save planning settings
# ---------------------------------------------------------

st.divider()

st.subheader("💾 Save Planning Settings")


if st.button(
    "💾 Save Planning Settings",
    type="primary",
    use_container_width=True,
):

    if abs(total_percentage - 100) > 0.01:

        st.error(
            "Please make sure Needs + Investments + Lifestyle "
            "equals exactly 100% before saving."
        )

    elif not goal_name.strip():

        st.error(
            "Please enter a savings goal name."
        )

    else:

        try:

            latest_records = (
                budget_worksheet.get_all_records()
            )

            existing_row_number = None

            for row_number, record in enumerate(
                latest_records,
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

                except (ValueError, TypeError):

                    continue

                if record_year == selected_year:

                    existing_row_number = row_number
                    break


            plan_row = [
                selected_year,
                needs_percentage,
                investment_percentage,
                lifestyle_percentage,
                goal_name.strip(),
                goal_amount,
            ]


            if existing_row_number:

                budget_worksheet.update(
                    f"A{existing_row_number}:F{existing_row_number}",
                    [plan_row],
                )

                st.success(
                    f"✅ Planning settings for "
                    f"{selected_year} updated successfully!"
                )

            else:

                budget_worksheet.append_row(
                    plan_row
                )

                st.success(
                    f"✅ Planning settings for "
                    f"{selected_year} saved successfully!"
                )


        except Exception as e:

            st.error(
                "Unable to save planning settings."
            )

            st.exception(e)
