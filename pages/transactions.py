import streamlit as st
import io
import pandas as pd

from utils.data import load_expenses
from utils.sheets import get_google_sheet


st.set_page_config(
    page_title="Transactions",
    layout="wide",
)


st.title("Transactions")
st.caption("Search, edit and manage your transactions")


# ==================================================
# LOAD DATA
# ==================================================

try:

    df = load_expenses()
    worksheet = get_google_sheet()

except Exception as e:

    st.error("Unable to load transaction data.")
    st.exception(e)
    st.stop()


if df.empty:

    st.info(
        "No transactions available yet. "
        "Add your first transaction from Add Transaction."
    )

    st.stop()


# ==================================================
# FILTERS
# ==================================================

st.subheader("Filters")

col1, col2, col3, col4 = st.columns(4)


with col1:

    search_text = st.text_input(
        "Search",
        placeholder="Description or person...",
    )


with col2:

    transaction_type_filter = st.selectbox(
        "Type",
        [
            "All",
            "Income",
            "Expense",
        ],
    )


with col3:

    categories = sorted(
        df["Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_category = st.selectbox(
        "Category",
        ["All"] + categories,
    )


with col4:

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    date_range = st.date_input(
        "Date Range",
        value=(
            min_date,
            max_date,
        ),
    )


# ==================================================
# APPLY FILTERS
# ==================================================

filtered_df = df.copy()


# Date filter
if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (
            filtered_df["Date"].dt.date
            >= start_date
        )
        &
        (
            filtered_df["Date"].dt.date
            <= end_date
        )
    ]


# Search filter
if search_text.strip():

    search_value = search_text.strip()

    description_mask = (
        filtered_df["Description"]
        .fillna("")
        .astype(str)
        .str.contains(
            search_value,
            case=False,
            na=False,
        )
    )

    person_mask = (
        filtered_df[
            "Paid to or received from"
        ]
        .fillna("")
        .astype(str)
        .str.contains(
            search_value,
            case=False,
            na=False,
        )
    )

    filtered_df = filtered_df[
        description_mask | person_mask
    ]


# Type filter
if transaction_type_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Type"]
        == transaction_type_filter
    ]


# Category filter
if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"]
        == selected_category
    ]


# ==================================================
# SUMMARY
# ==================================================

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


# ==================================================
# EXPORT
# ==================================================

st.divider()

st.subheader("Export Transactions")


export_df = (
    filtered_df
    .sort_values(
        "Date",
        ascending=False,
    )
    .copy()
)


# Always show positive amount to user
export_df["Amount"] = (
    export_df["Amount"].abs()
)


export_df["Date"] = (
    export_df["Date"]
    .dt.strftime("%d/%m/%Y")
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


col1, col2 = st.columns(2)


with col1:

    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="expense_transactions.csv",
        mime="text/csv",
        use_container_width=True,
    )


with col2:

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl",
    ) as writer:

        export_df.to_excel(
            writer,
            index=False,
            sheet_name="Transactions",
        )

    excel_buffer.seek(0)

    st.download_button(
        label="Download Excel",
        data=excel_buffer,
        file_name="expense_transactions.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
    )


# ==================================================
# EDIT TRANSACTIONS
# ==================================================

st.divider()

st.subheader("Edit Transactions")


if filtered_df.empty:

    st.info(
        "No transactions match the selected filters."
    )

