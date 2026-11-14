import streamlit as st

from utils.sheets import get_google_sheet


st.title("➕ Add Transaction")
st.caption("Add a new income or expense to your Google Sheet")


try:
    worksheet = get_google_sheet()

except Exception as e:
    st.error("Unable to connect to Google Sheets.")
    st.exception(e)
    st.stop()


st.subheader("Transaction Details")


with st.form("transaction_form"):

    date = st.date_input("Date")

    description = st.text_input(
        "Description",
        placeholder="Example: Grocery shopping",
    )

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


if submitted:

    if amount <= 0:

        st.error(
            "Please enter an amount greater than 0."
        )

    else:

        if transaction_type == "Expense":
            final_amount = -amount
        else:
            final_amount = amount

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
            "Refresh the Account History page to see the new transaction."
        )
