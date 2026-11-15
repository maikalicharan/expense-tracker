import streamlit as st
import pandas as pd
from datetime import date

from utils.sheets import get_google_sheet
from utils.data import load_expenses


st.set_page_config(
    page_title="Goals",
    layout="wide",
)


st.title("Goals")
st.caption(
    "Create, track and fund your financial goals"
)


# ==================================================
# GOOGLE SHEET SETUP
# ==================================================

try:

    worksheet = get_google_sheet()
    spreadsheet = worksheet.spreadsheet

except Exception as e:

    st.error(
        "Unable to connect to Google Sheets."
    )

    st.exception(e)

    st.stop()


# ==================================================
# GET OR CREATE WORKSHEETS
# ==================================================

try:

    try:

        goals_worksheet = spreadsheet.worksheet(
            "Financial_Goals"
        )

    except Exception:

        goals_worksheet = spreadsheet.add_worksheet(
            title="Financial_Goals",
            rows=1000,
            cols=6,
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


    try:

        contributions_worksheet = spreadsheet.worksheet(
            "Goal_Contributions"
        )

    except Exception:

        contributions_worksheet = spreadsheet.add_worksheet(
            title="Goal_Contributions",
            rows=2000,
            cols=6,
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
        "Unable to prepare goal worksheets."
    )

    st.exception(e)

    st.stop()


# ==================================================
# LOAD GOALS
# ==================================================

try:

    goals_records = (
        goals_worksheet.get_all_records()
    )

    goals_df = pd.DataFrame(
        goals_records
    )

except Exception as e:

    st.error(
        "Unable to load financial goals."
    )

    st.exception(e)

    st.stop()


# ==================================================
# LOAD CONTRIBUTIONS
# ==================================================

try:

    contribution_records = (
        contributions_worksheet.get_all_records()
    )

    contributions_df = pd.DataFrame(
        contribution_records
    )

except Exception as e:

    st.error(
        "Unable to load goal contributions."
    )

    st.exception(e)

    st.stop()


# ==================================================
# NORMALIZE GOALS DATA
# ==================================================

if not goals_df.empty:

    goals_df["Goal ID"] = pd.to_numeric(
        goals_df["Goal ID"],
        errors="coerce",
    )

    goals_df["Target Amount"] = pd.to_numeric(
        goals_df["Target Amount"],
        errors="coerce",
    ).fillna(0)

    goals_df["Current Saved"] = pd.to_numeric(
        goals_df["Current Saved"],
        errors="coerce",
    ).fillna(0)

    goals_df["Target Date"] = pd.to_datetime(
        goals_df["Target Date"],
        errors="coerce",
    )

    goals_df["Goal Name"] = (
        goals_df["Goal Name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ==================================================
# NORMALIZE CONTRIBUTION DATA
# ==================================================

if not contributions_df.empty:

    contributions_df["Contribution ID"] = (
        pd.to_numeric(
            contributions_df["Contribution ID"],
            errors="coerce",
        )
    )

    contributions_df["Goal ID"] = (
        pd.to_numeric(
            contributions_df["Goal ID"],
            errors="coerce",
        )
    )

    contributions_df["Amount"] = (
        pd.to_numeric(
            contributions_df["Amount"],
            errors="coerce",
        )
        .fillna(0)
        .abs()
    )

    contributions_df["Date"] = pd.to_datetime(
        contributions_df["Date"],
        errors="coerce",
    )


# ==================================================
# LOAD TRANSACTION DATA
# ==================================================

try:

    expenses_df = load_expenses()

except Exception:

    expenses_df = pd.DataFrame()


# ==================================================
# AVAILABLE SAVINGS CALCULATION
# ==================================================

available_savings = 0.0


if not expenses_df.empty:

    total_income = expenses_df.loc[
        expenses_df["Type"] == "Income",
        "Amount",
    ].sum()

    total_expenses = expenses_df.loc[
        expenses_df["Type"] == "Expense",
        "Expense Amount",
    ].sum()

    available_savings = (
        total_income
        - total_expenses
    )


# ==================================================
# HEADER SUMMARY
# ==================================================

if goals_df.empty:

    active_goals_count = 0
    completed_goals_count = 0
    total_target_amount = 0.0
    total_saved_amount = 0.0
    total_remaining_amount = 0.0

else:

    goals_df["Remaining"] = (
        goals_df["Target Amount"]
        - goals_df["Current Saved"]
    ).clip(lower=0)

    active_goals = goals_df[
        goals_df["Remaining"] > 0
    ]

    completed_goals = goals_df[
        goals_df["Remaining"] <= 0
    ]

    active_goals_count = len(
        active_goals
    )

    completed_goals_count = len(
        completed_goals
    )

    total_target_amount = (
        goals_df["Target Amount"].sum()
    )

    total_saved_amount = (
        goals_df["Current Saved"].sum()
    )

    total_remaining_amount = (
        goals_df["Remaining"].sum()
    )


st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Active Goals",
        active_goals_count,
    )


with col2:

    st.metric(
        "Completed Goals",
        completed_goals_count,
    )


with col3:

    st.metric(
        "Total Saved",
        f"₹{total_saved_amount:,.2f}",
    )


with col4:

    st.metric(
        "Total Remaining",
        f"₹{total_remaining_amount:,.2f}",
    )


# ==================================================
# CREATE NEW GOAL
# ==================================================

st.divider()

st.subheader("Create New Goal")


with st.form(
    "create_goal_form"
):

    goal_name = st.text_input(
        "Goal Name",
        placeholder="Example: Emergency Fund",
    )

    target_amount = st.number_input(
        "Target Amount",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
    )

    initial_saved = st.number_input(
        "Already Saved",
        min_value=0.0,
        step=500.0,
        format="%.2f",
        help=(
            "Amount you have already saved toward this goal."
        ),
    )

    target_date = st.date_input(
        "Target Date",
        min_value=date.today(),
    )

    create_goal = st.form_submit_button(
        "Create Goal",
        type="primary",
        use_container_width=True,
    )


if create_goal:

    cleaned_goal_name = goal_name.strip()


    if not cleaned_goal_name:

        st.error(
            "Please enter a goal name."
        )

        st.stop()


    if target_amount <= 0:

        st.error(
            "Target amount must be greater than zero."
        )

        st.stop()


    if initial_saved < 0:

        st.error(
            "Already Saved cannot be negative."
        )

        st.stop()


    if initial_saved > target_amount:

        st.error(
            "Already Saved cannot be greater "
            "than the Target Amount."
        )

        st.stop()


    try:

        existing_ids = []

        if not goals_df.empty:

            existing_ids = (
                goals_df["Goal ID"]
                .dropna()
                .astype(int)
                .tolist()
            )


        if existing_ids:

            new_goal_id = (
                max(existing_ids) + 1
            )

        else:

            new_goal_id = 1


        goals_worksheet.append_row(
            [
                new_goal_id,
                cleaned_goal_name,
                float(target_amount),
                float(initial_saved),
                target_date.strftime(
                    "%d/%m/%Y"
                ),
                date.today().strftime(
                    "%d/%m/%Y"
                ),
            ]
        )


        # ------------------------------------------
        # RECORD INITIAL SAVING AS CONTRIBUTION
        # ------------------------------------------

        if initial_saved > 0:

            existing_contribution_ids = []

            if not contributions_df.empty:

                existing_contribution_ids = (
                    contributions_df[
                        "Contribution ID"
                    ]
                    .dropna()
                    .astype(int)
                    .tolist()
                )


            if existing_contribution_ids:

                new_contribution_id = (
                    max(
                        existing_contribution_ids
                    ) + 1
                )

            else:

                new_contribution_id = 1


            contributions_worksheet.append_row(
                [
                    new_contribution_id,
                    new_goal_id,
                    cleaned_goal_name,
                    date.today().strftime(
                        "%d/%m/%Y"
                    ),
                    float(initial_saved),
                    "Initial saved amount",
                ]
            )


        st.success(
            f"Goal '{cleaned_goal_name}' "
            "created successfully!"
        )

        st.rerun()


    except Exception as e:

        st.error(
            "Unable to create the goal."
        )

        st.exception(e)


# ==================================================
# ACTIVE GOALS
# ==================================================

st.divider()

st.subheader("Your Goals")


if goals_df.empty:

    st.info(
        "No goals created yet. "
        "Create your first financial goal above."
    )

else:

    for _, goal in goals_df.iterrows():

        goal_id = int(
            goal["Goal ID"]
        )

        goal_name = str(
            goal["Goal Name"]
        )

        target_amount = float(
            goal["Target Amount"]
        )

        current_saved = float(
            goal["Current Saved"]
        )

        remaining = max(
            target_amount
            - current_saved,
            0,
        )


        if target_amount > 0:

            progress = (
                current_saved
                / target_amount
            )

            progress = max(
                0,
                min(
                    progress,
                    1,
                )
            )

        else:

            progress = 0


        target_date_value = (
            goal["Target Date"]
        )


        if pd.notna(
            target_date_value
        ):

            target_date_text = (
                target_date_value.strftime(
                    "%d/%m/%Y"
                )
            )

        else:

            target_date_text = (
                "Not specified"
            )


        if remaining <= 0:

            status = "Completed"

        else:

            status = "Active"


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
                f"₹{remaining:,.2f}",
            )


        st.progress(
            progress
        )


        st.caption(
            f"Progress: {progress * 100:.1f}% "
            f"• Target Date: {target_date_text} "
            f"• Status: {status}"
        )


        # ------------------------------------------
        # REQUIRED MONTHLY SAVING
        # ------------------------------------------

        if (
            remaining > 0
            and
            pd.notna(target_date_value)
        ):

            today = pd.Timestamp.today().normalize()


            months_remaining = (
                (
                    target_date_value.year
                    - today.year
                )
                * 12
                +
                (
                    target_date_value.month
                    - today.month
                )
            )


            if months_remaining <= 0:

                months_remaining = 1


            required_monthly_saving = (
                remaining
                / months_remaining
            )


            st.caption(
                f"Required monthly saving: "
                f"₹{required_monthly_saving:,.2f}"
            )


        if status == "Completed":

            st.success(
                "Goal completed!"
            )


        # ==================================================
        # ADD CONTRIBUTION
        # ==================================================

        if remaining > 0:

            with st.expander(
                f"Add Contribution — {goal_name}"
            ):

                st.info(
                    f"Available savings: "
                    f"₹{max(available_savings, 0):,.2f}"
                )


                with st.form(
                    f"contribution_form_{goal_id}"
                ):

                    contribution_amount = (
                        st.number_input(
                            "Contribution Amount",
                            min_value=0.0,
                            step=500.0,
                            format="%.2f",
                        )
                    )


                    contribution_date = (
                        st.date_input(
                            "Date",
                            value=date.today(),
                        )
                    )


                    contribution_note = (
                        st.text_input(
                            "Note",
                            placeholder=(
                                "Example: Monthly goal saving"
                            ),
                        )
                    )


                    add_contribution = (
                        st.form_submit_button(
                            "Add Contribution",
                            type="primary",
                            use_container_width=True,
                        )
                    )


                if add_contribution:

                    if contribution_amount <= 0:

                        st.error(
                            "Contribution amount must "
                            "be greater than zero."
                        )

                    elif contribution_amount > remaining:

                        st.error(
                            f"Contribution cannot be greater "
                            f"than the remaining goal amount "
                            f"of ₹{remaining:,.2f}."
                        )

                    elif (
                        available_savings > 0
                        and
                        contribution_amount
                        > available_savings
                    ):

                        st.error(
                            f"Contribution cannot be greater "
                            f"than your available savings "
                            f"of ₹{available_savings:,.2f}."
                        )

                    elif available_savings <= 0:

                        st.error(
                            "You currently do not have "
                            "positive available savings "
                            "based on your transactions."
                        )

                    else:

                        try:

                            # ----------------------------------
                            # CONTRIBUTION ID
                            # ----------------------------------

                            existing_ids = []

                            if not contributions_df.empty:

                                existing_ids = (
                                    contributions_df[
                                        "Contribution ID"
                                    ]
                                    .dropna()
                                    .astype(int)
                                    .tolist()
                                )


                            if existing_ids:

                                new_contribution_id = (
                                    max(
                                        existing_ids
                                    ) + 1
                                )

                            else:

                                new_contribution_id = 1


                            # ----------------------------------
                            # ADD CONTRIBUTION
                            # ----------------------------------

                            contributions_worksheet.append_row(
                                [
                                    new_contribution_id,
                                    goal_id,
                                    goal_name,
                                    contribution_date.strftime(
                                        "%d/%m/%Y"
                                    ),
                                    float(
                                        contribution_amount
                                    ),
                                    contribution_note.strip(),
                                ]
                            )


                            # ----------------------------------
                            # UPDATE GOAL SAVED AMOUNT
                            # ----------------------------------

                            new_current_saved = (
                                current_saved
                                + contribution_amount
                            )


                            records = (
                                goals_worksheet
                                .get_all_records()
                            )


                            goal_row_number = None


                            for row_number, record in enumerate(
                                records,
                                start=2,
                            ):

                                if str(
                                    record.get(
                                        "Goal ID",
                                        "",
                                    )
                                ).strip() == str(
                                    goal_id
                                ).strip():

                                    goal_row_number = (
                                        row_number
                                    )

                                    break


                            if goal_row_number is None:

                                st.error(
                                    "Goal could not be found."
                                )

                                st.stop()


                            goals_worksheet.update(
                                f"D{goal_row_number}",
                                [
                                    [
                                        float(
                                            new_current_saved
                                        )
                                    ]
                                ],
                            )


                            st.success(
                                f"₹{contribution_amount:,.2f} "
                                "contribution added successfully!"
                            )


                            st.rerun()


                        except Exception as e:

                            st.error(
                                "Unable to add the contribution."
                            )

                            st.exception(e)


        # ==================================================
        # CONTRIBUTION HISTORY
        # ==================================================

        goal_contributions = pd.DataFrame()


        if not contributions_df.empty:

            goal_contributions = (
                contributions_df[
                    contributions_df["Goal ID"]
                    == goal_id
                ]
                .sort_values(
                    "Date",
                    ascending=False,
                )
                .copy()
            )


        if not goal_contributions.empty:

            with st.expander(
                f"Contribution History — {goal_name}"
            ):

                contribution_display = (
                    goal_contributions.copy()
                )


                contribution_display["Date"] = (
                    contribution_display["Date"]
                    .dt.strftime("%d/%m/%Y")
                )


                contribution_display["Amount"] = (
                    contribution_display["Amount"]
                    .abs()
                )


                contribution_display = (
                    contribution_display[
                        [
                            "Date",
                            "Amount",
                            "Note",
                        ]
                    ]
                )


                st.dataframe(
                    contribution_display,
                    use_container_width=True,
                    hide_index=True,
                    column_config={

                        "Date":
                            st.column_config.TextColumn(
                                "Date"
                            ),

                        "Amount":
                            st.column_config.NumberColumn(
                                "Amount",
                                format="₹%.2f",
                            ),

                        "Note":
                            st.column_config.TextColumn(
                                "Note"
                            ),
                    },
                )


        # ==================================================
        # UPDATE GOAL
        # ==================================================

        with st.expander(
            f"Update Goal — {goal_name}"
        ):

            with st.form(
                f"update_goal_form_{goal_id}"
            ):

                updated_name = st.text_input(
                    "Goal Name",
                    value=goal_name,
                )


                updated_target = st.number_input(
                    "Target Amount",
                    min_value=0.0,
                    value=float(
                        target_amount
                    ),
                    step=1000.0,
                    format="%.2f",
                )


                updated_target_date = (
                    st.date_input(
                        "Target Date",
                        value=(
                            target_date_value.date()
                            if pd.notna(
                                target_date_value
                            )
                            else date.today()
                        ),
                    )
                )


                update_goal = st.form_submit_button(
                    "Save Goal Changes",
                    type="primary",
                    use_container_width=True,
                )


            if update_goal:

                cleaned_name = (
                    updated_name.strip()
                )


                if not cleaned_name:

                    st.error(
                        "Goal name cannot be blank."
                    )

                elif updated_target <= 0:

                    st.error(
                        "Target amount must be "
                        "greater than zero."
                    )

                elif current_saved > updated_target:

                    st.error(
                        "Target amount cannot be less "
                        "than the amount already saved."
                    )

                else:

                    try:

                        records = (
                            goals_worksheet
                            .get_all_records()
                        )


                        goal_row_number = None


                        for row_number, record in enumerate(
                            records,
                            start=2,
                        ):

                            if str(
                                record.get(
                                    "Goal ID",
                                    "",
                                )
                            ).strip() == str(
                                goal_id
                            ).strip():

                                goal_row_number = (
                                    row_number
                                )

                                break


                        if goal_row_number is None:

                            st.error(
                                "Goal could not be found."
                            )

                        else:

                            goals_worksheet.update(
                                f"B{goal_row_number}:E{goal_row_number}",
                                [[
                                    cleaned_name,
                                    float(
                                        updated_target
                                    ),
                                    float(
                                        current_saved
                                    ),
                                    updated_target_date.strftime(
                                        "%d/%m/%Y"
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


        # ==================================================
        # DELETE GOAL
        # ==================================================

        with st.expander(
            f"Delete Goal — {goal_name}"
        ):

            st.warning(
                "Deleting this goal will also delete "
                "its contribution history."
            )


            confirm_delete_goal = st.checkbox(
                "I understand that this goal "
                "and its contribution history "
                "will be permanently deleted.",
                key=f"confirm_delete_{goal_id}",
            )


            if st.button(
                "Delete Goal",
                key=f"delete_goal_{goal_id}",
                disabled=not confirm_delete_goal,
            ):

                try:

                    # ----------------------------------
                    # FIND GOAL ROW
                    # ----------------------------------

                    records = (
                        goals_worksheet
                        .get_all_records()
                    )


                    goal_row_number = None


                    for row_number, record in enumerate(
                        records,
                        start=2,
                    ):

                        if str(
                            record.get(
                                "Goal ID",
                                "",
                            )
                        ).strip() == str(
                            goal_id
                        ).strip():

                            goal_row_number = (
                                row_number
                            )

                            break


                    if goal_row_number is None:

                        st.error(
                            "Goal could not be found."
                        )

                        st.stop()


                    # ----------------------------------
                    # DELETE GOAL
                    # ----------------------------------

                    goals_worksheet.delete_rows(
                        goal_row_number
                    )


                    # ----------------------------------
                    # DELETE CONTRIBUTIONS
                    # ----------------------------------

                    contribution_records = (
                        contributions_worksheet
                        .get_all_records()
                    )


                    contribution_rows_to_delete = []


                    for row_number, record in enumerate(
                        contribution_records,
                        start=2,
                    ):

                        if str(
                            record.get(
                                "Goal ID",
                                "",
                            )
                        ).strip() == str(
                            goal_id
                        ).strip():

                            contribution_rows_to_delete.append(
                                row_number
                            )


                    for row_number in reversed(
                        contribution_rows_to_delete
                    ):

                        contributions_worksheet.delete_rows(
                            row_number
                        )


                    st.success(
                        f"Goal '{goal_name}' "
                        "deleted successfully!"
                    )


                    st.rerun()


                except Exception as e:

                    st.error(
                        "Unable to delete the goal."
                    )

                    st.exception(e)


        st.divider()


# ==================================================
# GOAL FUNDING SUMMARY
# ==================================================

if not goals_df.empty:

    st.subheader(
        "Goal Funding Summary"
    )


    if available_savings > 0:

        st.info(
            f"Current available savings from your "
            f"transactions: ₹{available_savings:,.2f}"
        )

    else:

        st.warning(
            "Your current transaction history does not "
            "show positive available savings."
        )


    if total_remaining_amount > 0:

        st.write(
            f"Total amount still needed across active goals: "
            f"**₹{total_remaining_amount:,.2f}**"
        )

    else:

        st.success(
            "All current financial goals are completed."
        )
