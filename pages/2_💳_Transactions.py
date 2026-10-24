```python
import streamlit as st

from utils.data import load_expenses
from utils.sheets import get_google_sheet


st.set_page_config(
    page_title="Transactions",
    page_icon="💳",
    layout="wide",
)

st.title("💳 Transactions")
st.caption("Search, edit and manage your transactions")


# -----------------------------
# Load data
# -----------------------------

try:
    df = load_expenses()
    worksheet = get_google_sheet()

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

st.subheader("✏️ Edit Transactions")

st.info(
    "You can edit Date, Description, Category, Amount and "
    "Paid to or received from. After editing, click Save Changes."
)


# Keep the original row ID so we know which Google Sheet row to update.
editable_df = filtered_df.sort_values(
    "Date",
    ascending=False,
).copy()


editable_df["Date"] = editable_df["Date"].dt.strftime(
    "%d/%m/%Y"
)


editable_df = editable_df[
    [
        "ID",
        "Date",
        "Description",
        "Category",
        "Amount",
        "Paid to or received from",
    ]
].copy()


edited_df = st.data_editor(
    editable_df,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    disabled=["ID"],
    column_config={
        "ID": st.column_config.NumberColumn(
            "ID",
            disabled=True,
        ),
        "Date": st.column_config.TextColumn(
            "Date",
            help="Format: DD/MM/YYYY",
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
        "Paid to or received from": st.column_config.TextColumn(
            "Paid to or received from",
        ),
    },
    key="transaction_editor",
)


# -----------------------------
# Save changes
# -----------------------------

if st.button(
    "💾 Save Changes",
    type="primary",
    use_container_width=True,
):

    try:

        original_df = editable_df.reset_index(drop=True)
        changed_df = edited_df.reset_index(drop=True)

        changes_made = 0

        for index in range(len(changed_df)):

            original_row = original_df.iloc[index]
            changed_row = changed_df.iloc[index]

            if original_row.equals(changed_row):
                continue

            transaction_id = changed_row["ID"]

            # Find the transaction in the Google Sheet.
            records = worksheet.get_all_records()

            sheet_row_number = None

            for row_number, record in enumerate(
                records,
                start=2,
            ):

                if str(record.get("ID", "")).strip() == str(
                    transaction_id
                ).strip():

                    sheet_row_number = row_number
                    break

            if sheet_row_number is None:
                continue

            # Validate amount.
            try:
                amount = float(changed_row["Amount"])
            except (ValueError, TypeError):
                st.error(
                    f"Invalid amount for transaction #{transaction_id}."
                )
                st.stop()

            # Update Google Sheet row.
            worksheet.update(
                f"A{sheet_row_number}:F{sheet_row_number}",
                [[
                    int(transaction_id),
                    str(changed_row["Date"]),
                    str(changed_row["Description"]),
                    str(changed_row["Category"]),
                    amount,
                    str(changed_row["Paid to or received from"]),
                ]],
            )

            changes_made += 1

        if changes_made > 0:

            st.success(
                f"✅ {changes_made} transaction(s) updated successfully!"
            )

            st.rerun()

        else:

            st.info("No changes were made.")

    except Exception as e:

        st.error("Unable to save changes to Google Sheets.")
        st.exception(e)
```
