import streamlit as st

from utils.sheets import get_google_sheet
from utils.data import load_expenses


st.title("➕ Add Transaction")
st.caption("Add a new income or expense to your Google Sheet")


try:
    worksheet = get_google_sheet()

except Exception as e:
    st.error("Unable to connect to Google Sheets.")
    st.exception(e)
    st.stop()


st.subheader("Transaction Details")


# ---------------------------------------------------------
# Load existing categories
# ---------------------------------------------------------

try:

    records = worksheet.get_all_records()

    existing_categories = sorted(
        {
            str(row.get("Category", "")).strip()
            for row in records
            if str(row.get("Category", "")).strip()
        }
    )

except Exception as e:

    st.error("Unable to load categories.")
    st.exception(e)
    st.stop()


# ---------------------------------------------------------
# Transaction form
# ---------------------------------------------------------

with st.form("transaction_form"):

    date = st.date_input(
        "Date"
    )

    description = st.text_input(
        "Description",
        placeholder="Example: Grocery shopping",
    )

    category_options = [
        "➕ Add New Category"
    ] + existing_categories

    selected_category = st.selectbox(
        "Category",
        category_options,
    )

    if selected_category == "➕ Add New Category":

        new_category = st.text_input(
            "New Category",
            placeholder="Example: Groceries",
        )

    else:

        new_category = ""


    transaction_type = st.selectbox(
        "Type",
        [
            "Expense",
            "Income",
        ],
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0,
        format="%.2f",
    )

    paid_to_received_from = st.text_input(
        "Paid to or received from",
        placeholder="Example: Shop / Person / Company",
    )

    submitted = st.form_submit_button(
        "💾 Save Transaction",
        use_container_width=True,
    )


# ---------------------------------------------------------
# Save transaction
# ---------------------------------------------------------

if submitted:

    # Determine final category

    if selected_category == "➕ Add New Category":

        final_category = new_category.strip()

        if not final_category:

            st.error(
                "Please enter a category name."
            )

            st.stop()

    else:

        final_category = selected_category


    # Validate amount

    if amount <= 0:

        st.error(
            "Please enter an amount greater than 0."
        )

        st.stop()


    # Determine positive / negative amount

    if transaction_type == "Expense":

        final_amount = -amount

    else:

        final_amount = amount


    try:

        # Get latest records before generating ID

        records = worksheet.get_all_records()


        # -------------------------------------------------
        # Generate new ID
        # -------------------------------------------------

        existing_ids = [
            row.get("ID")
            for row in records
            if row.get("ID") not in ("", None)
        ]

        numeric_ids = []

        for existing_id in existing_ids:

            try:

                numeric_ids.append(
                    int(float(existing_id))
                )

            except (ValueError, TypeError):

                pass


        if numeric_ids:

            new_id = max(numeric_ids) + 1

        else:

            new_id = 1


        # -------------------------------------------------
        # Add row to Google Sheet
        # -------------------------------------------------

        worksheet.append_row(
            [
                new_id,
                date.strftime("%d/%m/%Y"),
                description.strip(),
                final_category,
                final_amount,
                paid_to_received_from.strip(),
            ]
        )


        # Clear cached data so other pages get fresh data

        load_expenses.clear()


        st.success(
            f"Transaction #{new_id} added successfully! 🎉"
        )

        st.info(
            "Your transaction has been saved. "
            "You can now view it in Account History or Transactions."
        )


    except Exception as e:

        st.error(
            "Unable to save the transaction to Google Sheets."
        )

        st.exception(e)
