import streamlit as st

from utils.data import load_expenses


st.set_page_config(
    page_title="Transactions",
    page_icon="💳",
    layout="wide",
)

st.title("💳 Transactions")
st.caption("Search and filter all your transactions")


# Load data
try:
    df = load_expenses()

except Exception as e:
    st.error("Unable to load transaction data.")
    st.exception(e)
    st.stop()


# -----------------------------
# Filters
# -----------------------------

st.subheader("🔎 Filters")

col1, col2, col3 = st.columns(3)

with col1:
    search_text = st.text_input(
        "Search",
        placeholder="Search description or person...",
    )

with col2:
    transaction_type = st.selectbox(
        "Type",
        ["All", "Income", "Expense"],
    )

with col3:
    categories = sorted(
        df["Category"].dropna().unique().tolist()
    )

    selected_category = st.selectbox(
        "Category",
        ["All"] + categories,
    )


# -----------------------------
# Apply filters
# -----------------------------

filtered_df = df.copy()


if search_text:

    search_mask = (
        filtered_df["Description"]
        .str.contains(
            search_text,
            case=False,
            na=False,
        )
        |
        filtered_df["Paid to or received from"]
        .str.contains(
            search_text,
            case=False,
            na=False,
        )
    )

    filtered_df = filtered_df[search_mask]


if transaction_type != "All":

    filtered_df = filtered_df[
        filtered_df["Type"] == transaction_type
    ]


if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


# -----------------------------
# Summary
# -----------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Transactions",
        len(filtered_df),
    )

with col2:
    income = filtered_df.loc[
        filtered_df["Type"] == "Income",
        "Amount",
    ].sum()

    st.metric(
        "Income",
        f"₹{income:,.2f}",
    )

with col3:
    expenses = filtered_df.loc[
        filtered_df["Type"] == "Expense",
        "Expense Amount",
    ].sum()

    st.metric(
        "Expenses",
        f"₹{expenses:,.2f}",
    )


# -----------------------------
# Transaction table
# -----------------------------

st.divider()

st.subheader("📋 Transaction List")


display_df = filtered_df.sort_values(
    "Date",
    ascending=False,
).copy()


display_df["Date"] = display_df["Date"].dt.strftime(
    "%d/%m/%Y"
)


st.dataframe(
    display_df[
        [
            "ID",
            "Date",
            "Description",
            "Category",
            "Amount",
            "Type",
            "Paid to or received from",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)