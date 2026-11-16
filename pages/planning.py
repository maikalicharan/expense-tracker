import streamlit as st
import pandas as pd
from datetime import date

from utils.data import load_expenses
from utils.sheets import get_google_sheet
from utils.planning import (
    VALID_BUCKETS,
    calculate_budget_actuals,
    calculate_planned_amounts,
    budget_comparison,
)


st.set_page_config(
    page_title="Planning",
    layout="wide",
)


st.title("Planning")
st.caption(
    "Plan your spending, savings and financial goals"
)


# ==================================================
# LOAD DATA
# ==================================================

try:

    df = load_expenses()
    worksheet = get_google_sheet()
    spreadsheet = worksheet.spreadsheet

except Exception as e:

    st.error(
        "Unable to load financial planning data."
    )
    st.exception(e)
    st.stop()


if df.empty:

    st.info(
        "Add some income and expense transactions "
        "before creating a financial plan."
    )
    st.stop()


df = df.copy()

df = df.dropna(
    subset=["Date"]
)

df["Year"] = df["Date"].dt.year
df["Month Period"] = df["Date"].dt.to_period("M")


# ==================================================
# BUDGET PLANS SHEET
# ==================================================

try:

    try:

        budget_worksheet = spreadsheet.worksheet(
            "Budget_Plans"
        )

    except Exception:

        budget_worksheet = spreadsheet.add_worksheet(
            title="Budget_Plans",
            rows=1000,
            cols=6,
        )

        budget_worksheet.append_row(
            [
                "Year",
                "Needs %",
                "Investment %",
                "Lifestyle %",
                "Goal Name",
                "Goal Amount",
            ]
        )

except Exception as e:

    st.error(
        "Unable to prepare Budget_Plans worksheet."
    )
    st.exception(e)
    st.stop()


# ==================================================
# BUDGET CATEGORIES SHEET
# ==================================================

try:

    try:

        category_worksheet = spreadsheet.worksheet(
            "Budget_Categories"
        )

    except Exception:

        category_worksheet = spreadsheet.add_worksheet(
            title="Budget_Categories",
            rows=1000,
            cols=2,
        )

        category_worksheet.append_row(
            [
                "Category",
                "Planning Bucket",
            ]
        )

except Exception as e:

    st.error(
        "Unable to prepare Budget_Categories worksheet."
    )
    st.exception(e)
    st.stop()


# ==================================================
# LOAD CATEGORY MAPPINGS
# ==================================================

try:

    category_records = (
        category_worksheet
        .get_all_records()
    )

except Exception as e:

    st.error(
        "Unable to load category mappings."
    )
    st.exception(e)
    st.stop()


category_mapping = {}

for record in category_records:

    category = str(
        record.get(
            "Category",
            "",
        )
    ).strip()

    bucket = str(
        record.get(
            "Planning Bucket",
            "",
        )
    ).strip()

    if (
        category
        and bucket in VALID_BUCKETS
    ):

        category_mapping[category] = bucket


# ==================================================
# YEAR SELECTION
# ==================================================

