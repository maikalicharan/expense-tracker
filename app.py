import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import load_expenses
from utils.calculations import calculate_summary


st.set_page_config(
    page_title="Account History",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# LOAD DATA
# ============================================================

try:
    df = load_expenses()
    summary = calculate_summary(df)

except Exception as e:
    st.error("Unable to load account history.")
    st.exception(e)
    st.stop()


# ============================================================
# PAGE TITLE
# ============================================================

st.title("💰 Account History")


# ============================================================
# MONTH NAMES
# ============================================================

month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


# ============================================================
# AVAILABLE YEARS
# ============================================================

available_years = sorted(
    df["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist(),
    reverse=True,
)


if not available_years:
    st.warning("No transaction data available.")
    st.stop()


# ============================================================
# YEAR AND MONTH DROPDOWNS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    selected_year = st.selectbox(
        "Year",
        available_years,
        label_visibility="collapsed",
    )


with col2:

    year_df = df[
        df["Year"] == selected_year
    ].copy()

    available_month_values = sorted(
        year_df["Month"]
        .dropna()
        .unique()
        .tolist()
    )

    month_display = {
        f"{selected_year}-{month:02d}": month_names[month - 1]
        for month in range(1, 13)
    }

    available_month_names = [
        month_display[month]
        for month in available_month_values
        if month in month_display
    ]

    month_options = [
        "All Months"
    ] + available_month_names

    selected_month = st.selectbox(
        "Month",
        month_options,
        label_visibility="collapsed",
    )


# ============================================================
# FILTER BY SELECTED YEAR AND MONTH
# ============================================================

filtered_df = year_df.copy()


if selected_month != "All Months":

    selected_month_number = (
        month_names.index(selected_month) + 1
    )

    selected_month_value = (
        f"{selected_year}-{selected_month_number:02d}"
    )

    filtered_df = filtered_df[
        filtered_df["Month"] == selected_month_value
    ]


# ============================================================
# DYNAMIC SUBTITLE
# ============================================================

if selected_month == "All Months":

    st.caption(
        f"Account history for {selected_year}"
    )

else:

    st.caption(
        f"Account history for {selected_month} {selected_year}"
    )


st.divider()


# ============================================================
# TOTAL RECEIVED / TOTAL SPENT
# ============================================================

selected_income = (
    filtered_df.loc[
        filtered_df["Type"] == "Income",
        "Amount",
    ].sum()
)


selected_expenses = (
    filtered_df.loc[
        filtered_df["Type"] == "Expense",
        "Expense Amount",
    ].sum()
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "💵 Total Received",
        f"₹{selected_income:,.2f}",
    )


with col2:

    st.metric(
        "💸 Total Spent",
        f"₹{selected_expenses:,.2f}",
    )


st.divider()


# ============================================================
# CATEGORY DROPDOWN
# ============================================================

available_categories = sorted(
    filtered_df["Category"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)


category_options = [
    "📂 All Categories"
] + available_categories


selected_category_display = st.selectbox(
    "Category",
    category_options,
    label_visibility="collapsed",
)


if selected_category_display == "📂 All Categories":

    selected_category = "All Categories"

else:

    selected_category = selected_category_display


# ============================================================
# CATEGORY FILTER
# ============================================================

category_transactions = filtered_df.copy()


if selected_category != "All Categories":

    category_transactions = category_transactions[
        category_transactions["Category"].astype(str).str.strip()
        == selected_category
    ]


# ============================================================
# TRANSACTIONS
# ============================================================

st.subheader("🧾 Transactions")


if selected_category == "All Categories":

    st.caption(
        "Showing transactions for the selected year and month."
    )

else:

    st.caption(
        f"Showing transactions for: **{selected_category}**"
    )


if category_transactions.empty:

    st.info(
        "No transactions found for this selection."
    )

else:

    transaction_columns = [
        "Date",
        "Description",
        "Category",
        "Amount",
        "Type",
        "Paid to or received from",
    ]

    display_df = category_transactions[
        transaction_columns
    ].copy()

    display_df["Date"] = display_df["Date"].dt.strftime(
        "%d/%m/%Y"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# ============================================================
# YEARLY MONTHLY SPENDING GRAPH
# ============================================================

st.subheader(
    f"📊 Monthly Spending — {selected_year}"
)


# Create all 12 months for the selected year.
# This ensures months with zero spending are also displayed.

all_month_values = [
    f"{selected_year}-{month:02d}"
    for month in range(1, 13)
]


yearly_spending = (
    year_df[
        year_df["Type"] == "Expense"
    ]
    .groupby("Month")["Expense Amount"]
    .sum()
    .reindex(
        all_month_values,
        fill_value=0,
    )
    .reset_index()
)


yearly_spending.columns = [
    "Month",
    "Spent",
]


yearly_spending["Month"] = yearly_spending[
    "Month"
].map(month_display)


yearly_spending["Month"] = pd.Categorical(
    yearly_spending["Month"],
    categories=month_names,
    ordered=True,
)


yearly_spending = yearly_spending.sort_values(
    "Month"
)


# ============================================================
# SPENDING CHART
# ============================================================

spending_chart = px.bar(
    yearly_spending,
    x="Month",
    y="Spent",
    text="Spent",
)


spending_chart.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b>"
        "<br>Spent: ₹%{y:,.2f}"
        "<extra></extra>"
    ),
)


spending_chart.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Spent (₹)",
    showlegend=False,
)


st.plotly_chart(
    spending_chart,
    use_container_width=True,
)
