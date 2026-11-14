import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import load_expenses
from utils.calculations import calculate_summary


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
)


st.title("💰 Expense Tracker")
st.caption("Your personal finance dashboard")


# Load data from Google Sheets
try:
    df = load_expenses()
    summary = calculate_summary(df)

except Exception as e:
    st.error("Unable to load expense data.")
    st.exception(e)
    st.stop()


# Summary values
total_income = summary["total_income"]
total_expenses = summary["total_expenses"]
balance = summary["balance"]
savings_percentage = summary["savings_percentage"]


# Dashboard cards
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "💵 Total Income",
        f"₹{total_income:,.2f}",
    )

with col2:
    st.metric(
        "💸 Total Expenses",
        f"₹{total_expenses:,.2f}",
    )


col3, col4 = st.columns(2)

with col3:
    st.metric(
        "💰 Balance",
        f"₹{balance:,.2f}",
    )

with col4:
    st.metric(
        "📊 Savings",
        f"{savings_percentage:,.2f}%",
    )

st.divider()

# Dashboard year filter
available_years = sorted(
    df["Year"].dropna().astype(int).unique().tolist(),
    reverse=True,
)

selected_year = st.selectbox(
    "📅 Year",
    available_years,
)

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

# Monthly income and expense data

year_df = df[df["Year"] == selected_year]
filtered_df = year_df.copy()

available_months = sorted(
    filtered_df["Month"].dropna().unique().tolist()
)

month_display = {
    f"{selected_year}-{month:02d}": month_names[month - 1]
    for month in range(1, 13)
}

month_options = [
    month_display[month]
    for month in available_months
]

selected_month = st.selectbox(
    "📅 Month",
    ["All Months"] + month_options,
)

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


# 12-month breakdown for selected year
yearly_monthly_data = (
    year_df.groupby(["Month", "Type"])["Amount"]
    .sum()
    .reset_index()
)

yearly_monthly_data["Amount"] = yearly_monthly_data.apply(
    lambda row: (
        abs(row["Amount"])
        if row["Type"] == "Expense"
        else row["Amount"]
    ),
    axis=1,
)
    
monthly_data = (
    filtered_df.groupby(["Month", "Type"])["Amount"]
    .sum()
    .reset_index()
)

monthly_data["Amount"] = monthly_data.apply(
    lambda row: (
        abs(row["Amount"])
        if row["Type"] == "Expense"
        else row["Amount"]
    ),
    axis=1,
)

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

all_months = [
    f"{selected_year}-{month:02d}"
    for month in range(1, 13)
]

monthly_summary = (
    yearly_monthly_data
    .pivot(
        index="Month",
        columns="Type",
        values="Amount",
    )
    .reindex(all_months)
    .fillna(0)
    .reset_index()
)

month_display = {
    f"{selected_year}-{month:02d}": month_names[month - 1]
    for month in range(1, 13)
}

monthly_summary["Month"] = monthly_summary["Month"].map(
    month_display
)

if "Income" not in monthly_summary.columns:
    monthly_summary["Income"] = 0

if "Expense" not in monthly_summary.columns:
    monthly_summary["Expense"] = 0

monthly_summary["Net Balance"] = (
    monthly_summary["Income"]
    - monthly_summary["Expense"]
)

monthly_summary = monthly_summary[
    [
        "Month",
        "Income",
        "Expense",
        "Net Balance",
    ]
]

year_total_income = monthly_summary["Income"].sum()
year_total_expense = monthly_summary["Expense"].sum()
year_net_balance = monthly_summary["Net Balance"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 Year Income",
        f"₹{year_total_income:,.2f}",
    )

with col2:
    st.metric(
        "💸 Year Expenses",
        f"₹{year_total_expense:,.2f}",
    )

with col3:
    st.metric(
        "💰 Year Net Balance",
        f"₹{year_net_balance:,.2f}",
    )

monthly_order = month_names

monthly_summary["Month"] = pd.Categorical(
    monthly_summary["Month"],
    categories=monthly_order,
    ordered=True,
)

monthly_summary = monthly_summary.sort_values("Month")

st.dataframe(
    monthly_summary,
    use_container_width=True,
    hide_index=True,
)

st.subheader("📈 Monthly Income vs Expenses")

# Category-wise expense data
category_expenses = (
    filtered_df[filtered_df["Type"] == "Expense"]
    .groupby("Category")["Expense Amount"]
    .sum()
    .reset_index()
)

monthly_chart = px.line(
    monthly_data,
    x="Month",
    y="Amount",
    color="Type",
    markers=True,
)

monthly_chart.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount (₹)",
    legend_title="",
)

st.plotly_chart(
    monthly_chart,
    use_container_width=True,
)

st.subheader("📂 Category Breakdown")

category_breakdown = (
    filtered_df
    .groupby("Category")
    .agg(
        Spent=("Expense Amount", "sum"),
        Earned=("Amount", lambda x: x[x > 0].sum()),
    )
    .reset_index()
)

category_breakdown["Net"] = (
    category_breakdown["Earned"]
    - category_breakdown["Spent"]
)

category_breakdown = category_breakdown[
    [
        "Category",
        "Earned",
        "Spent",
        "Net",
    ]
]
)

st.dataframe(
    category_breakdown,
    use_container_width=True,
    hide_index=True,
)

available_categories = sorted(
    filtered_df["Category"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_category = st.selectbox(
    "📂 Category",
    ["All Categories"] + available_categories,
)

category_transactions = filtered_df.copy()

if selected_category != "All Categories":
    category_transactions = category_transactions[
        category_transactions["Category"] == selected_category
    ]

st.subheader("🧾 Transactions")

if category_transactions.empty:
    st.info("No transactions found for this selection.")

else:
    st.dataframe(
        category_transactions[
            [
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


st.subheader("🍕 Expenses by Category")

category_total = category_expenses["Expense Amount"].sum()

st.metric(
    "💸 Total Expenses for Selection",
    f"₹{category_total:,.2f}",
)

category_chart = px.pie(
    category_expenses,
    names="Category",
    values="Expense Amount",
    hole=0.4,
)

category_chart.update_traces(
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<extra></extra>",
)

category_chart.update_layout(
    legend_title="Category",
)

st.plotly_chart(
    category_chart,
    use_container_width=True,
)

st.divider()

st.subheader("Recent Transactions")

# Show the latest 10 transactions
recent_transactions = df.sort_values(
    "Date",
    ascending=False,
).head(10)

st.dataframe(
    recent_transactions[
        [
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