available_years = sorted(
    df["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist(),
    reverse=True,
)


selected_year = st.selectbox(
    "Planning Year",
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


# ==================================================
# FINANCIAL POSITION
# ==================================================

total_income = year_df.loc[
    year_df["Type"] == "Income",
    "Amount",
].sum()


total_expenses = year_df.loc[
    year_df["Type"] == "Expense",
    "Expense Amount",
].sum()


actual_savings = (
    total_income
    - total_expenses
)


st.divider()

st.subheader(
    f"Financial Position — {selected_year}"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Income",
        f"₹{total_income:,.2f}",
    )


with col2:

    st.metric(
        "Expenses",
        f"₹{total_expenses:,.2f}",
    )


with col3:

    st.metric(
        "Savings",
        f"₹{actual_savings:,.2f}",
    )


# ==================================================
# LOAD SAVED PLAN
# ==================================================

try:

    budget_records = (
        budget_worksheet
        .get_all_records()
    )

except Exception as e:

    st.error(
        "Unable to load saved planning settings."
    )
    st.exception(e)
    st.stop()


saved_plan = None


for record in budget_records:

    try:

        record_year = int(
            float(
                record.get(
                    "Year",
                    0,
                )
            )
        )

    except (
        ValueError,
        TypeError,
    ):

        continue


    if record_year == selected_year:

        saved_plan = record
        break


if saved_plan:

    default_needs = float(
        saved_plan.get(
            "Needs %",
            50,
        )
        or 50
    )

    default_investment = float(
        saved_plan.get(
            "Investment %",
            20,
        )
        or 20
    )

    default_lifestyle = float(
        saved_plan.get(
            "Lifestyle %",
            30,
        )
        or 30
    )

    default_goal_name = str(
        saved_plan.get(
            "Goal Name",
            "",
        )
        or ""
    )

    default_goal_amount = float(
        saved_plan.get(
            "Goal Amount",
            0,
        )
        or 0
    )

else:

    default_needs = 50.0
    default_investment = 20.0
    default_lifestyle = 30.0

    default_goal_name = ""
    default_goal_amount = 0.0


# ==================================================
# BUDGET ALLOCATION
# ==================================================

st.divider()

st.subheader(
    "Budget Allocation"
)


col1, col2, col3 = st.columns(3)


with col1:

    needs_percent = st.number_input(
        "Needs %",
        min_value=0.0,
        max_value=100.0,
        value=default_needs,
        step=1.0,
    )


with col2:

    investment_percent = st.number_input(
        "Investment %",
        min_value=0.0,
        max_value=100.0,
        value=default_investment,
        step=1.0,
    )


with col3:

    lifestyle_percent = st.number_input(
        "Lifestyle %",
        min_value=0.0,
        max_value=100.0,
        value=default_lifestyle,
        step=1.0,
    )


total_percentage = (
    needs_percent
    + investment_percent
    + lifestyle_percent
)


if abs(
    total_percentage - 100
) > 0.001:

    st.warning(
        f"Allocation currently totals "
        f"{total_percentage:.1f}%. "
        "It must total 100%."
    )


# ==================================================
# PLANNED AMOUNTS
# ==================================================

planned = calculate_planned_amounts(
    total_income,
    needs_percent,
    investment_percent,
    lifestyle_percent,
)


st.divider()

st.subheader(
    "Planned Budget"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Planned Needs",
        f"₹{planned['Needs']:,.2f}",
    )


with col2:

    st.metric(
        "Planned Investment",
        f"₹{planned['Investment']:,.2f}",
    )


with col3:

    st.metric(
        "Planned Lifestyle",
        f"₹{planned['Lifestyle']:,.2f}",
    )


# ==================================================
# CATEGORY MAPPING
# ==================================================

st.divider()

st.subheader(
    "Category Mapping"
)

st.caption(
    "Assign each expense category to Needs, "
    "Investment or Lifestyle. This mapping is "
    "used by Planning and Dashboard."
)


all_categories = sorted(
    year_df[
        year_df["Type"] == "Expense"
    ]["Category"]
    .dropna()
    .astype(str)
    .str.strip()
    .loc[
        lambda x: x != ""
    ]
    .unique()
    .tolist()
)


if not all_categories:

    st.info(
        "No expense categories are available "
        "for mapping yet."
    )

else:

    mapping_rows = []


    for category in all_categories:

        current_bucket = (
            category_mapping.get(
                category,
                "Needs",
            )
        )

        mapping_rows.append(
            {
                "Category": category,
                "Planning Bucket": current_bucket,
            }
        )


    mapping_df = pd.DataFrame(
        mapping_rows
    )


    edited_mapping = st.data_editor(
        mapping_df,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        disabled=["Category"],
        column_config={

            "Category": st.column_config.TextColumn(
                "Category",
                disabled=True,
            ),

            "Planning Bucket":
                st.column_config.SelectboxColumn(
                    "Planning Bucket",
                    options=VALID_BUCKETS,
                    required=True,
                ),
        },
        key="budget_category_mapping",
    )


    if st.button(
        "Save Category Mapping",
        type="primary",
    ):

        try:

            existing_records = (
                category_worksheet
                .get_all_records()
            )


            existing_rows = {}

            for row_number, record in enumerate(
                existing_records,
                start=2,
            ):

                category = str(
                    record.get(
                        "Category",
                        "",
                    )
                ).strip()

                if category:

                    existing_rows[
                        category
                    ] = row_number


            saved_count = 0


            for _, row in edited_mapping.iterrows():

                category = str(
                    row["Category"]
                ).strip()

                bucket = str(
                    row["Planning Bucket"]
                ).strip()


                if (
                    not category
                    or bucket not in VALID_BUCKETS
                ):

                    continue


                if category in existing_rows:

                    row_number = existing_rows[
                        category
                    ]

                    category_worksheet.update(
                        f"A{row_number}:B{row_number}",
                        [[
                            category,
                            bucket,
                        ]],
                    )

                else:

                    category_worksheet.append_row(
                        [
                            category,
                            bucket,
                        ]
                    )


                saved_count += 1


            st.success(
                f"{saved_count} category mapping(s) saved."
            )

            st.rerun()


        except Exception as e:

            st.error(
                "Unable to save category mappings."
            )

            st.exception(e)


# ==================================================
# ACTUAL BUDGET SPENDING
# ==================================================

expense_df = year_df[
    year_df["Type"] == "Expense"
].copy()


actual = calculate_budget_actuals(
    expense_df,
    category_mapping,
)


comparison_df = budget_comparison(
    planned,
    actual,
)


st.divider()

st.subheader(
    "Actual vs Planned"
)


display_comparison = comparison_df.copy()


display_comparison["Status"] = (
    display_comparison["Difference"]
    .apply(
        lambda value:
        "Remaining"
        if value >= 0
        else "Over Budget"
    )
)


st.dataframe(
    display_comparison,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Category": st.column_config.TextColumn(
            "Category",
        ),

        "Planned": st.column_config.NumberColumn(
            "Planned",
            format="₹%.2f",
        ),

        "Actual": st.column_config.NumberColumn(
            "Actual",
            format="₹%.2f",
        ),

        "Difference": st.column_config.NumberColumn(
            "Difference",
            format="₹%.2f",
        ),

        "Status": st.column_config.TextColumn(
            "Status",
        ),
    },
)


