import streamlit as st
import pandas as pd

from utils.data import load_expenses


# =========================================================
# PAGE
# =========================================================

st.title("Financial Health")
st.caption("Understand your overall financial position")


# =========================================================
# LOAD DATA
# =========================================================

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


# =========================================================
# CLEAN DATA
# =========================================================

df = df.copy()

df = df.dropna(
    subset=["Date"]
)

df["Year"] = df["Date"].dt.year

df["Month Period"] = (
    df["Date"]
    .dt.to_period("M")
)


# =========================================================
# YEAR SELECTION
# =========================================================

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


# =========================================================
# BASIC FINANCIAL VALUES
# =========================================================

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


# =========================================================
# RATIOS
# =========================================================

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


# =========================================================
# MONTHLY ANALYSIS
# =========================================================

monthly_income = (
    year_df[
        year_df["Type"] == "Income"
    ]
    .groupby("Month Period")["Amount"]
    .sum()
)


monthly_expenses = (
    year_df[
        year_df["Type"] == "Expense"
    ]
    .groupby("Month Period")["Expense Amount"]
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


# =========================================================
# HEADER
# =========================================================

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


# =========================================================
# MONTHLY AVERAGES
# =========================================================

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


# =========================================================
# FINANCIAL STABILITY
# =========================================================

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


# =========================================================
# MONTHLY CASH FLOW
# =========================================================

st.divider()

st.subheader("Monthly Cash Flow")


monthly_display = monthly_analysis.reset_index()

monthly_display["Month"] = (
    monthly_display["Month Period"]
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


# =========================================================
# CASH FLOW CONSISTENCY
# =========================================================

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


# =========================================================
# FINANCIAL INSIGHTS
# =========================================================

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
            "More than 90% of your income is currently being "
            "used for expenses."
        )


    if negative_months > 0:

        st.warning(
            f"You had {negative_months} month(s) where "
            "expenses exceeded income."
        )


    if positive_months == number_of_months:

        st.success(
            "Your cash flow was positive in every analysed month."
        )
