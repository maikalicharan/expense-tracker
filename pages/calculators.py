import streamlit as st


st.title("🧮 Financial Calculators")
st.caption("Calculate investments, savings and financial goals")


# -----------------------------
# Calculator Tabs
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 SIP",
        "🏦 PPF",
        "💰 FD / RD",
        "🎯 Retirement",
    ]
)


# =========================================================
# SIP CALCULATOR
# =========================================================

with tab1:

    st.subheader("📈 SIP Calculator")

    st.caption(
        "Estimate the future value of your monthly SIP investment."
    )

    col1, col2 = st.columns(2)

    with col1:

        monthly_sip = st.number_input(
            "Monthly Investment",
            min_value=0.0,
            value=5000.0,
            step=500.0,
            format="%.2f",
            key="sip_monthly",
        )

    with col2:

        sip_years = st.number_input(
            "Investment Period (Years)",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
            key="sip_years",
        )

    sip_return = st.number_input(
        "Expected Annual Return (%)",
        min_value=0.0,
        max_value=50.0,
        value=12.0,
        step=0.5,
        key="sip_return",
    )

    sip_months = sip_years * 12

    sip_monthly_rate = (
        sip_return / 100 / 12
    )

    if sip_monthly_rate == 0:

        sip_future_value = (
            monthly_sip * sip_months
        )

    else:

        sip_future_value = (
            monthly_sip
            * (
                (
                    (1 + sip_monthly_rate)
                    ** sip_months
                    - 1
                )
                / sip_monthly_rate
            )
            * (1 + sip_monthly_rate)
        )

    sip_invested = (
        monthly_sip * sip_months
    )

    sip_profit = (
        sip_future_value - sip_invested
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Invested",
            f"₹{sip_invested:,.2f}",
        )

    with col2:

        st.metric(
            "Estimated Returns",
            f"₹{sip_profit:,.2f}",
        )

    with col3:

        st.metric(
            "Future Value",
            f"₹{sip_future_value:,.2f}",
        )

    st.caption(
        "This is an estimate. Actual market returns may differ."
    )


# =========================================================
# PPF CALCULATOR
# =========================================================

with tab2:

    st.subheader("🏦 PPF Calculator")

    st.caption(
        "Estimate the maturity value of a PPF investment."
    )

    col1, col2 = st.columns(2)

    with col1:

        yearly_ppf = st.number_input(
            "Yearly Investment",
            min_value=0.0,
            value=50000.0,
            step=5000.0,
            format="%.2f",
            key="ppf_yearly",
        )

    with col2:

        ppf_years = st.number_input(
            "Investment Period (Years)",
            min_value=1,
            max_value=50,
            value=15,
            step=1,
            key="ppf_years",
        )

    ppf_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=7.1,
        step=0.1,
        key="ppf_rate",
    )

    ppf_rate_decimal = (
        ppf_rate / 100
    )

    ppf_value = 0.0

    for _ in range(ppf_years):

        ppf_value = (
            ppf_value
            + yearly_ppf
        ) * (
            1 + ppf_rate_decimal
        )

    ppf_invested = (
        yearly_ppf * ppf_years
    )

    ppf_interest = (
        ppf_value - ppf_invested
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Invested",
            f"₹{ppf_invested:,.2f}",
        )

    with col2:

        st.metric(
            "Estimated Interest",
            f"₹{ppf_interest:,.2f}",
        )

    with col3:

        st.metric(
            "Estimated Maturity",
            f"₹{ppf_value:,.2f}",
        )

    st.caption(
        "PPF interest rates can change. Use the current "
        "applicable rate when making real financial decisions."
    )


# =========================================================
# FD / RD CALCULATOR
# =========================================================