# ==================================================
# BUDGET STATUS
# ==================================================

st.subheader(
    "Budget Status"
)


for _, row in comparison_df.iterrows():

    bucket = row["Category"]
    difference = float(
        row["Difference"]
    )


    if difference >= 0:

        st.success(
            f"{bucket}: "
            f"₹{difference:,.2f} remaining."
        )

    else:

        st.warning(
            f"{bucket}: "
            f"₹{abs(difference):,.2f} over budget."
        )


# ==================================================
# GOAL PLANNING
# ==================================================

st.divider()

st.subheader(
    "Savings Goal"
)


goal_name = st.text_input(
    "Goal Name",
    value=default_goal_name,
    placeholder="Example: Emergency Fund",
)


goal_amount = st.number_input(
    "Goal Amount",
    min_value=0.0,
    value=default_goal_amount,
    step=1000.0,
    format="%.2f",
)


goal_target_date = st.date_input(
    "Goal Target Date",
    value=date.today(),
)


required_monthly_saving = 0.0


if goal_amount > 0:

    today = pd.Timestamp.today().normalize()

    target_timestamp = pd.Timestamp(
        goal_target_date
    )


    months_remaining = (
        (
            target_timestamp.year
            - today.year
        )
        * 12
        +
        (
            target_timestamp.month
            - today.month
        )
    )


    if months_remaining <= 0:

        months_remaining = 1


    required_monthly_saving = (
        goal_amount
        / months_remaining
    )


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Goal Amount",
        f"₹{goal_amount:,.2f}",
    )


