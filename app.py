import streamlit as st

from utils.ui import apply_custom_css


st.set_page_config(
    page_title="My Finance",
    layout="wide",
)

apply_custom_css()


# Main
dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
)


# Transactions
account_history = st.Page(
    "pages/account_history.py",
    title="Account History",
)

add_transaction = st.Page(
    "pages/add_transaction.py",
    title="Add Transaction",
)

transactions = st.Page(
    "pages/transactions.py",
    title="Transactions",
)


# Planning
planning = st.Page(
    "pages/planning.py",
    title="Planning",
)

financial_health = st.Page(
    "pages/financial_health.py",
    title="Financial Health",
)

investments = st.Page(
    "pages/investments.py",
    title="Investments",
)

calculators = st.Page(
    "pages/calculators.py",
    title="Calculators",
)


# System
settings = st.Page(
    "pages/settings.py",
    title="Settings",
)


pg = st.navigation(
    {
        "Main": [
            dashboard,
        ],

        "Transactions": [
            account_history,
            add_transaction,
            transactions,
        ],

        "Planning": [
            planning,
            financial_health,
            investments,
            calculators,
        ],

        "System": [
            settings,
        ],
    }
)


with st.sidebar:
    st.markdown("### My Finance")
    st.caption("Personal financial management")


pg.run()
