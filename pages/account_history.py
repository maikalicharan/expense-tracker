import streamlit as st
import pandas as pd

from utils.data import load_expenses


st.set_page_config(
    page_title="Account History",
    layout="wide",
)


st.title("Account History")
st.caption("View your income and spending history")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    df = load_expenses()

except Exception as e:

    st.error("Unable to load account history.")
    st.exception(e)
    st.stop()


if df.empty:

    st.info(
        "No transactions available yet. "
        "Add your first transaction from Add Transaction."
    )

    st.stop()


# --------------------------------------------------
# PREPARE DATA
# --------------------------------------------------

df = df.copy()

df = df.dropna(
    subset=["Date"]
)

df["Year"] = (
    df["Date"]
    .dt.year
)

df["Month"] = (
    df["Date"]
    .dt.month
)

df["Month Name"] = (
    df["Date"]
    .dt.strftime("%B")
)


# --------------------------------------------------
# YEAR FILTER
# --------------------------------------------------

available_years = sorted(
    df["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist(),
    reverse=True,
)


selected_year = st.selectbox(
    "Year",
    available_years,
)


year_df = df[
    df["Year"] == selected_year
].copy()


if year_df.empty:

    st.info(
        "No transactions found for the selected year."
    )

    st.stop()


# --------------------------------------------------
# MONTH FILTER
# --------------------------------------------------

month_names = [
    "All Months",
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


selected_month = st.selectbox(
    "Month",
    month_names,
)


if selected_month != "All Months":

    selected_month_number = (
        month_names.index(
            selected_month
        )
    )

    filtered_df = year_df[
        year_df["Month"]
        == selected_month_number
    ].copy()

else:

    filtered_df = year_df.copy()


# --------------------------------------------------
# PAGE DESCRIPTION
# --------------------------------------------------

if selected_month == "All Months":

    st.caption(
        f"Account activity for {selected_year}"
    )

else:

    st.caption(
        f"Account activity for "
        f"{selected_month} {selected_year}"
    )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

total_received = filtered_df.loc[
    filtered_df["Type"] == "Income",
    "Amount",
].sum()


total_spent = filtered_df.loc[
    filtered_df["Type"] == "Expense",
    "Expense Amount",
].sum()


net_balance = (
    total_received
    - total_spent
)


st.divider()

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Received",
        f"₹{total_received:,.2f}",
    )


with col2:

    st.metric(
        "Total Spent",
        f"₹{total_spent:,.2f}",
    )


with col3:

    st.metric(
        "Net Balance",
        f"₹{net_balance:,.2f}",
    )


# --------------------------------------------------
# CATEGORY FILTER
# --------------------------------------------------

st.divider()

st.subheader("Transactions")


available_categories = sorted(
    filtered_df["Category"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


selected_category = st.selectbox(
    "Category",
    ["All Categories"] + available_categories,
)


category_df = filtered_df.copy()


if selected_category != "All Categories":

    category_df = category_df[
        category_df["Category"]
        == selected_category
    ].copy()


# --------------------------------------------------
# TRANSACTION TABLE
# --------------------------------------------------

if category_df.empty:

    st.info(
        "No transactions found for the selected filters."
    )

else:

    display_df = category_df.sort_values(
        "Date",
        ascending=False,
    ).copy()


    # ----------------------------------------------
    # IMPORTANT:
    # SHOW AMOUNTS AS POSITIVE VALUES
    # ----------------------------------------------

    display_df["Amount"] = (
        display_df["Amount"]
        .abs()
    )


    display_df["Date"] = (
        display_df["Date"]
        .dt.strftime("%d/%m/%Y")
    )


    display_df = display_df[
        [
            "Date",
            "Description",
            "Category",
            "Amount",
            "Type",
            "Paid to or received from",
        ]
    ].copy()


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={

            "Date": st.column_config.TextColumn(
                "Date",
            ),

            "Description": st.column_config.TextColumn(
                "Description",
            ),

            "Category": st.column_config.TextColumn(
                "Category",
            ),

            "Amount": st.column_config.NumberColumn(
                "Amount",
                format="₹%.2f",
            ),

            "Type": st.column_config.TextColumn(
                "Type",
            ),

            "Paid to or received from":
                st.column_config.TextColumn(
                    "Paid to or received from",
                ),
        },
    )


# --------------------------------------------------
# 12-MONTH SPENDING CHART
# --------------------------------------------------

st.divider()

st.subheader(
    f"Monthly Spending — {selected_year}"
)


# Month numbers 1-12
month_numbers = list(
    range(1, 13)
)


month_labels = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


monthly_spending = (
    year_df[
        year_df["Type"] == "Expense"
    ]
    .groupby("Month")[
        "Expense Amount"
    ]
    .sum()
)


monthly_chart_df = pd.DataFrame(
    {
        "Month": month_labels,
        "Spending": [
            monthly_spending.get(
                month_number,
                0,
            )
            for month_number
            in month_numbers
        ],
    }
)


monthly_chart_df = (
    monthly_chart_df
    .set_index("Month")
)


st.bar_chart(
    monthly_chart_df,
    y="Spending",
)


st.caption(
    "Monthly spending includes all expense transactions "
    "for the selected year. Months with no spending show ₹0."
)
