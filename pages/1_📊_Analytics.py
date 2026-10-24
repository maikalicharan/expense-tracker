import streamlit as st
import plotly.express as px

from utils.data import load_expenses


st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Expense Analytics")
st.caption("Analyze your income and spending over time")


# Load expense data
try:
    df = load_expenses()

except Exception as e:
    st.error("Unable to load expense data.")
    st.exception(e)
    st.stop()


# -----------------------------
# Filters
# -----------------------------

available_years = sorted(
    df["Year"].dropna().unique().astype(int),
    reverse=True,
)

col1, col2 = st.columns(2)

with col1:
    selected_year = st.selectbox(
        "Year",
        available_years,
    )

with col2:
    selected_month = st.selectbox(
        "Month",
        ["All Months"]
        + sorted(
            df.loc[
                df["Year"] == selected_year,
                "Month"
            ].dropna().unique()
        ),
    )


# -----------------------------
# Filter data
# -----------------------------

filtered_df = df[
    df["Year"] == selected_year
].copy()


if selected_month != "All Months":
    filtered_df = filtered_df[
        filtered_df["Month"] == selected_month
    ]


# -----------------------------
# Monthly summary
# -----------------------------

monthly = (
    filtered_df.groupby(["Month", "Type"])["Amount"]
    .sum()
    .reset_index()
)


# Make expenses positive
monthly.loc[
    monthly["Type"] == "Expense",
    "Amount"
] = monthly.loc[
    monthly["Type"] == "Expense",
    "Amount"
].abs()


# -----------------------------
# Chart
# -----------------------------

if monthly.empty:

    st.info("No transactions found for this selection.")

else:

    fig = px.line(
        monthly,
        x="Month",
        y="Amount",
        color="Type",
        markers=True,
        title="Income vs Expenses",
        labels={
            "Month": "Month",
            "Amount": "Amount (₹)",
            "Type": "Transaction Type",
        },
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (₹)",
        legend_title="",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
    # -----------------------------
# Category Analysis
# -----------------------------

st.divider()

st.subheader("🗂️ Spending by Category")


category_expenses = (
    filtered_df[filtered_df["Type"] == "Expense"]
    .groupby("Category")["Expense Amount"]
    .sum()
    .reset_index()
    .sort_values("Expense Amount", ascending=False)
)


if category_expenses.empty:

    st.info("No expense data found for this selection.")

else:

    col1, col2 = st.columns(2)

    with col1:

        fig_category = px.pie(
            category_expenses,
            names="Category",
            values="Expense Amount",
            hole=0.45,
            title="Expense Distribution by Category",
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True,
        )

    with col2:

        st.dataframe(
            category_expenses,
            use_container_width=True,
            hide_index=True,
        )