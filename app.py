import streamlit as st


st.set_page_config(
    page_title="My Finance",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# PAGE NAVIGATION
# ============================================================

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠",
)

account_history = st.Page(
    "pages/account_history.py",
    title="Account History",
    icon="🧾",
)

add_transaction = st.Page(
    "pages/add_transaction.py",
    title="Add Transaction",
    icon="➕",
)

planning = st.Page(
    "pages/planning.py",
    title="Planning",
    icon="📊",
)

investments = st.Page(
    "pages/investments.py",
    title="Investments",
    icon="📈",
)

calculators = st.Page(
    "pages/calculators.py",
    title="Calculators",
    icon="🧮",
)

settings = st.Page(
    "pages/settings.py",
    title="Settings",
    icon="⚙️",
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

pg = st.navigation(
    {
        "Main": [
            dashboard,
        ],
        "Transactions": [
            account_history,
            add_transaction,
        ],
        "Financial Planning": [
            planning,
        ],
        "Investments": [
            investments,
        ],
        "Financial Tools": [
            calculators,
        ],
        "System": [
            settings,
        ],
    }
)


# ============================================================
# SIDEBAR BRANDING
# ============================================================

with st.sidebar:

    st.markdown("---")

    st.caption("💰 My Finance")

    st.caption(
        "Your personal financial management tool"
    )


# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()
