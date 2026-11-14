import streamlit as st
import pandas as pd

from utils.data import load_expenses


st.title("📊 Financial Planning")
st.caption("Plan your income, spending and savings")


# -----------------------------
# Load Data
# -----------------------------

try:
    df = load_expenses()

except Exception as e:
    st.error("Unable to load financial data.")
    st.exception(e)
    st.stop()


# -----------------------------
# Empty Data Check
# -----------------------------

if df.empty:

    st.info(
        "Add some income and expense transactions first "
        "to start financial planning."
    )

    st.stop()


# -----------------------------
# Year Selection
# -----------------------------

available_years = sorted(
    df["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist(),
    reverse=True,
)


selected_year = st.selectbox(
    "Select Year",
    available_years,
)


year_df = df[
    df["Year"] == selected_year
].copy()


# -----------------------------
# Income Calculation
# -----------------------------

total_income = (
    year_df.loc[
        year_df["Type"] == "Income",
        "Amount",
    ].sum()
)


total_expenses = (
    year_df.loc[
        year_df["Type"] == "Expense",
        "Expense Amount",
    ].sum()
)


current_savings = total_income - total_expenses


if total_income > 0:

    current_savings_percentage = (
        current_savings / total_income
    ) * 100

else:

    current_savings_percentage = 0


# -----------------------------
# Current Financial Position
# -----------------------------

st.subheader("💰 Current Financial Position")


col1, col2, col3 = st.columns(3)


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
        "Current Savings",
        f"₹{current_savings:,.2f}",
    )


st.divider()


# -----------------------------
# Budget Planning
# -----------------------------

st.subheader("🎯 Budget Planner")

st.caption(
    "Set your ideal allocation for income. "
    "The percentages below should add up to 100%."
)


col1, col2, col3 = st.columns(3)


with col1:

    needs_percentage = st.number_input(
        "Needs %",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0,
    )


with col2:

    investment_percentage = st.number_input(
        "Investment %",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
    )


with col3:

    lifestyle_percentage = st.number_input(
        "Lifestyle %",
        min_value=0.0,
        max_value=100.0,
        value=30.0,
        step=1.0,
    )


total_percentage = (
    needs_percentage
    + investment_percentage
    + lifestyle_percentage
)


if total_percentage != 100:

    st.warning(
        f"Your allocation currently totals "
        f"{total_percentage:.0f}%. "
        "Please make it exactly 100%."
    )


else:

    st.success(
        "Your budget allocation is correctly set to 100%. ✅"
    )


st.divider()


# -----------------------------
# Planned Amounts
# -----------------------------

st.subheader("💵 Planned Allocation")


planned_needs = (
    total_income
    * needs_percentage
    / 100
)


planned_investments = (
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
        "🏠 Planned Needs",
        f"₹{planned_needs:,.2f}",
    )


with col2:

    st.metric(
        "📈 Planned Investments",
        f"₹{planned_investments:,.2f}",
    )


with col3:

    st.metric(
        "🎉 Planned Lifestyle",
        f"₹{planned_lifestyle:,.2f}",
    )


st.divider()


# -----------------------------
# Actual vs Planned
# -----------------------------

st.subheader("📊 Actual vs Planned")


actual_needs = (
    year_df[
        (year_df["Type"] == "Expense")
        & (
            year_df["Category"]
            .astype(str)
            .str.lower()
            .str.contains(
                "need|rent|food|grocery|bill|utility|transport",
                na=False,
            )
        )
    ]["Expense Amount"].sum()
)


actual_lifestyle = (
    year_df[
        (year_df["Type"] == "Expense")
        & (
            year_df["Category"]
            .astype(str)
            .str.lower()
            .str.contains(
                "lifestyle|shopping|entertainment|travel|dining",
                na=False,
            )
        )
    ]["Expense Amount"].sum()
)


planning_df = pd.DataFrame(
    {
        "Category": [
            "Needs",
            "Investments",
            "Lifestyle",
        ],
        "Planned": [
            planned_needs,
            planned_investments,
            planned_lifestyle,
        ],
        "Actual": [
            actual_needs,
            0,
            actual_lifestyle,
        ],
    }
)


st.dataframe(
    planning_df,
    use_container_width=True,
    hide_index=True,
)


st.divider()


# -----------------------------
# Savings Goal
# -----------------------------

st.subheader("🎯 Savings Goal")


monthly_income = (
    total_income / 12
)


monthly_expenses = (
    total_expenses / 12
)


monthly_savings = (
    monthly_income - monthly_expenses
)


col1, col2 = st.columns(2)


with col1:

    savings_goal_percentage = st.number_input(
        "Target Savings %",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
    )


with col2:

    target_monthly_savings = (
        monthly_income
        * savings_goal_percentage
        / 100
    )

    st.metric(
        "Target Monthly Savings",
        f"₹{target_monthly_savings:,.2f}",
    )


if monthly_savings >= target_monthly_savings:

    st.success(
        "🎉 You are currently meeting your savings goal."
    )

else:

    difference = (
        target_monthly_savings
        - monthly_savings
    )

    st.warning(
        f"You need approximately "
        f"₹{difference:,.2f} more monthly savings "
        "to reach your target."
    )
