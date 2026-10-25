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

col1, col2, col3, col4 = st.columns(4)

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

with col4:
    date_range = st.date_input(
        "Date Range",
        value=(
            df["Date"].min().date(),
            df["Date"].max().date(),
        ),
    )


# -----------------------------
# Apply filters
# -----------------------------

filtered_df = df.copy()


if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date)
        & (filtered_df["Date"].dt.date <= end_date)
    ]


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
# Export filtered transactions
# -----------------------------

st.divider()

st.subheader("📥 Export Transactions")

export_df = filtered_df.sort_values(
    "Date",
    ascending=False,
).copy()

export_df["Date"] = export_df["Date"].dt.strftime(
    "%d/%m/%Y"
)

export_df = export_df[
    [
        "ID",
        "Date",
        "Description",
        "Category",
        "Amount",
        "Type",
        "Paid to or received from",
    ]
]

csv_data = export_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="expense_transactions.csv",
    mime="text/csv",
    use_container_width=True,
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

            try:
                amount = float(changed_row["Amount"])
            except (ValueError, TypeError):

                st.error(
                    f"Invalid amount for transaction #{transaction_id}."
                )

                st.stop()

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


# -----------------------------
# Delete transaction
# -----------------------------

st.divider()

st.subheader("🗑️ Delete Transaction")

st.warning(
    "Deleted transactions will be permanently removed from your "
    "Google Sheet."
)


if filtered_df.empty:

    st.info("There are no transactions available to delete.")

else:

    delete_options = filtered_df.sort_values(
        "Date",
        ascending=False,
    ).copy()

    delete_options["Delete Label"] = delete_options.apply(
        lambda row: (
            f"#{int(row['ID'])} | "
            f"{row['Date'].strftime('%d/%m/%Y')} | "
            f"{row['Description'] or 'No description'} | "
            f"₹{abs(row['Amount']):,.2f}"
        ),
        axis=1,
    )

    selected_delete_label = st.selectbox(
        "Select transaction to delete",
        delete_options["Delete Label"].tolist(),
    )

    selected_delete_row = delete_options[
        delete_options["Delete Label"] == selected_delete_label
    ].iloc[0]

    selected_delete_id = selected_delete_row["ID"]

    confirm_delete = st.checkbox(
        "I understand that this transaction will be permanently deleted."
    )

    if st.button(
        "🗑️ Delete Transaction",
        type="secondary",
        disabled=not confirm_delete,
    ):

        try:

            records = worksheet.get_all_records()

            sheet_row_number = None

            for row_number, record in enumerate(
                records,
                start=2,
            ):

                if str(record.get("ID", "")).strip() == str(
                    selected_delete_id
                ).strip():

                    sheet_row_number = row_number
                    break

            if sheet_row_number is None:

                st.error(
                    f"Transaction #{selected_delete_id} "
                    "could not be found in Google Sheets."
                )

            else:

                worksheet.delete_rows(sheet_row_number)

                st.success(
                    f"✅ Transaction #{int(selected_delete_id)} "
                    "deleted successfully!"
                )

                st.rerun()

        except Exception as e:

            st.error("Unable to delete the transaction.")
            st.exception(e)
