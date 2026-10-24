import streamlit as st

from utils.sheets import get_google_sheet


st.set_page_config(
    page_title="Add Transaction",
    page_icon="➕",
    layout="wide",
)


st.title("➕ Add Transaction")
st.caption("Add a new income or expense to your Google Sheet")


# -----------------------------
# Load Google Sheet
# -----------------------------

try:
    worksheet = get_google_sheet()

except Exception as e:
    st.error("Unable to connect to Google Sheets.")
    st.exception(e)
    st.stop()


# -----------------------------
# Transaction Form
# -----------------------------

st.subheader("Transaction Details")


with st.form("transaction_form"):

    date = st.date_input("Date")

    description = st.text_input(
        "Description",
        placeholder="Example: Grocery shopping",
    )

    # Get existing categories from the sheet
    records = worksheet.get_all_records()

    existing_categories = sorted(
        {
            str(row["Category"]).strip()
            for row in records
            if row.get("Category")
        }
    )

    category = st.selectbox(
        "Category",
        existing_categories,
    )

    transaction_type = st.selectbox(
        "Type",
        ["Expense", "Income"],
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


# -----------------------------
# Save Transaction
# -----------------------------

if submitted:

    if amount <= 0:
        st.error("Please enter an amount greater than 0.")

    else:

        # Make expense negative and income positive
        if transaction_type == "Expense":
            final_amount = -amount
        else:
            final_amount = amount

        # Get existing IDs
        existing_ids = [
            row.get("ID")
            for row in records
            if row.get("ID") not in ("", None)
        ]

        numeric_ids = []

        for existing_id in existing_ids:
            try:
                numeric_ids.append(int(existing_id))
            except (ValueError, TypeError):
                pass

        if numeric_ids:
            new_id = max(numeric_ids) + 1
        else:
            new_id = 1

        # Add new row to Google Sheet
        worksheet.append_row(
            [
                new_id,
                date.strftime("%d/%m/%Y"),
                description,
                category,
                final_amount,
                paid_to_received_from,
            ]
        )

        st.success(
            f"Transaction #{new_id} added successfully! 🎉"
        )

        st.info(
            "Your Google Sheet has been updated. "
            "Refresh the Transactions page to see the new transaction."
        )