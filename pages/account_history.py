import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.data import load_expenses


st.set_page_config(
    page_title="Account History",
    layout="wide",
)


st.title("Account History")
st.caption("View your income and spending history")


# ==================================================
# LOAD DATA
# ==================================================

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


# ==================================================
# PREPARE DATA
# ==================================================

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


# ==================================================
# FILTER OPTIONS
# ==================================================

available_years = sorted(
    df["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist(),
    reverse=True,
)


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


# ==================================================
# COMPACT FILTER BAR
# ==================================================

filter_col1, filter_col2, filter_col3 = st.columns(
    [1, 1.4, 1.6]
)


with filter_col1:

    selected_year = st.selectbox(
        "Year",
        available_years,
        label_visibility="collapsed",
    )


with filter_col2:

    selected_month = st.selectbox(
        "Month",
        month_names,
        label_visibility="collapsed",
    )


# --------------------------------------------------
# YEAR + MONTH DATA
# --------------------------------------------------

year_df = df[
    df["Year"] == selected_year
].copy()


if selected_month != "All Months":

    selected_month_number = (
        month_names.index(
            selected_month
        )
    )

    filtered_month_df = year_df[
        year_df["Month"]
        == selected_month_number
    ].copy()

else:

    filtered_month_df = year_df.copy()


# --------------------------------------------------
# CATEGORY TOTALS FOR SELECTED PERIOD
# --------------------------------------------------

category_totals = (
    filtered_month_df[
        filtered_month_df["Type"] == "Expense"
    ]
    .groupby("Category")[
        "Expense Amount"
    ]
    .sum()
    .sort_values(
        ascending=False
    )
)


category_options = [
    "All Categories"
]


for category, amount in category_totals.items():

    category_options.append(
        f"{category} — ₹{amount:,.2f}"
    )


with filter_col3:

    selected_category_label = st.selectbox(
        "Category",
        category_options,
        label_visibility="collapsed",
    )


# ==================================================
# CATEGORY SELECTION
# ==================================================

if selected_category_label == "All Categories":

    selected_category = "All Categories"

    filtered_df = filtered_month_df.copy()

else:

    selected_category = (
        selected_category_label
        .split(" — ₹")[0]
    )

    filtered_df = filtered_month_df[
        filtered_month_df["Category"]
        == selected_category
    ].copy()


# ==================================================
# PERIOD DESCRIPTION
# ==================================================

if selected_month == "All Months":

    st.caption(
        f"Account activity for {selected_year}"
    )

else:

    st.caption(
        f"Account activity for "
        f"{selected_month} {selected_year}"
    )


# ==================================================
# SUMMARY
# ==================================================

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


# ==================================================
# SELECTED CATEGORY TOTAL
# ==================================================

if selected_category != "All Categories":

    st.divider()

    category_total = (
        filtered_df.loc[
            filtered_df["Type"] == "Expense",
            "Expense Amount",
        ].sum()
    )


    st.subheader(
        f"{selected_category} Spending"
    )


    st.metric(
        "Total Spent",
        f"₹{category_total:,.2f}",
    )


# ==================================================
# CATEGORY BREAKDOWN
# ==================================================

st.divider()

st.subheader("Category Spending")


if category_totals.empty:

    st.info(
        "No expense data available for the selected period."
    )

else:

    category_display = (
        category_totals
        .reset_index()
    )


    category_display.columns = [
        "Category",
        "Total Spent",
    ]


    st.dataframe(
        category_display,
        use_container_width=True,
        hide_index=True,
        column_config={

            "Category": st.column_config.TextColumn(
                "Category",
            ),

            "Total Spent": st.column_config.NumberColumn(
                "Total Spent",
                format="₹%.2f",
            ),
        },
    )


# ==================================================
# TRANSACTIONS
# ==================================================

st.divider()

st.subheader("Transactions")


if filtered_df.empty:

    st.info(
        "No transactions found for the selected filters."
    )

else:

    display_df = filtered_df.sort_values(
        "Date",
        ascending=False,
    ).copy()


    # Always show positive amounts
    display_df["Amount"] = (
        display_df["Amount"].abs()
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


# ==================================================
# MONTHLY SPENDING GRAPH
# ==================================================

st.divider()

st.subheader(
    f"Monthly Spending — {selected_year}"
)


# Fixed Jan → Dec order
month_chart_labels = [
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


month_chart_numbers = list(
    range(1, 13)
)


# --------------------------------------------------
# MONTHLY SPENDING
# --------------------------------------------------

if selected_category == "All Categories":

    chart_source_df = year_df.copy()

else:

    chart_source_df = year_df[
        year_df["Category"]
        == selected_category
    ].copy()


monthly_spending = (
    chart_source_df[
        chart_source_df["Type"] == "Expense"
    ]
    .groupby("Month")[
        "Expense Amount"
    ]
    .sum()
)


monthly_values = [
    float(
        monthly_spending.get(
            month_number,
            0,
        )
    )
    for month_number
    in month_chart_numbers
]


chart_df = pd.DataFrame(
    {
        "Month": month_chart_labels,
        "Spending": monthly_values,
    }
)


# ==================================================
# MODERN PLOTLY CHART
# ==================================================

fig = go.Figure()


fig.add_trace(
    go.Bar(
        x=chart_df["Month"],
        y=chart_df["Spending"],
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Spending: ₹%{y:,.2f}"
            "<extra></extra>"
        ),
        marker=dict(
            line=dict(
                width=0,
            ),
        ),
    )
)


fig.update_layout(

    height=360,

    margin=dict(
        l=10,
        r=10,
        t=20,
        b=10,
    ),

    xaxis=dict(
        title=None,
        categoryorder="array",
        categoryarray=month_chart_labels,
        showgrid=False,
        fixedrange=True,
    ),

    yaxis=dict(
        title=None,
        showgrid=True,
        gridcolor="rgba(128,128,128,0.15)",
        zeroline=True,
        tickprefix="₹",
        fixedrange=True,
    ),

    plot_bgcolor="rgba(0,0,0,0)",

    paper_bgcolor="rgba(0,0,0,0)",

    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
    ),

    bargap=0.35,

    showlegend=False,
)


st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


if selected_category == "All Categories":

    st.caption(
        "Monthly spending across all expense categories."
    )

else:

    st.caption(
        f"Monthly spending for {selected_category}."
    )
