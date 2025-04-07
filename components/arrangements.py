import streamlit as st
import pandas as pd
from datetime import datetime, date


def render_arrangements_page(data_manager):
    """Render the arrangements management page"""
    st.markdown(
        """<div class="card-title" style="display: flex; align-items: center;">
        <h1><svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px;">
          <path d="M10 1.5a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-1Zm-5 0A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5v1A1.5 1.5 0 0 1 9.5 4h-3A1.5 1.5 0 0 1 5 2.5v-1Zm-2 0h1v1A2.5 2.5 0 0 0 6.5 5h3A2.5 2.5 0 0 0 12 2.5v-1h1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-10a2 2 0 0 1 2-2Z"/>
          <path d="M4.5 8a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7Zm0 2.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7Z"/>
        </svg>
        Arrangements</H!>
    </div>""",
        unsafe_allow_html=True,
    )

    today = date.today()

    # Check if arrangements are suspended
    is_suspended = data_manager.is_arrangement_suspended(today)

    if is_suspended:
        st.warning("⚠️ Arrangements are currently suspended for today")

    # Create tabs for different arrangement views
    auto_tab, manual_tab = st.tabs(["Auto Arrangements", "Manual Arrangements"])

    with auto_tab:
        display_auto_arrangements(data_manager, today, is_suspended)

    with manual_tab:
        create_manual_arrangements(data_manager, today, is_suspended)


def display_auto_arrangements(data_manager, today, is_suspended):
    """Display automatically generated arrangements"""

    if is_suspended:
        st.warning("⚠️ Arrangements are currently suspended for today")
        return

    # Get today's absent teachers
    absent_teachers = data_manager.get_absent_teachers(str(today))
    if not absent_teachers:
        st.info("No absences marked for today")
        return

    st.subheader("Today's Arrangements")

    # Show current arrangements
    arrangements = data_manager.get_todays_arrangements()
    if not arrangements.empty:
        # Define custom formatting based on match quality
        def get_match_color(quality):
            if quality == "ideal":
                return "#28a745"  # Green
            elif quality == "acceptable":
                return "#ffc107"  # Yellow/Orange
            else:
                return "#dc3545"  # Red

        # Apply formatting to dataframe
        st.dataframe(
            arrangements,
            column_config={
                "absent_teacher": st.column_config.TextColumn("Absent Teacher"),
                "absent_category": st.column_config.TextColumn("Category"),
                "replacement_teacher": st.column_config.TextColumn(
                    "Replacement Teacher"
                ),
                "replacement_category": st.column_config.TextColumn("Category"),
                "class": st.column_config.TextColumn("Class"),
                "period": st.column_config.NumberColumn("Period"),
                "match_quality": st.column_config.TextColumn(
                    "Match Quality",
                    help="Indicates how well the replacement teacher matches the absent teacher's category",
                    width="medium",
                ),
                "status": st.column_config.TextColumn("Status"),
            },
            hide_index=True,
        )

        # Display explanation for match quality
        with st.expander("About Teacher Categories and Match Quality"):
            st.markdown(
                """
            ### Teacher Categories
            Teachers are categorized into three groups:
            - **PGT**: Post Graduate Teachers 
            - **TGT**: Trained Graduate Teachers
            - **PRT**: Primary Teachers
            
            ### Match Quality Criteria
            - **Ideal**: When replacement teacher is from the same category as the absent teacher
            - **Acceptable**: When a TGT replaces a PGT or when a PRT replaces a TGT
            - **Suboptimal**: Any other combination
            
            The system prioritizes finding replacements in the following order:
            1. Same category, same subject
            2. Same category, different subject
            3. Same subject, different category
            4. Any available teacher
            """
            )
    else:
        st.info("No arrangements have been made yet")


def create_manual_arrangements(data_manager, today, is_suspended):
    """Create manual arrangements for teachers (e.g., half-day leave)"""

    st.subheader("Create Manual Arrangement")
    st.markdown(
        """
    Use this form to create manual arrangements for specific periods, such as when a teacher takes half-day leave or 
    needs to be absent for specific periods only.
    """
    )

    # Get all teachers
    all_teachers = data_manager.get_all_teachers()
    if not all_teachers:
        st.error("No teachers found in the system.")
        return

    # Convert teacher list to dataframes for selection
    teacher_df = pd.DataFrame(all_teachers)

    # Define the periods
    periods = [1, 2, 3, 4, 5, 6, 7]

    # Setup the form for manual arrangement
    with st.form("manual_arrangement_form"):
        st.markdown("### Select Teachers and Period")

        col1, col2 = st.columns(2)

        with col1:
            # Absent Teacher Selection
            absent_teacher_options = [
                f"{t['name']} ({t['teacher_id']}) - {t.get('category', 'N/A')}"
                for t in all_teachers
            ]
            absent_teacher = st.selectbox(
                "Select Absent Teacher",
                options=absent_teacher_options,
                key="absent_teacher",
            )

            # Extract teacher ID from selection
            if absent_teacher:
                absent_teacher_id = absent_teacher.split("(")[1].split(")")[0]
            else:
                absent_teacher_id = None

            # Period Selection
            period = st.selectbox("Select Period", options=periods, key="period")

            # Class Selection
            class_name = st.text_input("Class Name/Section", key="class_name")

        with col2:
            # Replacement Teacher Selection
            replacement_options = [
                f"{t['name']} ({t['teacher_id']}) - {t.get('category', 'N/A')}"
                for t in all_teachers
                if t["teacher_id"] != absent_teacher_id
            ]
            replacement_teacher = st.selectbox(
                "Select Replacement Teacher",
                options=replacement_options,
                key="replacement_teacher",
            )

            # Extract teacher ID from selection
            if replacement_teacher:
                replacement_teacher_id = replacement_teacher.split("(")[1].split(")")[0]
            else:
                replacement_teacher_id = None

            # Optional date selection (defaults to today)
            use_different_date = st.checkbox("Use Different Date", value=False)
            if use_different_date:
                selected_date = st.date_input("Select Date", value=today)
            else:
                selected_date = today

        # Submit button
        submitted = st.form_submit_button("Create Arrangement")

        if submitted:
            if not absent_teacher_id or not replacement_teacher_id or not class_name:
                st.error("Please fill in all required fields.")
            else:
                # Create the manual arrangement
                success = data_manager.create_manual_arrangement(
                    absent_teacher_id,
                    replacement_teacher_id,
                    period,
                    class_name,
                    str(selected_date),
                )

                if success:
                    st.success(
                        f"Manual arrangement created successfully for period {period}."
                    )

                    # Show current arrangements including the new one
                    st.subheader("Current Arrangements")
                    all_arrangements = data_manager.get_todays_arrangements()
                    if not all_arrangements.empty:
                        st.dataframe(
                            all_arrangements,
                            column_config={
                                "absent_teacher": st.column_config.TextColumn(
                                    "Absent Teacher"
                                ),
                                "replacement_teacher": st.column_config.TextColumn(
                                    "Replacement Teacher"
                                ),
                                "class": st.column_config.TextColumn("Class"),
                                "period": st.column_config.NumberColumn("Period"),
                                "status": st.column_config.TextColumn("Status"),
                            },
                            hide_index=True,
                        )
                else:
                    st.error("Failed to create manual arrangement. Please try again.")
