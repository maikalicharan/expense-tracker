import streamlit as st


st.title("📈 Investments")
st.caption("Plan your investments and understand your allocation")


# -----------------------------
# Investment Goal
# -----------------------------

st.subheader("🎯 Investment Goal")


col1, col2 = st.columns(2)


with col1:

    monthly_income = st.number_input(
        "Monthly Income",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
    )


with col2:

    monthly_expenses = st.number_input(
        "Monthly Expenses",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
    )


monthly_surplus = (
    monthly_income - monthly_expenses
)


if monthly_surplus < 0:

    st.error(
        "Your monthly expenses are higher than your income."
    )

else:

    st.metric(
        "Monthly Surplus",
        f"₹{monthly_surplus:,.2f}",
    )


st.divider()


# -----------------------------
# Investment Allocation
# -----------------------------

st.subheader("📊 Investment Allocation")


investment_percentage = st.slider(
    "What percentage of your monthly surplus "
    "would you like to invest?",
    min_value=0,
    max_value=100,
    value=30,
    step=5,
)


monthly_investment = (
    monthly_surplus
    * investment_percentage
    / 100
)


monthly_savings = (
    monthly_surplus
    - monthly_investment
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "📈 Monthly Investment",
        f"₹{monthly_investment:,.2f}",
    )


with col2:

    st.metric(
        "💰 Remaining Savings",
        f"₹{monthly_savings:,.2f}",
    )


st.divider()


# -----------------------------
# Investment Categories
# -----------------------------

st.subheader("🧮 Investment Planning")


st.caption(
    "Use these categories to plan how you want to distribute "
    "your investment amount."
)


col1, col2, col3 = st.columns(3)


with col1:

    long_term_percentage = st.number_input(
        "Long-term %",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=5.0,
    )


with col2:

    retirement_percentage = st.number_input(
        "Retirement %",
        min_value=0.0,
        max_value=100.0,
        value=25.0,
        step=5.0,
    )


with col3:

    short_term_percentage = st.number_input(
        "Short-term %",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=5.0,
    )


total_allocation = (
    long_term_percentage
    + retirement_percentage
    + short_term_percentage
)


if total_allocation != 100:

    st.warning(
        f"Investment allocation currently totals "
        f"{total_allocation:.0f}%. "
        "Please make it exactly 100%."
    )

else:

    st.success(
        "Investment allocation is correctly set to 100%. ✅"
    )


# -----------------------------
# Planned Investment Amounts
# -----------------------------

long_term_amount = (
    monthly_investment
    * long_term_percentage
    / 100
)


retirement_amount = (
    monthly_investment
    * retirement_percentage
    / 100
)


short_term_amount = (
    monthly_investment
    * short_term_percentage
    / 100
)


st.subheader("💵 Planned Monthly Investment")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🌱 Long-term",
        f"₹{long_term_amount:,.2f}",
    )


with col2:

    st.metric(
        "🏖️ Retirement",
        f"₹{retirement_amount:,.2f}",
    )


with col3:

    st.metric(
        "🎯 Short-term",
        f"₹{short_term_amount:,.2f}",
    )


st.divider()


# -----------------------------
# Investment Projection
# -----------------------------

st.subheader("📈 Simple Investment Projection")


investment_years = st.number_input(
    "Investment Period (Years)",
    min_value=1,
    max_value=50,
    value=10,
    step=1,
)


expected_return = st.number_input(
    "Expected Annual Return (%)",
    min_value=0.0,
    max_value=50.0,
    value=10.0,
    step=0.5,
)


months = investment_years * 12


monthly_rate = (
    expected_return / 100 / 12
)


if monthly_rate == 0:

    projected_value = (
        monthly_investment * months
    )

else:

    projected_value = (
        monthly_investment
        * (
            (
                (1 + monthly_rate) ** months
                - 1
            )
            / monthly_rate
        )
    )


total_invested = (
    monthly_investment * months
)


estimated_growth = (
    projected_value - total_invested
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "💰 Total Invested",
        f"₹{total_invested:,.2f}",
    )


with col2:

    st.metric(
        "📈 Estimated Growth",
        f"₹{estimated_growth:,.2f}",
    )


with col3:

    st.metric(
        "🏆 Projected Value",
        f"₹{projected_value:,.2f}",
    )


st.caption(
    "Projection is an estimate based on the assumptions you enter. "
    "Actual investment returns can be different."
)


st.divider()


# -----------------------------
# Future Investment Tools
# -----------------------------

st.subheader("🛠️ Investment Tools")


st.info(
    "More investment tools are planned here, including "
    "SIP, PPF, EPF/PF, FD/RD, retirement planning and "
    "goal-based investment calculations."
)
