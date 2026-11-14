import streamlit as st


st.title("⚙️ Settings")
st.caption("Manage your app preferences")


# -----------------------------
# Appearance
# -----------------------------

st.subheader("🎨 Appearance")


theme = st.selectbox(
    "Preferred Theme",
    [
        "System Default",
        "Light",
        "Dark",
    ],
)


st.info(
    "Theme preference is currently for planning purposes. "
    "Full theme customization will be added later."
)


st.divider()


# -----------------------------
# Currency
# -----------------------------

st.subheader("💱 Currency")


currency = st.selectbox(
    "Default Currency",
    [
        "₹ Indian Rupee (INR)",
        "$ US Dollar (USD)",
        "€ Euro (EUR)",
        "£ British Pound (GBP)",
    ],
)


st.divider()


# -----------------------------
# Number Format
# -----------------------------

st.subheader("🔢 Number Format")


decimal_places = st.selectbox(
    "Decimal Places",
    [
        0,
        1,
        2,
    ],
    index=2,
)


st.divider()


# -----------------------------
# App Information
# -----------------------------

st.subheader("ℹ️ App Information")


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        **My Finance**

        Personal financial management tool.

        Current version: **Prototype v1**
        """
    )


with col2:

    st.markdown(
        """
        **Current Modules**

        - 🏠 Dashboard
        - 🧾 Account History
        - ➕ Add Transaction
        - 💳 Transactions
        - 📊 Financial Planning
        - 📈 Investments
        - 🧮 Financial Calculators
        """
    )


st.divider()


# -----------------------------
# Data Information
# -----------------------------

st.subheader("🗄️ Data")


st.info(
    "Your current transaction data is stored in your "
    "connected Google Sheet."
)


st.warning(
    "Before making major changes to your Google Sheet, "
    "keep a backup of your data."
)


st.divider()


# -----------------------------
# Future Features
# -----------------------------

st.subheader("🚀 Coming Soon")


st.markdown(
    """
    - 👤 User profile
    - 🔐 Login and authentication
    - 👨‍👩‍👧 Family accounts
    - 🔔 Budget notifications
    - ☁️ Cloud database
    - 📱 Mobile app
    - 🖥️ Desktop app
    - 🔒 Advanced security
    """
)
