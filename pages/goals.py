import streamlit as st
import pandas as pd
from datetime import date

from utils.sheets import get_google_sheet


st.title("Goals")
st.caption("Create and track your financial goals")


# --------------------------------------------------
# GOOGLE SHEETS CONNECTION
# --------------------------------------------------

try:
    expenses_worksheet = get_google_sheet()
    spreadsheet = expenses_worksheet.spreadsheet

except Exception as e:
    st.error("Unable to connect to Google Sheets.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# GET OR CREATE FINANCIAL_GOALS WORKSHEET
# --------------------------------------------------

try:

    try:
        goals_worksheet = spreadsheet.worksheet("Financial_Goals")

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
    st.error("Unable to access Financial_Goals worksheet.")
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
# CREATE NEW GOAL
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
            "Current Saved Amount",
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

        st.error("Target amount must be greater than 0.")

    elif current_saved > target_amount:

        st.error(
            "Current saved amount cannot be greater than "
            "the target amount."
        )

    else:

        try:

            latest_records = goals_worksheet.get_all_records()

            existing_ids = []

            for record in latest_records:

                try:

                    existing_id = int(
                        float(record.get("Goal ID", 0))
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
                    target_date.strftime("%d/%m/%Y"),
                    date.today().strftime("%d/%m/%Y"),
                ]
            )

            st.success(
                f"Goal #{new_goal_id} created successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error("Unable to create the goal.")
            st.exception(e)


# --------------------------------------------------
# EXISTING GOALS
# --------------------------------------------------

st.divider()

st.subheader("Your Goals")


if goals_df.empty:

    st.info(
        "No financial goals created yet. "
        "Create your first goal above."
    )

    st.stop()


# --------------------------------------------------
# PREPARE DATA
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
# GOAL CARDS
# --------------------------------------------------

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
        target_amount - current_saved,
        0,
    )

    if target_amount > 0:

        progress = (
            current_saved / target_amount
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


    # --------------------------------------------------
    # STATUS
    # --------------------------------------------------

    if current_saved >= target_amount:

        st.success(
            "Completed — congratulations! 🎉"
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

                if current_saved > 0:

                    st.caption(
                        f"{days_remaining} days remaining"
                    )

            else:

                st.warning(
                    "Target date has passed. "
                    "Consider updating your goal."
                )

        except Exception:

            st.warning(
                "Unable to calculate goal timeline."
            )


    st.divider()


# --------------------------------------------------
# UPDATE GOAL
# --------------------------------------------------

st.subheader("Update Goal")

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
        float(selected_goal["Goal ID"])
    )

    selected_goal_name = str(
        selected_goal["Goal Name"]
    )

    selected_target = float(
        selected_goal["Target Amount"]
    )

    selected_saved = float(
        selected_goal["Current Saved"]
    )

    selected_target_date = pd.to_datetime(
        selected_goal["Target Date"],
        dayfirst=True,
    ).date()


    with st.form("update_goal_form"):

        updated_name = st.text_input(
            "Goal Name",
            value=selected_goal_name,
        )

        col1, col2 = st.columns(2)

        with col1:

            updated_target = st.number_input(
                "Target Amount",
                min_value=0.0,
                value=selected_target,
                step=1000.0,
                format="%.2f",
            )

        with col2:

            updated_saved = st.number_input(
                "Current Saved Amount",
                min_value=0.0,
                value=selected_saved,
                step=1000.0,
                format="%.2f",
            )

        updated_date = st.date_input(
            "Target Date",
            value=selected_target_date,
        )

        update_goal = st.form_submit_button(
            "Update Goal",
            type="primary",
        )


    if update_goal:

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
                        record.get("Goal ID", "")
                    ).strip() == str(
                        selected_goal_id
                    ).strip():

                        sheet_row_number = row_number
                        break


                if sheet_row_number is None:

                    st.error(
                        "Selected goal could not be found."
                    )

                else:

                    goals_worksheet.update(
                        f"A{sheet_row_number}:F{sheet_row_number}",
                        [[
                            selected_goal_id,
                            updated_name.strip(),
                            updated_target,
                            updated_saved,
                            updated_date.strftime(
                                "%d/%m/%Y"
                            ),
                            str(
                                selected_goal["Created Date"]
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
                record.get("Goal ID", "")
            ).strip() == str(
                selected_goal_id
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
