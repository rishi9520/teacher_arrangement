import streamlit as st
import pandas as pd
from datetime import datetime, date
import os


def render_schedule_manager_page(data_manager):
    """Render the schedule management page"""
    st.markdown(
        """<div class="card-title">
            <h1><svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px;">
                <path d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm-3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm-5 3a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm3 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"/>
                <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
            </svg>
            Daily Schedule Viewer</h1>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("### View Teacher Schedules for Each Day of the Week")

    # Day selection
    day_names_dict = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
    }

    # Create tabs for each day
    tabs = st.tabs([day_names_dict[day] for day in range(6)])

    # Handle each tab (day)
    for day_idx, tab in enumerate(tabs):
        with tab:
            display_day_schedule(data_manager, day_idx, day_names_dict[day_idx])


def display_day_schedule(data_manager, day_idx, day_name):
    """Display schedule for a specific day"""
    st.subheader(f"{day_name} Schedule")

    # Get the file path for this day's schedule
    schedule_file = data_manager.schedule_files[day_idx]

    # Check if the file exists
    file_exists = os.path.exists(schedule_file)

    if file_exists:
        try:
            schedule_df = pd.read_csv(schedule_file)

            # Display the current schedule
            if not schedule_df.empty:
                st.dataframe(
                    schedule_df,
                    column_config={
                        "teacher_id": st.column_config.TextColumn("Teacher ID"),
                        "name": st.column_config.TextColumn("Name"),
                        "subject": st.column_config.TextColumn("Subject"),
                        "category": st.column_config.TextColumn("Category"),
                        "period1": st.column_config.TextColumn("Period 1"),
                        "period2": st.column_config.TextColumn("Period 2"),
                        "period3": st.column_config.TextColumn("Period 3"),
                        "period4": st.column_config.TextColumn("Period 4"),
                        "period5": st.column_config.TextColumn("Period 5"),
                        "period6": st.column_config.TextColumn("Period 6"),
                        "period7": st.column_config.TextColumn("Period 7"),
                    },
                    hide_index=True,
                )
            else:
                st.info(f"No schedule entries for {day_name} yet.")
        except Exception as e:
            st.error(f"Error loading {day_name} schedule: {str(e)}")
    else:
        st.warning(f"Schedule file for {day_name} does not exist yet.")

        # Try to show legacy schedule if available
        try:
            legacy_df = pd.read_csv(data_manager.schedules_file)
            if not legacy_df.empty:
                st.info("Showing legacy schedule (not day-specific):")
                st.dataframe(
                    legacy_df,
                    column_config={
                        "teacher_id": st.column_config.TextColumn("Teacher ID"),
                        "name": st.column_config.TextColumn("Name"),
                        "subject": st.column_config.TextColumn("Subject"),
                        "category": st.column_config.TextColumn("Category", default=""),
                        "period1": st.column_config.TextColumn("Period 1"),
                        "period2": st.column_config.TextColumn("Period 2"),
                        "period3": st.column_config.TextColumn("Period 3"),
                        "period4": st.column_config.TextColumn("Period 4"),
                        "period5": st.column_config.TextColumn("Period 5"),
                        "period6": st.column_config.TextColumn("Period 6"),
                        "period7": st.column_config.TextColumn("Period 7"),
                    },
                    hide_index=True,
                )
        except Exception:
            pass
