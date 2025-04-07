import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import plotly.express as px


def render_reports_page(data_manager):
    """Render the reports page"""
    st.markdown(
        """
        <div style="margin-top: 20px; margin-bottom: 30px;">
            <h1 style="display: flex; align-items: center; gap: 10px;">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 3v18M3 12h18M3 6h18M3 18h18"/>
                </svg>
                Reports
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <h3 style="display: flex; align-items: center; gap: 10px; color: #2C3E50;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            Select Date Range
        </h3>
    """,
        unsafe_allow_html=True,
    )

    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date.today() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", date.today())

    if end_date < start_date:
        st.error("🚨End date should be after start date")
        return

    # Load attendance data
    try:
        attendance_df = pd.read_csv("attached_assets/attendance.csv")
        attendance_df["date"] = pd.to_datetime(attendance_df["date"]).dt.date

        # Apply date filter to main dataframe
        mask = (attendance_df["date"] >= start_date) & (
            attendance_df["date"] <= end_date
        )
        filtered_df = attendance_df[mask]
    except Exception as e:
        st.error(f"Error loading reports: {str(e)}")
        return

    # Create tabs after filtering
    tab1, tab2, tab3 = st.tabs(["Attendance Summary", "Teacher Analysis", "Raw Data"])
    with tab1:
        if not filtered_df.empty:
            # Summary statistics
            total_records = len(filtered_df)
            present_count = len(filtered_df[filtered_df["status"] == "present"])
            absent_count = len(filtered_df[filtered_df["status"] == "absent"])
            auto_marked = len(filtered_df[filtered_df["is_auto"] == True])

        # Custom CSS for stat cards
        st.markdown(
            """
        <style>
        .stat-card-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            border-radius: 20px;
            padding: 25px;
            flex: 1;
            min-width: 200px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.06);
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            margin: 10px;
            height: 160px;
        }
        .stat-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        }
        .stat-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 20px;
            padding: 2px;
            background: linear-gradient(90deg, rgba(255,255,255,0.2), rgba(255,255,255,0.6));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
        }
        .stat-number {
            font-size: 36px;
            font-weight: 800;
            margin: 10px 0;
            font-family: 'Inter', system-ui, sans-serif;
            background: linear-gradient(45deg, #333, #666);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-label {
            color: #666;
            font-size: 15px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 20px;
            font-family: 'Inter', system-ui, sans-serif;
        }
        .stat-trend {
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 30px;
            opacity: 0.2;
        }
        .stat-trend path {
            stroke: currentColor;
            stroke-width: 2;
            fill: none;
        }
        .stat-icon {
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 30px;
            height: 30px;
        }

        </style>
        """,
            unsafe_allow_html=True,
        )

        # Display metrics in new design
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">{total_records}</div>
                    <div class="stat-label">Total Records</div>
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="24" height="24">
                            <rect x="2" y="13" width="4" height="8" fill="#1976D2"/>
                            <rect x="8" y="9" width="4" height="12" fill="#2196F3"/>
                            <rect x="14" y="5" width="4" height="16" fill="#64B5F6"/>
                            <rect x="20" y="2" width="4" height="19" fill="#90CAF9"/>
                        </svg>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">{present_count}</div>
                    <div class="stat-label">Present Today</div>
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="24" height="24">
                            <rect x="2" y="13" width="4" height="8" fill="#388E3C"/>
                            <rect x="8" y="9" width="4" height="12" fill="#4CAF50"/>
                            <rect x="14" y="5" width="4" height="16" fill="#81C784"/>
                            <rect x="20" y="2" width="4" height="19" fill="#A5D6A7"/>
                        </svg>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">{absent_count}</div>
                    <div class="stat-label">Absent Today</div>
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="24" height="24">
                            <rect x="2" y="13" width="4" height="8" fill="#C62828"/>
                            <rect x="8" y="9" width="4" height="12" fill="#F44336"/>
                            <rect x="14" y="5" width="4" height="16" fill="#E57373"/>
                            <rect x="20" y="2" width="4" height="19" fill="#FFCDD2"/>
                        </svg>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">{auto_marked}</div>
                    <div class="stat-label">Auto Marked</div>
                    <div class="stat-icon">
                        <svg viewBox="0 0 24 24" width="24" height="24">
                            <rect x="2" y="13" width="4" height="8" fill="#6A1B9A"/>
                            <rect x="8" y="9" width="4" height="12" fill="#9C27B0"/>
                            <rect x="14" y="5" width="4" height="16" fill="#BA68C8"/>
                            <rect x="20" y="2" width="4" height="19" fill="#E1BEE7"/>
                        </svg>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.divider()
        # 🔹 Two-column layout for tables
        col1, col2 = st.columns([1, 1])  # Ensure equal width

        # 🔹 LEFT: Detailed Records
        with col1:
            if not filtered_df.empty:
                st.markdown(
                    """
                <h3 style="display: flex; align-items: center; gap: 10px; color: #2C3E50;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                        <polyline points="10 9 9 9 8 9"/>
                    </svg>
                    Detailed Records
                </h3>
            """,
                    unsafe_allow_html=True,
                )
                st.dataframe(
                    filtered_df,
                    column_config={
                        "teacher_id": st.column_config.Column(
                            "Teacher ID", help="Unique identifier for each teacher"
                        ),
                        "date": st.column_config.DateColumn("📅Date"),
                        "status": st.column_config.Column("📌Status"),
                        "timestamp": st.column_config.TimeColumn("⏰Time"),
                        "is_auto": st.column_config.CheckboxColumn("🤖Auto Marked"),
                    },
                    hide_index=True,
                    width=900,
                )
            else:
                st.info("⚠️No records found for the selected date range")

        # 🔹 RIGHT: Recent Activity
        with col2:
            try:
                st.markdown(
                    """
                <h3 style="display: flex; align-items: center; gap: 10px; color: #2C3E50;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                    </svg>
                    Recent Activity
                </h3>
            """,
                    unsafe_allow_html=True,
                )
                recent_records = data_manager.get_recent_attendance(10)

                if not recent_records.empty:
                    recent_records["display_time"] = pd.to_datetime(
                        recent_records["timestamp"]
                    ).dt.strftime("%I:%M %p")
                    st.dataframe(
                        recent_records,
                        column_config={
                            "date": "📅Date",
                            "teacher_id": "👨‍🏫Teacher ID",
                            "status": "📌Status",
                            "display_time": "⏰Time",
                            "is_auto": "🤖Auto Marked",
                        },
                        hide_index=True,
                    )
                else:
                    st.info("No recent activity")

            except Exception as e:
                st.error(f"Error loading reports: {str(e)}")

            # 🔹 Attendance trend chart
        st.markdown(
            """
            <h3 style="display: flex; align-items: center; gap: 10px; color: #2C3E50;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 3v18h18"/>
                    <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
                </svg>
                Attendance Trend
            </h3>
        """,
            unsafe_allow_html=True,
        )
        daily_attendance = (
            attendance_df.groupby(["date", "status"]).size().unstack(fill_value=0)
        )
        fig = px.line(daily_attendance, title="Daily Attendance Trend")
        st.plotly_chart(fig)
    with tab2:
        st.subheader("Teacher Analysis")

        # Get teacher data
        teachers = data_manager.get_all_teachers()
        teacher_ids = [t["teacher_id"] for t in teachers]
        teacher_names = {t["teacher_id"]: t["name"] for t in teachers}

        # Filter to include only data for the teachers we know
        filtered_df["teacher_name"] = filtered_df["teacher_id"].apply(
            lambda x: teacher_names.get(x, x)
        )

        # Group by teacher using filtered data
        teacher_summary = (
            filtered_df.groupby(["teacher_id", "teacher_name", "status"])
            .size()
            .reset_index(name="count")
        )

        # Pivot to get present/absent counts per teacher
        teacher_pivot = teacher_summary.pivot(
            index=["teacher_id", "teacher_name"], columns="status", values="count"
        ).reset_index()

        # Fill NaN with 0
        if "present" not in teacher_pivot.columns:
            teacher_pivot["present"] = 0
        if "absent" not in teacher_pivot.columns:
            teacher_pivot["absent"] = 0

        teacher_pivot = teacher_pivot.fillna(0)

        # Calculate total and attendance percentage
        teacher_pivot["total"] = teacher_pivot["present"] + teacher_pivot["absent"]
        teacher_pivot["attendance_rate"] = (
            teacher_pivot["present"] / teacher_pivot["total"] * 100
        ).round(1)

        # Sort by attendance rate
        teacher_pivot = teacher_pivot.sort_values("attendance_rate", ascending=False)

        # Display as bar chart
        fig3 = px.bar(
            teacher_pivot,
            x="teacher_name",
            y="attendance_rate",
            labels={
                "teacher_name": "Teacher",
                "attendance_rate": "Attendance Rate (%)",
            },
            color="attendance_rate",
            color_continuous_scale=["#d32f2f", "#ffeb3b", "#2e7d32"],
            range_color=[0, 100],
        )

        fig3.update_layout(
            xaxis_title="Teacher",
            yaxis_title="Attendance Rate (%)",
            xaxis={"categoryorder": "total descending"},
            margin=dict(l=0, r=0, t=20, b=0),
            height=500,
        )

        st.plotly_chart(fig3, use_container_width=True)

        # Display teacher details in a table
        st.subheader("Teacher Attendance Details")

        display_df = teacher_pivot.copy()
        display_df = display_df.rename(
            columns={
                "teacher_name": "Teacher",
                "present": "Present Days",
                "absent": "Absent Days",
                "total": "Total Records",
                "attendance_rate": "Attendance Rate (%)",
            }
        )

        # Drop teacher_id column for display
        display_df = display_df.drop(columns=["teacher_id"])

        st.dataframe(display_df, use_container_width=True)

    with tab3:
        st.subheader("Raw Attendance Data")

        # Display the raw data with filters
        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            status_filter = st.selectbox(
                "Filter by Status", ["All", "present", "absent"]
            )

        with filter_col2:
            teacher_filter = st.selectbox(
                "Filter by Teacher",
                ["All"]
                + [
                    f"{teacher_names.get(tid, tid)} ({tid})"
                    for tid in sorted(teacher_ids)
                ],
            )

        # Apply additional filters to already date-filtered data
        display_df = filtered_df.copy()

        if status_filter != "All":
            display_df = display_df[display_df["status"] == status_filter]

        if teacher_filter != "All":
            teacher_id = teacher_filter.split("(")[-1].replace(")", "")
            filtered_df = filtered_df[filtered_df["teacher_id"] == teacher_id]

        # Sort by date and time
        filtered_df = filtered_df.sort_values("timestamp", ascending=False)

        # Replace teacher_id with teacher name where possible
        filtered_df["teacher"] = filtered_df["teacher_id"].apply(
            lambda x: f"{teacher_names.get(x, 'Unknown')} ({x})"
        )

        # Select columns to display
        display_cols = ["date", "teacher", "status", "timestamp", "is_auto"]

        # Rename columns for display
        renamed_df = filtered_df[
            ["date", "teacher", "status", "timestamp", "is_auto"]
        ].rename(
            columns={
                "date": "Date",
                "teacher": "Teacher",
                "status": "Status",
                "timestamp": "Timestamp",
                "is_auto": "Auto-marked",
            }
        )

        st.dataframe(renamed_df, use_container_width=True)

        # Export option
        if st.button("Export Filtered Data"):
            csv = renamed_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