else:

    st.caption(
        "Amount is always entered as a positive value. "
        "Select Income or Expense to determine how it "
        "is stored internally."
    )


    # --------------------------------------------------
    # SORT DATA
    # --------------------------------------------------

    editable_source_df = (
        filtered_df
        .sort_values(
            "Date",
            ascending=False,
        )
        .copy()
    )


    # --------------------------------------------------
    # CREATE USER-FACING EDIT TABLE
    # --------------------------------------------------

    editable_df = editable_source_df[
        [
            "ID",
            "Date",
            "Description",
            "Category",
            "Amount",
            "Type",
            "Paid to or received from",
        ]
    ].copy()


    # Date shown as DD/MM/YYYY
    editable_df["Date"] = (
        editable_df["Date"]
        .dt.strftime("%d/%m/%Y")
    )


    # Amount shown without negative sign
    editable_df["Amount"] = (
        editable_df["Amount"]
        .abs()
    )


    edited_df = st.data_editor(
        editable_df,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",

        disabled=[
            "ID",
        ],

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
                min_value=0.01,
            ),

            "Type": st.column_config.SelectboxColumn(
                "Type",
                options=[
                    "Income",
                    "Expense",
                ],
                required=True,
            ),

            "Paid to or received from":
                st.column_config.TextColumn(
                    "Paid to or received from",
                ),
        },

        key="transaction_editor",
    )


    # ==================================================
    # SAVE CHANGES
    # ==================================================

    if st.button(
        "Save Changes",
        type="primary",
        use_container_width=True,
    ):

        try:

            original_df = (
                editable_source_df
                .reset_index(drop=True)
                .copy()
            )

            changed_df = (
                edited_df
                .reset_index(drop=True)
                .copy()
            )


            changes_made = 0


            # --------------------------------------------------
            # PROCESS EACH ROW
            # --------------------------------------------------

            for index in range(
                len(changed_df)
            ):

                original_row = (
                    original_df.iloc[index]
                )

                changed_row = (
                    changed_df.iloc[index]
                )


                # ----------------------------------------------
                # ID
                # ----------------------------------------------

                try:

                    transaction_id = int(
                        float(
                            changed_row["ID"]
                        )
                    )

                except (
                    ValueError,
                    TypeError,
                ):

                    st.error(
                        "Invalid transaction ID."
                    )

                    st.stop()


                # ----------------------------------------------
                # DATE
                # ----------------------------------------------

                date_text = str(
                    changed_row["Date"]
                ).strip()


                try:

                    validated_date = pd.to_datetime(
                        date_text,
                        format="%d/%m/%Y",
                        errors="raise",
                    )

                except Exception:

                    st.error(
                        f"Invalid date for transaction "
                        f"#{transaction_id}. "
                        "Use DD/MM/YYYY."
                    )

                    st.stop()


                new_date = (
                    validated_date.strftime(
                        "%d/%m/%Y"
                    )
                )


                # ----------------------------------------------
                # DESCRIPTION
                # ----------------------------------------------

                description = str(
                    changed_row["Description"]
                ).strip()


                # ----------------------------------------------
                # CATEGORY
                # ----------------------------------------------

                category = str(
                    changed_row["Category"]
                ).strip()


                if not category:

                    st.error(
                        f"Category cannot be blank "
                        f"for transaction #{transaction_id}."
                    )

                    st.stop()


                # ----------------------------------------------
                # AMOUNT
                # ----------------------------------------------

                try:

                    display_amount = float(
                        changed_row["Amount"]
                    )

                except (
                    ValueError,
                    TypeError,
                ):

                    st.error(
                        f"Invalid amount for transaction "
                        f"#{transaction_id}."
                    )

                    st.stop()


                if display_amount <= 0:

                    st.error(
                        f"Amount must be greater than zero "
                        f"for transaction #{transaction_id}."
                    )

                    st.stop()


                # ----------------------------------------------
                # TYPE
                # ----------------------------------------------

                new_type = str(
                    changed_row["Type"]
                ).strip()


                if new_type not in [
                    "Income",
                    "Expense",
                ]:

                    st.error(
                        f"Invalid transaction type "
                        f"for transaction #{transaction_id}."
                    )

                    st.stop()


                # ----------------------------------------------
                # APPLY INTERNAL SIGN
                # ----------------------------------------------

                if new_type == "Income":

                    final_amount = abs(
                        display_amount
                    )

                else:

                    final_amount = -abs(
                        display_amount
                    )


                # ----------------------------------------------
                # PAID TO / RECEIVED FROM
                # ----------------------------------------------

                paid_to_received_from = str(
                    changed_row[
                        "Paid to or received from"
                    ]
                ).strip()


                # ==================================================
                # ORIGINAL VALUES
                # ==================================================

                original_amount = float(
                    original_row["Amount"]
                )

                original_type = str(
                    original_row["Type"]
                ).strip()

                original_date = (
                    original_row["Date"]
                    .strftime("%d/%m/%Y")
                    if pd.notna(
                        original_row["Date"]
                    )
                    else ""
                )

                original_description = str(
                    original_row["Description"]
                ).strip()

                original_category = str(
                    original_row["Category"]
                ).strip()

                original_person = str(
                    original_row[
                        "Paid to or received from"
                    ]
                ).strip()


                # ==================================================
                # CHECK WHETHER ANYTHING CHANGED
                # ==================================================

                if (
                    original_date
                    == new_date
                    and
                    original_description
                    == description
                    and
                    original_category
                    == category
                    and
                    original_amount
                    == final_amount
                    and
                    original_type
                    == new_type
                    and
                    original_person
                    == paid_to_received_from
                ):

                    continue


                # ==================================================
                # FIND GOOGLE SHEET ROW
                # ==================================================

                records = (
                    worksheet.get_all_records()
                )

                sheet_row_number = None


                for row_number, record in enumerate(
                    records,
                    start=2,
                ):

                    sheet_id = str(
                        record.get(
                            "ID",
                            "",
                        )
                    ).strip()


                    if sheet_id == str(
                        transaction_id
                    ).strip():

                        sheet_row_number = (
                            row_number
                        )

                        break


                if sheet_row_number is None:

                    st.error(
                        f"Transaction #{transaction_id} "
                        "could not be found in Google Sheets."
                    )

                    st.stop()


                # ==================================================
                # UPDATE GOOGLE SHEET
                # ==================================================

                worksheet.update(
                    f"A{sheet_row_number}:F{sheet_row_number}",
                    [[
                        transaction_id,
                        new_date,
                        description,
                        category,
                        final_amount,
                        paid_to_received_from,
                    ]],
                )


                changes_made += 1


            # ==================================================
            # SAVE RESULT
            # ==================================================

            if changes_made > 0:

                # Clear cached transaction data
                load_expenses.clear()

                st.success(
                    f"{changes_made} transaction(s) "
                    "updated successfully!"
                )

                st.rerun()

            else:

                st.info(
                    "No changes were made."
                )


        except Exception as e:

            st.error(
                "Unable to save changes "
                "to Google Sheets."
            )

            st.exception(e)