with tab3:

    st.subheader("💰 FD / RD Calculator")

    calculator_type = st.radio(
        "Choose Calculator",
        [
            "Fixed Deposit (FD)",
            "Recurring Deposit (RD)",
        ],
        horizontal=True,
    )


    if calculator_type == "Fixed Deposit (FD)":

        principal = st.number_input(
            "Principal Amount",
            min_value=0.0,
            value=100000.0,
            step=5000.0,
            format="%.2f",
            key="fd_principal",
        )

        fd_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=7.0,
            step=0.1,
            key="fd_rate",
        )

        fd_years = st.number_input(
            "Tenure (Years)",
            min_value=1,
            max_value=50,
            value=5,
            step=1,
            key="fd_years",
        )

        compounding_frequency = st.selectbox(
            "Compounding Frequency",
            [
                "Yearly",
                "Half-yearly",
                "Quarterly",
                "Monthly",
            ],
            key="fd_frequency",
        )

        frequency_map = {
            "Yearly": 1,
            "Half-yearly": 2,
            "Quarterly": 4,
            "Monthly": 12,
        }

        n = frequency_map[
            compounding_frequency
        ]

        fd_rate_decimal = (
            fd_rate / 100
        )

        fd_maturity = (
            principal
            * (
                1
                + fd_rate_decimal / n
            )
            ** (n * fd_years)
        )

        fd_interest = (
            fd_maturity - principal
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Principal",
                f"₹{principal:,.2f}",
            )

        with col2:

            st.metric(
                "Interest Earned",
                f"₹{fd_interest:,.2f}",
            )

        st.metric(
            "Maturity Amount",
            f"₹{fd_maturity:,.2f}",
        )


    else:

        monthly_rd = st.number_input(
            "Monthly Deposit",
            min_value=0.0,
            value=5000.0,
            step=500.0,
            format="%.2f",
            key="rd_monthly",
        )

        rd_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=7.0,
            step=0.1,
            key="rd_rate",
        )

        rd_years = st.number_input(
            "Tenure (Years)",
            min_value=1,
            max_value=50,
            value=5,
            step=1,
            key="rd_years",
        )

        rd_months = (
            rd_years * 12
        )

        rd_monthly_rate = (
            rd_rate / 100 / 12
        )

        if rd_monthly_rate == 0:

            rd_maturity = (
                monthly_rd * rd_months
            )

        else:

            rd_maturity = (
                monthly_rd
                * (
                    (
                        (1 + rd_monthly_rate)
                        ** rd_months
                        - 1
                    )
                    / rd_monthly_rate
                )
            )

        rd_invested = (
            monthly_rd * rd_months
        )

        rd_interest = (
            rd_maturity - rd_invested
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Deposited",
                f"₹{rd_invested:,.2f}",
            )

        with col2:

            st.metric(
                "Estimated Interest",
                f"₹{rd_interest:,.2f}",
            )

        with col3:

            st.metric(
                "Maturity Amount",
                f"₹{rd_maturity:,.2f}",
            )


# =========================================================
# RETIREMENT CALCULATOR
# =========================================================

with tab4:

    st.subheader("🎯 Retirement Calculator")

    st.caption(
        "Estimate how much you may need for retirement."
    )

    col1, col2 = st.columns(2)

    with col1:

        current_age = st.number_input(
            "Current Age",
            min_value=18,
            max_value=80,
            value=30,
            step=1,
            key="retirement_current_age",
        )

    with col2:

        retirement_age = st.number_input(
            "Retirement Age",
            min_value=19,
            max_value=100,
            value=60,
            step=1,
            key="retirement_age",
        )

    current_monthly_expenses = st.number_input(
        "Current Monthly Expenses",
        min_value=0.0,
        value=30000.0,
        step=1000.0,
        format="%.2f",
        key="retirement_expenses",
    )

    inflation_rate = st.number_input(
        "Expected Inflation (%)",
        min_value=0.0,
        max_value=20.0,
        value=6.0,
        step=0.5,
        key="retirement_inflation",
    )

    retirement_years = st.number_input(
        "Expected Retirement Years",
        min_value=1,
        max_value=60,
        value=25,
        step=1,
        key="retirement_duration",
    )

    expected_return = st.number_input(
        "Expected Investment Return (%)",
        min_value=0.0,
        max_value=30.0,
        value=10.0,
        step=0.5,
        key="retirement_return",
    )

    years_to_retirement = (
        retirement_age - current_age
    )


    if years_to_retirement <= 0:

        st.error(
            "Retirement age must be greater than current age."
        )

    else:

        future_monthly_expenses = (
            current_monthly_expenses
            * (
                1
                + inflation_rate / 100
            )
            ** years_to_retirement
        )

        annual_retirement_expenses = (
            future_monthly_expenses * 12
        )

        retirement_corpus = (
            annual_retirement_expenses
            * retirement_years
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Monthly Expenses at Retirement",
                f"₹{future_monthly_expenses:,.2f}",
            )

        with col2:

            st.metric(
                "Estimated Retirement Corpus",
                f"₹{retirement_corpus:,.2f}",
            )

        st.info(
            f"You have approximately "
            f"{years_to_retirement} years until retirement."
        )

        st.caption(
            "This is a simplified planning estimate. "
            "Actual retirement needs depend on inflation, "
            "returns, taxes, healthcare, lifestyle and other factors."
        )
