import streamlit as st
import pandas as pd
from datetime import date

from utils.sheets import get_google_sheet


st.title("Goals")
st.caption("Create, track and contribute towards your financial goals")


# --------------------------------------------------
# GOOGLE SHEETS
# --------------------------------------------------

try:

    expenses_worksheet = get_google_sheet()
    spreadsheet = expenses_worksheet.spreadsheet

except Exception as e:

    st.error("Unable to connect to Google Sheets.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# FINANCIAL_GOALS WORKSHEET
# --------------------------------------------------

try:

    try:

        goals_worksheet = spreadsheet.worksheet(
            "Financial_Goals"
        )

    except Exception:

        goals_worksheet = spreadsheet.add_worksheet(
            title="Financial_Goals",
            rows=1000,
            cols=10,
        )

        goals_worksheet.append_row(
            [
                "Goal ID",
                "Goal Name",
                "Target Amount",
                "Current Saved",
                "Target Date",
                "Created Date",
            ]
        )

except Exception as e:

    st.error(
        "Unable to access Financial_Goals worksheet."
    )

    st.exception(e)
    st.stop()


# --------------------------------------------------
# CONTRIBUTIONS WORKSHEET
# --------------------------------------------------

try:

    try:

        contributions_worksheet = spreadsheet.worksheet(
            "Goal_Contributions"
        )

    except Exception:

        contributions_worksheet = spreadsheet.add_worksheet(
            title="Goal_Contributions",
            rows=2000,
            cols=10,
        )

        contributions_worksheet.append_row(
            [
                "Contribution ID",
                "Goal ID",
                "Goal Name",
                "Date",
                "Amount",
                "Note",
            ]
        )

except Exception as e:

    st.error(
        "Unable to access Goal_Contributions worksheet."
    )

    st.exception(e)
    st.stop()


# --------------------------------------------------
# LOAD GOALS
# --------------------------------------------------

try:

    records = goals_worksheet.get_all_records()

    goals_df = pd.DataFrame(records)

except Exception as e:

    st.error("Unable to load financial goals.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# CREATE GOAL
# --------------------------------------------------

st.subheader("Create New Goal")

with st.form("create_goal_form"):

    goal_name = st.text_input(
        "Goal Name",
        placeholder="Example: Emergency Fund",
    )

    col1, col2 = st.columns(2)

    with col1:

        target_amount = st.number_input(
            "Target Amount",
            min_value=0.0,
            step=1000.0,
            format="%.2f",
        )

    with col2:

        current_saved = st.number_input(
            "Starting Saved Amount",
            min_value=0.0,
            step=1000.0,
            format="%.2f",
        )

    target_date = st.date_input(
        "Target Date",
        value=date.today(),
        min_value=date.today(),
    )

    create_goal = st.form_submit_button(
        "Create Goal",
        type="primary",
    )


if create_goal:

    if not goal_name.strip():

        st.error("Please enter a goal name.")

    elif target_amount <= 0:

        st.error(
            "Target amount must be greater than 0."
        )

    elif current_saved > target_amount:

        st.error(
            "Starting saved amount cannot be greater "
            "than the target amount."
        )

    else:

        try:

            latest_records = (
                goals_worksheet.get_all_records()
            )

            existing_ids = []

            for record in latest_records:

                try:

                    existing_id = int(
                        float(
                            record.get(
                                "Goal ID",
                                0,
                            )
                        )
                    )

                    existing_ids.append(existing_id)

                except (ValueError, TypeError):

                    pass


            if existing_ids:

                new_goal_id = max(existing_ids) + 1

            else:

                new_goal_id = 1


            goals_worksheet.append_row(
                [
                    new_goal_id,
                    goal_name.strip(),
                    target_amount,
                    current_saved,
                    target_date.strftime(
                        "%d/%m/%Y"
                    ),
                    date.today().strftime(
                        "%d/%m/%Y"
                    ),
                ]
            )


            st.success(
                f"Goal #{new_goal_id} created successfully!"
            )

            st.rerun()


        except Exception as e:

            st.error(
                "Unable to create the goal."
            )

            st.exception(e)


# --------------------------------------------------
# LOAD GOALS AGAIN
# --------------------------------------------------

try:

    records = goals_worksheet.get_all_records()

    goals_df = pd.DataFrame(records)

except Exception as e:

    st.error("Unable to refresh goals.")
    st.exception(e)
    st.stop()


if goals_df.empty:

    st.divider()

    st.info(
        "No financial goals created yet. "
        "Create your first goal above."
    )

    st.stop()


# --------------------------------------------------
# PREPARE GOALS DATA
# --------------------------------------------------

goals_df["Target Amount"] = pd.to_numeric(
    goals_df["Target Amount"],
    errors="coerce",
).fillna(0)

goals_df["Current Saved"] = pd.to_numeric(
    goals_df["Current Saved"],
    errors="coerce",
).fillna(0)


# --------------------------------------------------
# ADD CONTRIBUTION
# --------------------------------------------------

st.divider()

st.subheader("Add Goal Contribution")

st.caption(
    "Record money saved towards a specific financial goal."
)


goal_options = []

for _, goal in goals_df.iterrows():

    goal_options.append(
        f"#{int(float(goal['Goal ID']))} | "
        f"{goal['Goal Name']}"
    )


selected_goal_label = st.selectbox(
    "Select Goal",
    goal_options,
)


selected_goal = None

for _, goal in goals_df.iterrows():

    label = (
        f"#{int(float(goal['Goal ID']))} | "
        f"{goal['Goal Name']}"
    )

    if label == selected_goal_label:

        selected_goal = goal
        break


if selected_goal is not None:

    selected_goal_id = int(
        float(
            selected_goal["Goal ID"]
        )
    )

    selected_goal_name = str(
        selected_goal["Goal Name"]
    )

    selected_target = float(
        selected_goal["Target Amount"]
    )

    selected_current_saved = float(
        selected_goal["Current Saved"]
    )

    remaining_before_contribution = max(
        selected_target
        - selected_current_saved,
        0,
    )


    st.info(
        f"Current saved: ₹{selected_current_saved:,.2f} "
        f"• Remaining: ₹{remaining_before_contribution:,.2f}"
    )


    with st.form("contribution_form"):

        contribution_date = st.date_input(
            "Contribution Date",
            value=date.today(),
        )

        contribution_amount = st.number_input(
            "Contribution Amount",
            min_value=0.0,
            step=500.0,
            format="%.2f",
        )

        contribution_note = st.text_input(
            "Note",
            placeholder="Example: Monthly savings",
        )

        add_contribution = st.form_submit_button(
            "Add Contribution",
            type="primary",
        )


    if add_contribution:

        if contribution_amount <= 0:

            st.error(
                "Contribution amount must be greater than 0."
            )

        elif selected_current_saved >= selected_target:

            st.warning(
                "This goal is already completed."
            )

        else:

            remaining_amount = (
                selected_target
                - selected_current_saved
            )

            if contribution_amount > remaining_amount:

                st.error(
                    f"Maximum possible contribution is "
                    f"₹{remaining_amount:,.2f}."
                )

            else:

                try:

                    # ----------------------------------
                    # GET NEW CONTRIBUTION ID
                    # ----------------------------------

                    contribution_records = (
                        contributions_worksheet
                        .get_all_records()
                    )

                    existing_contribution_ids = []

                    for record in contribution_records:

                        try:

                            contribution_id = int(
                                float(
                                    record.get(
                                        "Contribution ID",
                                        0,
                                    )
                                )
                            )

                            existing_contribution_ids.append(
                                contribution_id
                            )

                        except (
                            ValueError,
                            TypeError,
                        ):

                            pass


                    if existing_contribution_ids:

                        new_contribution_id = (
                            max(
                                existing_contribution_ids
                            )
                            + 1
                        )

                    else:

                        new_contribution_id = 1


                    # ----------------------------------
                    # SAVE CONTRIBUTION
                    # ----------------------------------

                    contributions_worksheet.append_row(
                        [
                            new_contribution_id,
                            selected_goal_id,
                            selected_goal_name,
                            contribution_date.strftime(
                                "%d/%m/%Y"
                            ),
                            contribution_amount,
                            contribution_note.strip(),
                        ]
                    )


                    # ----------------------------------
                    # FIND GOAL ROW
                    # ----------------------------------

                    latest_goal_records = (
                        goals_worksheet
                        .get_all_records()
                    )

                    goal_sheet_row = None

                    for row_number, record in enumerate(
                        latest_goal_records,
                        start=2,
                    ):

                        if str(
                            record.get(
                                "Goal ID",
                                "",
                            )
                        ).strip() == str(
                            selected_goal_id
                        ).strip():

                            goal_sheet_row = row_number
                            break


                    if goal_sheet_row is None:

                        st.error(
                            "Goal could not be found."
                        )

                    else:

                        # ------------------------------
                        # UPDATE CURRENT SAVED
                        # ------------------------------

                        new_current_saved = (
                            selected_current_saved
                            + contribution_amount
                        )


                        goals_worksheet.update(
                            f"D{goal_sheet_row}",
                            [[
                                new_current_saved
                            ]],
                        )


                        # ------------------------------
                        # SUCCESS
                        # ------------------------------

                        st.success(
                            f"₹{contribution_amount:,.2f} "
                            f"added to {selected_goal_name}!"
                        )

                        st.info(
                            f"New saved amount: "
                            f"₹{new_current_saved:,.2f}"
                        )

                        st.rerun()


                except Exception as e:

                    st.error(
                        "Unable to save the contribution."
                    )

                    st.exception(e)


# --------------------------------------------------
# YOUR GOALS
# --------------------------------------------------

st.divider()

st.subheader("Your Goals")


for _, goal in goals_df.iterrows():

    goal_id = goal["Goal ID"]

    goal_name = str(
        goal["Goal Name"]
    )

    target_amount = float(
        goal["Target Amount"]
    )

    current_saved = float(
        goal["Current Saved"]
    )

    target_date_text = str(
        goal["Target Date"]
    )


    remaining_amount = max(
        target_amount
        - current_saved,
        0,
    )


    if target_amount > 0:

        progress = (
            current_saved
            / target_amount
        )

        progress = min(
            max(progress, 0),
            1,
        )

    else:

        progress = 0


    st.markdown(
        f"### {goal_name}"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Target",
            f"₹{target_amount:,.2f}",
        )


    with col2:

        st.metric(
            "Saved",
            f"₹{current_saved:,.2f}",
        )


    with col3:

        st.metric(
            "Remaining",
            f"₹{remaining_amount:,.2f}",
        )


    st.progress(
        progress,
        text=f"{progress * 100:.1f}% completed",
    )


    st.caption(
        f"Target Date: {target_date_text}"
    )


    if current_saved >= target_amount:

        st.success(
            "Completed — congratulations!"
        )

    else:

        try:

            target_date_value = pd.to_datetime(
                target_date_text,
                dayfirst=True,
            ).date()

            today = date.today()

            days_remaining = (
                target_date_value - today
            ).days

            if days_remaining > 0:

                months_remaining = max(
                    days_remaining / 30.44,
                    1,
                )

                required_monthly_saving = (
                    remaining_amount
                    / months_remaining
                )

                st.info(
                    f"Required monthly saving: "
                    f"₹{required_monthly_saving:,.2f}"
                )

                st.caption(
                    f"{days_remaining} days remaining"
                )

            else:

                st.warning(
                    "Target date has passed."
                )

        except Exception:

            st.warning(
                "Unable to calculate goal timeline."
            )


    st.divider()


# --------------------------------------------------
# CONTRIBUTION HISTORY
# --------------------------------------------------

st.subheader("Contribution History")


try:

    contribution_records = (
        contributions_worksheet
        .get_all_records()
    )

    contributions_df = pd.DataFrame(
        contribution_records
    )

except Exception:

    contributions_df = pd.DataFrame()


if contributions_df.empty:

    st.info(
        "No goal contributions recorded yet."
    )

else:

    contributions_df["Amount"] = pd.to_numeric(
        contributions_df["Amount"],
        errors="coerce",
    ).fillna(0)


    display_columns = [
        "Date",
        "Goal Name",
        "Amount",
        "Note",
    ]


    available_columns = [
        column
        for column in display_columns
        if column in contributions_df.columns
    ]


    history_df = contributions_df[
        available_columns
    ].copy()


    st.dataframe(
        history_df.sort_index(
            ascending=False
        ),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": "Date",
            "Goal Name": "Goal",
            "Amount": st.column_config.NumberColumn(
                "Amount",
                format="₹%.2f",
            ),
            "Note": "Note",
        },
    )


# --------------------------------------------------
# UPDATE GOAL
# --------------------------------------------------

st.divider()

st.subheader("Update Goal")


update_goal_label = st.selectbox(
    "Select Goal to Update",
    goal_options,
    key="update_goal_selector",
)


update_goal = None

for _, goal in goals_df.iterrows():

    label = (
        f"#{int(float(goal['Goal ID']))} | "
        f"{goal['Goal Name']}"
    )

    if label == update_goal_label:

        update_goal = goal
        break


if update_goal is not None:

    update_goal_id = int(
        float(update_goal["Goal ID"])
    )

    update_name = str(
        update_goal["Goal Name"]
    )

    update_target = float(
        update_goal["Target Amount"]
    )

    update_saved = float(
        update_goal["Current Saved"]
    )

    update_date = pd.to_datetime(
        update_goal["Target Date"],
        dayfirst=True,
    ).date()


    with st.form("update_goal_form"):

        updated_name = st.text_input(
            "Goal Name",
            value=update_name,
        )

        col1, col2 = st.columns(2)

        with col1:

            updated_target = st.number_input(
                "Target Amount",
                min_value=0.0,
                value=update_target,
                step=1000.0,
                format="%.2f",
            )

        with col2:

            updated_saved = st.number_input(
                "Current Saved Amount",
                min_value=0.0,
                value=update_saved,
                step=1000.0,
                format="%.2f",
            )

        updated_date = st.date_input(
            "Target Date",
            value=update_date,
        )

        save_update = st.form_submit_button(
            "Update Goal",
            type="primary",
        )


    if save_update:

        if not updated_name.strip():

            st.error(
                "Please enter a goal name."
            )

        elif updated_target <= 0:

            st.error(
                "Target amount must be greater than 0."
            )

        elif updated_saved > updated_target:

            st.error(
                "Current saved amount cannot be greater "
                "than the target amount."
            )

        else:

            try:

                latest_records = (
                    goals_worksheet.get_all_records()
                )

                sheet_row_number = None

                for row_number, record in enumerate(
                    latest_records,
                    start=2,
                ):

                    if str(
                        record.get(
                            "Goal ID",
                            "",
                        )
                    ).strip() == str(
                        update_goal_id
                    ).strip():

                        sheet_row_number = row_number
                        break


                if sheet_row_number is None:

                    st.error(
                        "Goal could not be found."
                    )

                else:

                    goals_worksheet.update(
                        f"A{sheet_row_number}:F{sheet_row_number}",
                        [[
                            update_goal_id,
                            updated_name.strip(),
                            updated_target,
                            updated_saved,
                            updated_date.strftime(
                                "%d/%m/%Y"
                            ),
                            str(
                                update_goal["Created Date"]
                            ),
                        ]],
                    )

                    st.success(
                        "Goal updated successfully!"
                    )

                    st.rerun()


            except Exception as e:

                st.error(
                    "Unable to update the goal."
                )

                st.exception(e)


# --------------------------------------------------
# DELETE GOAL
# --------------------------------------------------

st.divider()

st.subheader("Delete Goal")

st.warning(
    "Deleting a goal will permanently remove it "
    "from your Google Sheet."
)


delete_goal_label = st.selectbox(
    "Select Goal to Delete",
    goal_options,
    key="delete_goal_selector",
)


delete_goal_id = None

for _, goal in goals_df.iterrows():

    label = (
        f"#{int(float(goal['Goal ID']))} | "
        f"{goal['Goal Name']}"
    )

    if label == delete_goal_label:

        delete_goal_id = int(
            float(goal["Goal ID"])
        )

        break


confirm_delete = st.checkbox(
    "I understand that this goal will be permanently deleted."
)


if st.button(
    "Delete Goal",
    disabled=not confirm_delete,
):

    try:

        latest_records = (
            goals_worksheet.get_all_records()
        )

        sheet_row_number = None

        for row_number, record in enumerate(
            latest_records,
            start=2,
        ):

            if str(
                record.get(
                    "Goal ID",
                    "",
                )
            ).strip() == str(
                delete_goal_id
            ).strip():

                sheet_row_number = row_number
                break


        if sheet_row_number is None:

            st.error(
                "Goal could not be found."
            )

        else:

            goals_worksheet.delete_rows(
                sheet_row_number
            )

            st.success(
                "Goal deleted successfully!"
            )

            st.rerun()


    except Exception as e:

        st.error(
            "Unable to delete the goal."
        )

        st.exception(e)