# ==================================================
# DELETE TRANSACTION
# ==================================================

st.divider()

st.subheader("Delete Transaction")


if filtered_df.empty:

    st.info(
        "There are no transactions available to delete."
    )

else:

    st.warning(
        "Deleted transactions will be permanently "
        "removed from your Google Sheet."
    )


    delete_options = (
        filtered_df
        .sort_values(
            "Date",
            ascending=False,
        )
        .copy()
    )


    # User-friendly delete label
    delete_options["Delete Label"] = (
        delete_options.apply(
            lambda row: (
                f"#{int(row['ID'])} | "
                f"{row['Date'].strftime('%d/%m/%Y')} | "
                f"{row['Description'] or 'No description'} | "
                f"₹{abs(row['Amount']):,.2f} | "
                f"{row['Type']}"
            ),
            axis=1,
        )
    )


    selected_delete_label = st.selectbox(
        "Select transaction to delete",
        delete_options[
            "Delete Label"
        ].tolist(),
    )


    selected_delete_row = (
        delete_options[
            delete_options["Delete Label"]
            == selected_delete_label
        ]
        .iloc[0]
    )


    selected_delete_id = (
        selected_delete_row["ID"]
    )


    confirm_delete = st.checkbox(
        "I understand that this transaction "
        "will be permanently deleted."
    )


    if st.button(
        "Delete Transaction",
        disabled=not confirm_delete,
    ):

        try:

            records = (
                worksheet.get_all_records()
            )

            sheet_row_number = None


            for row_number, record in enumerate(
                records,
                start=2,
            ):

                if str(
                    record.get(
                        "ID",
                        "",
                    )
                ).strip() == str(
                    selected_delete_id
                ).strip():

                    sheet_row_number = (
                        row_number
                    )

                    break


            if sheet_row_number is None:

                st.error(
                    f"Transaction "
                    f"#{int(selected_delete_id)} "
                    "could not be found."
                )

            else:

                worksheet.delete_rows(
                    sheet_row_number
                )

                load_expenses.clear()

                st.success(
                    f"Transaction "
                    f"#{int(selected_delete_id)} "
                    "deleted successfully!"
                )

                st.rerun()


        except Exception as e:

            st.error(
                "Unable to delete the transaction."
            )

            st.exception(e)
