import streamlit as st

from utils.ui import apply_custom_css


st.set_page_config(
    page_title="My Finance",
    layout="wide",
)

apply_custom_css()


dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
)

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
            investments,
            calculators,
        ],
        "System": [
            settings,
        ],
    }
)


with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size: 1.15rem;
            font-weight: 700;
            color: #20242d;
            margin-bottom: 0.25rem;
        ">
            My Finance
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Personal financial management"
    )


pg.run()
