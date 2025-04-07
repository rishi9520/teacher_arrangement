import streamlit as st
from datetime import datetime, date
import pandas as pd


def render_admin_page(data_manager):
    """Render admin control panel"""
    st.markdown(
        """
    <h1 style="display: flex; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" style="margin-right: 10px;" viewBox="0 0 24 24">
  <path d="M3 17v2h6v-2H3zM3 5v2h10V5H3zm10 16v-2h8v-2h-8v-2h-2v6h2zM7 9v2H3v2h4v2h2V9H7zm14 4v-2H11v2h10zm-6-4h2V7h4V5h-4V3h-2v6z"/>
</svg>
        Administrative Controls
    </h1>
    """,
        unsafe_allow_html=True,
    )
    tab1, tab2, tab3 = st.tabs(
        ["Auto-marking Settings", "User Management", "System Settings"]
    )
    current_page = st.query_params.get(
        "page", "administrative control"
    )  # Default page = 'home'

    # Define CSS for specific pages
    css_styles = """
    <style>
    /* Default Button Style */
    button {
        background: linear-gradient(90deg, #1E3A8A, #3B82F6)
        color: white !important;
        border-radius: 5px !important;
    }
    /* Styling for Page 1 */
    .page-absent button {
        background: linear-gradient(90deg, #1E3A8A, #3B82F6)
        color: #fff !important;
        font-weight: bold !important;
    }
    </style>
"""

    # Inject CSS
    st.markdown(css_styles, unsafe_allow_html=True)

    # Add page-specific class
    st.markdown(f'<div class="page-{current_page}"></div>', unsafe_allow_html=True)
    with tab1:
        # Show auto-marked absences first
        st.markdown(
            """
    <h2 style="display: flex; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="black" style="margin-right: 10px;" viewBox="0 0 24 24">
          <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4zm7 4h-6v-2h6v2z"/>
        </svg>
        Auto-Marked Absences Today
    </h2>
    """,
            unsafe_allow_html=True,
        )
        today = date.today()
        attendance_df = data_manager.get_todays_attendance()
        auto_marked = attendance_df[
            (attendance_df["is_auto"] == True) & (attendance_df["status"] == "absent")
        ]

        if not auto_marked.empty:
            # Convert time to 12-hour format
            auto_marked["display_time"] = pd.to_datetime(
                auto_marked["timestamp"]
            ).dt.strftime("%I:%M %p")
            st.dataframe(
                auto_marked,
                column_config={
                    "teacher_id": "Teacher ID",
                    "display_time": "Time",
                    "status": "Status",
                },
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No auto-marked absences for today")

        st.divider()

        st.markdown(
            """
    <h3 style="display: flex; align-items: center;">
         <h3 style="display: flex; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" style="margin-right: 8px;" viewBox="0 0 24 24">
            <!-- Clock Outline -->
            <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
            <!-- Clock Hands -->
            <path d="M13 7h-2v5.414l3.293 3.293 1.414-1.414L13 11.586V7z"/>
            <!-- Small Play Symbol (triangle) indicating automation start/run -->
            <path d="M14.5 14.5v3l3-1.5-3-1.5z"/>
        </svg>
        Auto-Absence Settings
    </h3>
    """,
            unsafe_allow_html=True,
        )
        if "auto_marker" not in st.session_state:
            from auto_marker import AutoMarker

            st.session_state.auto_marker = AutoMarker(data_manager)
            st.session_state.auto_marker.start()

        timing = st.session_state.auto_marker.get_timing()

        st.write(
            "The system will automatically mark all unmarked teachers as absent at the configured time."
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        # Time settings
        with col1:
            hour = st.number_input(
                "Hour",
                min_value=1,
                max_value=23,
                value=timing["hour"] if timing["hour"] <= 12 else timing["hour"] - 12,
            )
        with col2:
            minute = st.number_input(
                "Minute", min_value=0, max_value=59, value=timing["minute"]
            )
        with col3:
            enabled = st.checkbox("Enable Auto-Marking", value=timing["enabled"])

        if st.button("Save Timing", use_container_width=True):
            # Convert 12-hour to 24-hour format for internal storage

            save_hour = hour
            if hour == 12:  # 12 AM = 00:00 in 24-hour format
                save_hour = 0

            st.session_state.auto_marker.set_timing(save_hour, minute, enabled)
            st.success("Auto-mark timing updated!")

        # Display current settings in 12-hour format
        current_time = datetime.strptime(
            f"{timing['hour']:02d}:{timing['minute']:02d}", "%H:%M"
        )
        display_time = current_time.strftime("%I:%M %p")
        st.info(
            f"Current Setting: "
            f"{'🟢 Enabled' if timing['enabled'] else '🔴 Disabled'} at "
            f"{display_time}"
        )
        st.divider()
        st.markdown(
            """
    <h3 style="display: flex; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" style="margin-right: 8px;" viewBox="0 0 24 24">
            <!-- User 1 -->
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V18c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-1.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-1.5c0-2.33-4.67-3.5-7-3.5z"/>
             <!-- Swap Arrows -->
            <path d="M14.5 8.5 L18.5 11.5 M18.5 8.5 L14.5 11.5"/> <!-- Simple X arrows -->
            <!-- OR more complex arrows if needed -->
        </svg>
        Arrangements Control
    </h3>
    """,
            unsafe_allow_html=True,
        )
        today = date.today()

        # Check if arrangements are suspended for today
        suspended = data_manager.is_arrangement_suspended(today)

        # Time settings for arrangements
        st.write(
            "Set the time when the system should create arrangements for absent teachers."
        )
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            arr_hour = st.number_input(
                "Hour", min_value=1, max_value=12, value=10, step=1
            )  # Default 10 AM
        with col2:
            arr_minute = st.number_input(
                "Minute", min_value=0, max_value=59, value=0, step=1
            )
        with col3:
            st.checkbox("Time will be set in AM")

        if st.button("Save Arrangement Time", use_container_width=True):
            # Save arrangement time (store in 24-hour format)
            save_hour = arr_hour if arr_hour != 12 else 0
            data_manager.set_arrangement_time(save_hour, arr_minute)
            st.success("Arrangement time updated!")

        # Display current arrangement time
        arr_timing = data_manager.get_arrangement_time()
        current_arr_time = datetime.strptime(
            f"{arr_timing['hour']:02d}:{arr_timing['minute']:02d}", "%H:%M"
        )
        display_arr_time = current_arr_time.strftime("%I:%M %p")
        st.info(f"Current arrangement time: {display_arr_time}")

        st.divider()

        if st.button(
            (
                "✋ Stop Today's Arrangements"
                if not suspended
                else "▶️ Resume Arrangements"
            ),
            type="primary" if not suspended else "secondary",
            use_container_width=True,
        ):
            if suspended:
                data_manager.resume_arrangements(today)
                st.success("Arrangements resumed for today!")
            else:
                data_manager.suspend_arrangements(today)
                st.success("Arrangements suspended for today!")

        # Show suspension status
        if suspended:
            st.warning("⚠️ Arrangements are currently suspended for today")
        else:
            st.info("✅ Arrangements are active for today")

    with tab2:
        st.subheader("User Management")

        # Load existing users
        try:
            users_df = pd.read_csv("attached_assets/users.csv")

            # Display users in a table with filtering
            st.write("All Registered Users:")

            # Filter options
            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                filter_role = st.selectbox(
                    "Filter by Role", ["All", "admin", "teacher"]
                )

            with filter_col2:
                search_term = st.text_input("Search by Name or ID")

            # Apply filters
            filtered_df = users_df.copy()

            if filter_role != "All":
                filtered_df = filtered_df[filtered_df["role"] == filter_role]

            if search_term:
                name_match = filtered_df["name"].str.contains(search_term, case=False)
                id_match = filtered_df["teacher_id"].str.contains(
                    search_term, case=False
                )
                filtered_df = filtered_df[name_match | id_match]

            # Display the filtered dataframe
            if not filtered_df.empty:
                # Don't show password column
                display_df = filtered_df.drop(columns=["password"])
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No users match the selected filters.")

        except Exception as e:
            st.error(f"Error loading users: {str(e)}")

    with tab3:
        st.subheader("System Settings")

        # Suspended dates management
        st.write("Manage Suspended Arrangement Dates:")

        try:
            suspended_dates_df = pd.read_csv("configs/suspended_dates.csv")

            if not suspended_dates_df.empty:
                st.write("Current suspended dates:")

                for _, row in suspended_dates_df.iterrows():
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(row["date"])

                    with col2:
                        if st.button("Remove", key=f"remove_{row['date']}"):
                            data_manager.resume_arrangements(row["date"])
                            st.success(f"Removed suspension for {row['date']}")
                            st.rerun()
            else:
                st.info("No dates are currently suspended.")

        except Exception as e:
            st.error(f"Error loading suspended dates: {str(e)}")

        st.write("Add a new suspended date:")

        suspended_date = st.date_input("Select Date")

        if st.button("Suspend Arrangements for Selected Date"):
            # Convert to string format
            date_str = suspended_date.strftime("%Y-%m-%d")

            if data_manager.is_arrangement_suspended(date_str):
                st.warning(f"Arrangements are already suspended for {date_str}")
            else:
                data_manager.suspend_arrangements(date_str)
                st.success(f"Arrangements suspended for {date_str}")
                st.rerun()

        # Database backup/export
        st.divider()
        st.subheader("Data Export")

        export_type = st.selectbox(
            "Select Data to Export",
            ["Attendance Records", "Teacher Information", "Arrangements"],
        )

        if st.button("Export Data"):
            try:
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

                if export_type == "Attendance Records":
                    df = pd.read_csv("attached_assets/attendance.csv")
                    filename = f"attendance_export_{current_time}.csv"

                elif export_type == "Teacher Information":
                    df = pd.read_csv("attached_assets/users.csv")
                    # Don't export passwords
                    df = df.drop(columns=["password"])
                    filename = f"teachers_export_{current_time}.csv"

                elif export_type == "Arrangements":
                    df = pd.read_csv("attached_assets/arrangements.csv")
                    filename = f"arrangements_export_{current_time}.csv"

                # Convert to CSV for download
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV File",
                    data=csv,
                    file_name=filename,
                    mime="text/csv",
                )

            except Exception as e:
                st.error(f"Export failed: {str(e)}")