with col2:

    st.metric(
        "Required Monthly Saving",
        f"₹{required_monthly_saving:,.2f}",
    )


# ==================================================
# AVERAGE MONTHLY SAVING
# ==================================================

monthly_income = (
    year_df[
        year_df["Type"] == "Income"
    ]
    .groupby("Month Period")["Amount"]
    .sum()
)


monthly_expenses = (
    year_df[
        year_df["Type"] == "Expense"
    ]
    .groupby("Month Period")["Expense Amount"]
    .sum()
)


monthly_savings = (
    monthly_income
    .sub(
        monthly_expenses,
        fill_value=0,
    )
)


if not monthly_savings.empty:

    average_monthly_saving = (
        monthly_savings.mean()
    )

else:

    average_monthly_saving = 0.0


if goal_amount > 0:

    st.metric(
        "Average Monthly Saving",
        f"₹{average_monthly_saving:,.2f}",
    )


    if (
        average_monthly_saving
        >= required_monthly_saving
    ):

        st.success(
            "Your current average monthly savings "
            "support this goal timeline."
        )

    else:

        shortfall = (
            required_monthly_saving
            - average_monthly_saving
        )

        st.warning(
            f"You need approximately "
            f"₹{shortfall:,.2f} more monthly savings "
            "to meet this goal timeline."
        )


# ==================================================
# SAVE PLANNING
# ==================================================

st.divider()

if st.button(
    "Save / Update Planning",
    type="primary",
):

    if abs(
        total_percentage - 100
    ) > 0.001:

        st.error(
            "Needs, Investment and Lifestyle "
            "must total exactly 100%."
        )

        st.stop()


    if goal_amount < 0:

        st.error(
            "Goal amount cannot be negative."
        )

        st.stop()


    try:

        records = (
            budget_worksheet
            .get_all_records()
        )


        existing_row_number = None


        for row_number, record in enumerate(
            records,
            start=2,
        ):

            try:

                record_year = int(
                    float(
                        record.get(
                            "Year",
                            0,
                        )
                    )
                )

            except (
                ValueError,
                TypeError,
            ):

                continue


            if record_year == selected_year:

                existing_row_number = (
                    row_number
                )

                break


        row_values = [
            selected_year,
            float(needs_percent),
            float(investment_percent),
            float(lifestyle_percent),
            goal_name.strip(),
            float(goal_amount),
        ]


        if existing_row_number is None:

            budget_worksheet.append_row(
                row_values
            )

            st.success(
                f"Planning for {selected_year} "
                "saved successfully!"
            )

        else:

            budget_worksheet.update(
                f"A{existing_row_number}:F{existing_row_number}",
                [row_values],
            )

            st.success(
                f"Planning for {selected_year} "
                "updated successfully!"
            )


        st.rerun()


    except Exception as e:

        st.error(
            "Unable to save planning settings."
        )

        st.exception(e)


# ==================================================
# PLANNING INSIGHTS
# ==================================================

st.divider()

st.subheader(
    "Planning Insights"
)


if total_income <= 0:

    st.warning(
        "Add income transactions to create "
        "a meaningful financial plan."
    )

elif actual_savings < 0:

    st.error(
        f"Expenses are ₹{abs(actual_savings):,.2f} "
        "higher than income for this year."
    )

elif goal_amount > 0:

    if (
        average_monthly_saving
        >= required_monthly_saving
    ):

        st.success(
            "Your current savings pattern supports "
            "your planned goal timeline."
        )

    else:

        st.warning(
            "Your current savings pattern may require "
            "higher monthly savings or a longer goal timeline."
        )

else:

    st.info(
        "Create a savings goal to compare your "
        "savings capacity with a target."
    )
