import pandas as pd
import os
from datetime import datetime, date
import json


class DataManager:
    def __init__(self):
        self.users_file = "attached_assets/users.csv"
        self.attendance_file = "attached_assets/attendance.csv"
        self.arrangements_file = "attached_assets/arrangements.csv"
        self.workload_file = "attached_assets/workload_counter.csv"
        print(f"--- DEBUG: Workload file path set to: {self.workload_file} ---")

        # Daily schedule files for 6 days of the week (Monday to Saturday)
        self.schedule_files = {
            0: "attached_assets/schedule_monday.csv",  # Monday
            1: "attached_assets/schedule_tuesday.csv",  # Tuesday
            2: "attached_assets/schedule_wednesday.csv",  # Wednesday
            3: "attached_assets/schedule_thursday.csv",  # Thursday
            4: "attached_assets/schedule_friday.csv",  # Friday
            5: "attached_assets/schedule_saturday.csv",  # Saturday
        }

        # Legacy schedule file - will be used as fallback
        self.schedules_file = "attached_assets/schedules.csv"
        self.suspended_dates_file = "configs/suspended_dates.csv"
        self.timing_file = "configs/timing.csv"
        self.workload_file = "attached_assets/workload_counter.csv"

        self._init_files()
        print("--- DEBUG: DataManager initialization complete ---")

    def _init_files(self):
        """Initialize CSV files if they don't exist"""
        if not os.path.exists("attached_assets"):
            os.makedirs("attached_assets")
        if not os.path.exists("configs"):
            os.makedirs("configs")

        # Initialize attendance.csv
        if not os.path.exists(self.attendance_file):
            pd.DataFrame(
                columns=["teacher_id", "date", "status", "timestamp", "is_auto"]
            ).to_csv(self.attendance_file, index=False)

        # Initialize arrangements.csv
        if not os.path.exists(self.arrangements_file):
            pd.DataFrame(
                columns=[
                    "date",
                    "absent_teacher",
                    "absent_category",
                    "replacement_teacher",
                    "replacement_category",
                    "class",
                    "period",
                    "status",
                    "match_quality",
                ]
            ).to_csv(self.arrangements_file, index=False)

        # Initialize daily schedule files for each day of the week
        schedule_columns = [
            "teacher_id",
            "name",
            "subject",
            "category",
            "period1",
            "period2",
            "period3",
            "period4",
            "period5",
            "period6",
            "period7",
        ]

        for day, schedule_file in self.schedule_files.items():
            if not os.path.exists(schedule_file):
                pd.DataFrame(columns=schedule_columns).to_csv(
                    schedule_file, index=False
                )
                print(f"Created schedule file for day {day}: {schedule_file}")

        # Initialize legacy schedules.csv (for backward compatibility)
        if not os.path.exists(self.schedules_file):
            pd.DataFrame(columns=schedule_columns).to_csv(
                self.schedules_file, index=False
            )

        # Initialize suspended_dates.csv
        if not os.path.exists(self.suspended_dates_file):
            pd.DataFrame(columns=["date"]).to_csv(
                self.suspended_dates_file, index=False
            )

        # Initialize timing.csv
        if not os.path.exists(self.timing_file):
            pd.DataFrame({"hour": [10], "minute": [0], "enabled": [True]}).to_csv(
                self.timing_file, index=False
            )
            # Initialize workload_counter.csv
        if not os.path.exists(self.workload_file):
            # Create empty workload counter with teacher_id and count columns
            workload_df = pd.DataFrame(columns=["teacher_id", "workload_count"])

            # If users.csv exists, initialize workload counter for all teachers with zero
            if os.path.exists(self.users_file):
                try:
                    users_df = pd.read_csv(self.users_file)
                    teacher_ids = users_df["teacher_id"].tolist()
                    workload_df = pd.DataFrame(
                        {
                            "teacher_id": teacher_ids,
                            "workload_count": [0] * len(teacher_ids),
                        }
                    )
                except Exception as e:
                    print(
                        f"Warning: Could not initialize workload counter from users: {str(e)}"
                    )

            workload_df.to_csv(self.workload_file, index=False)

    def set_arrangement_time(self, hour, minute):
        """Set arrangement creation time"""
        try:
            timing_df = pd.DataFrame(
                {"hour": [hour], "minute": [minute], "enabled": [True]}
            )
            timing_df.to_csv(self.timing_file, index=False)
            return True
        except Exception as e:
            print(f"Error setting arrangement time: {str(e)}")
            return False

    def get_arrangement_time(self):
        """Get arrangement creation time"""
        try:
            timing_df = pd.read_csv(self.timing_file)
            if not timing_df.empty:
                return timing_df.iloc[0].to_dict()
            return {"hour": 10, "minute": 0, "enabled": True}  # Default values
        except Exception as e:
            print(f"Error getting arrangement time: {str(e)}")
            return {"hour": 10, "minute": 0, "enabled": True}  # Default values

    def load_teacher_schedules(self, specific_day=None):
        """
        Load teacher schedules based on the day of the week

        Parameters:
        - specific_day: If provided, load schedule for this specific day (0-5, Monday-Saturday)
                       If None, use current day of the week
        """
        try:
            # Determine which day's schedule to load
            if specific_day is not None:
                day_of_week = specific_day  # Use provided day (0-5)
            else:
                # Get current day of the week (0 = Monday, 6 = Sunday)
                current_day = datetime.now().weekday()

                # We only have schedules for Monday-Saturday (0-5)
                if current_day == 6:  # Sunday
                    print("No schedule for Sunday, using Monday's schedule as default")
                    day_of_week = 0  # Use Monday's schedule as default
                else:
                    day_of_week = current_day

            # Check if we have a schedule file for this day
            if day_of_week in self.schedule_files and os.path.exists(
                self.schedule_files[day_of_week]
            ):
                file_path = self.schedule_files[day_of_week]
                print(f"Loading schedule for day {day_of_week} from {file_path}")

                # Read the schedule for the specific day
                schedules = pd.read_csv(file_path)

                # If the schedule is empty, fall back to the legacy schedule
                if schedules.empty:
                    print(
                        f"Schedule for day {day_of_week} is empty, using legacy schedule"
                    )
                    schedules = pd.read_csv(self.schedules_file)
            else:
                # Fallback to legacy schedule file if day-specific file doesn't exist
                print(
                    f"No schedule file found for day {day_of_week}, using legacy schedule"
                )
                schedules = pd.read_csv(self.schedules_file)

            return schedules

        except Exception as e:
            print(f"Error loading schedules: {str(e)}")
            import traceback

            traceback.print_exc()

            # Try fallback to legacy schedule
            try:
                print("Attempting to load legacy schedule as fallback")
                return pd.read_csv(self.schedules_file)
            except:
                # If all else fails, return empty DataFrame
                return pd.DataFrame()

    def get_attendance_report(self, start_date=None, end_date=None):
        attendance_df = pd.read_csv(self.attendance_file)
        if start_date and end_date:
            mask = (attendance_df["date"] >= start_date) & (
                attendance_df["date"] <= end_date
            )
            attendance_df = attendance_df.loc[mask]
        return attendance_df

    # def find_replacement_teacher(self, absent_teacher_id, period):
    #     """
    #     Find a suitable replacement teacher for a given period based on teacher categories
    #     Implements the category-based prioritization algorithm:

    #     For PGT teachers: PGT (same subject) → TGT (same subject) → PGT (any free)
    #     For TGT teachers: TGT (same subject) → PRT (same subject) → TGT (any free)
    #     For PRT teachers: PRT (same subject) → TGT (same subject) → PRT (any free)
    #     """
    #     try:
    #         schedules = self.load_teacher_schedules()
    #         users_df = pd.read_csv(self.users_file)

    #         # Get absent teacher's details from schedule
    #         absent_teacher_row = schedules[schedules["teacher_id"] == absent_teacher_id]
    #         if absent_teacher_row.empty:
    #             print(f"No schedule found for teacher ID: {absent_teacher_id}")
    #             return None, None, None, None

    #         absent_teacher = absent_teacher_row.iloc[0]
    #         subject = absent_teacher["subject"]
    #         absent_teacher_name = absent_teacher["name"]

    #         # Get absent teacher's category from users.csv
    #         user_row = users_df[users_df["teacher_id"] == absent_teacher_id]
    #         if not user_row.empty:
    #             absent_category = user_row.iloc[0]["category"]
    #         else:
    #             # Fallback to category from schedule if not found in users.csv
    #             absent_category = absent_teacher["category"]

    #         print(
    #             f"Finding replacement for {absent_teacher_id} ({absent_teacher_name}), Category: {absent_category}, Subject: {subject}"
    #         )

    #         # Get all free teachers for the period
    #         all_free_teachers = schedules[
    #             (schedules[f"period{period}"] == "FREE")
    #             & (schedules["teacher_id"] != absent_teacher_id)
    #         ]

    #         if all_free_teachers.empty:
    #             print(f"No free teachers available for period {period}")
    #             return None, None, None, None

    #         # Define the search pattern based on absent teacher's category
    #         if absent_category == "PGT":
    #             search_order = [
    #                 {
    #                     "category": "PGT",
    #                     "match_subject": True,
    #                     "quality": "Ideal - Same category, same subject",
    #                 },
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": True,
    #                     "quality": "Acceptable - Lower category, same subject",
    #                 },
    #                 {
    #                     "category": "PGT",
    #                     "match_subject": False,
    #                     "quality": "Suboptimal - Same category, any subject",
    #                 },
    #             ]
    #         elif absent_category == "TGT":
    #             search_order = [
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": True,
    #                     "quality": "Ideal - Same category, same subject",
    #                 },
    #                 {
    #                     "category": "PRT",
    #                     "match_subject": True,
    #                     "quality": "Acceptable - Lower category, same subject",
    #                 },
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": False,
    #                     "quality": "Suboptimal - Same category, any subject",
    #                 },
    #             ]
    #         elif absent_category == "PRT":
    #             search_order = [
    #                 {
    #                     "category": "PRT",
    #                     "match_subject": True,
    #                     "quality": "Ideal - Same category, same subject",
    #                 },
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": True,
    #                     "quality": "Acceptable - Higher category, same subject",
    #                 },
    #                 {
    #                     "category": "PRT",
    #                     "match_subject": False,
    #                     "quality": "Suboptimal - Same category, any subject",
    #                 },
    #             ]
    #         else:
    #             # Default fallback if category is unknown
    #             search_order = [
    #                 {
    #                     "category": None,
    #                     "match_subject": True,
    #                     "quality": "Same subject match",
    #                 },
    #                 {
    #                     "category": None,
    #                     "match_subject": False,
    #                     "quality": "Any available teacher",
    #                 },
    #             ]

    #         # Perform the search according to the defined order
    #         for search_criteria in search_order:
    #             category = search_criteria["category"]
    #             match_subject = search_criteria["match_subject"]
    #             quality = search_criteria["quality"]

    #             filtered_teachers = all_free_teachers

    #             # Apply category filter if specified
    #             if category:
    #                 filtered_teachers = filtered_teachers[
    #                     filtered_teachers["category"] == category
    #                 ]

    #             # Apply subject filter if required
    #             if match_subject:
    #                 filtered_teachers = filtered_teachers[
    #                     filtered_teachers["subject"] == subject
    #                 ]

    #             if not filtered_teachers.empty:
    #                 replacement_id = filtered_teachers.iloc[0]["teacher_id"]
    #                 replacement_category = filtered_teachers.iloc[0]["category"]
    #                 replacement_name = filtered_teachers.iloc[0]["name"]

    #                 print(
    #                     f"Found replacement ({quality}): {replacement_id} ({replacement_name}, {replacement_category})"
    #                 )
    #                 return (
    #                     replacement_id,
    #                     replacement_category,
    #                     replacement_name,
    #                     absent_teacher_name,
    #                 )

    #         # If no replacement found after all search criteria
    #         print(f"No suitable replacement found for period {period}")
    #         return None, None, None, None

    #     except Exception as e:
    #         print(f"Error finding replacement: {str(e)}")
    #         import traceback

    #         traceback.print_exc()
    #         return None, None, None, None

    # def create_arrangements(self, absent_teacher_id, current_date):
    #     """Create arrangements for an absent teacher based on teacher categories (PGT/TGT/PRT)"""
    #     print(
    #         f">>> DEBUG: Inside create_arrangements for teacher: {absent_teacher_id}, Date: {current_date}"
    #     )
    #     try:
    #         schedules = self.load_teacher_schedules()
    #         users_df = pd.read_csv(self.users_file)

    #         # Get absent teacher details
    #         absent_teacher = schedules[
    #             schedules["teacher_id"] == absent_teacher_id
    #         ].iloc[0]

    #         # Get absent teacher's name from schedule
    #         absent_teacher_name = absent_teacher["name"]  # Get teacher name

    #         # Get absent teacher's category from users.csv
    #         user_row = users_df[users_df["teacher_id"] == absent_teacher_id]
    #         if not user_row.empty:
    #             absent_category = user_row.iloc[0]["category"]
    #         else:
    #             # Fallback to category from schedule if not found in users.csv
    #             absent_category = absent_teacher["category"]

    #         print(
    #             f"Creating arrangements for {absent_teacher_id} ({absent_teacher_name}), Category: {absent_category}"
    #         )

    #         arrangements = []
    #         # Check each period
    #         for period in range(1, 8):  # 7 periods as per the schedule
    #             period_col = f"period{period}"
    #             class_name = absent_teacher[period_col]
    #             print(f">>> DEBUG: Checking Period {period}, Class: {class_name}")

    #             # Skip if the teacher has a free period
    #             if class_name == "FREE":
    #                 print(f"Teacher has free period {period}, no arrangement needed")
    #                 continue

    #             # Find a replacement teacher for this period
    #             replacement_result = self.find_replacement_teacher(
    #                 absent_teacher_id, period
    #             )
    #             if replacement_result is not None and len(replacement_result) == 4:
    #                 (
    #                     replacement_id,
    #                     replacement_category,
    #                     replacement_name,
    #                     absent_name,
    #                 ) = replacement_result

    #                 if replacement_id:
    #                     # Create an arrangement for this period
    #                     arrangement = {
    #                         "date": current_date,
    #                         "absent_teacher": absent_teacher_id,
    #                         "absent_name": absent_name,  # Add absent teacher name
    #                         "absent_category": absent_category,
    #                         "replacement_teacher": replacement_id,
    #                         "replacement_name": replacement_name,  # Add replacement teacher name
    #                         "replacement_category": replacement_category,
    #                         "class": class_name,
    #                         "period": period,
    #                         "status": "PENDING",
    #                         "match_quality": self._determine_match_quality(
    #                             absent_category,
    #                             replacement_category,
    #                             absent_teacher["subject"],
    #                             schedules.loc[
    #                                 schedules["teacher_id"] == replacement_id, "subject"
    #                             ].iloc[0],
    #                         ),
    #                     }
    #                     print(f"Created arrangement: {arrangement}")
    #                     arrangements.append(arrangement)
    #                 else:
    #                     print(f"Could not find replacement for period {period}")
    #             else:
    #                 print(f"Failed to get replacement information for period {period}")

    #         # Save the created arrangements
    #         if arrangements:
    #             self._save_arrangements(arrangements)
    #             print(f"Saved {len(arrangements)} arrangements for {absent_teacher_id}")
    #             return True
    #         else:
    #             print(f"No arrangements created for {absent_teacher_id}")
    #             return False

    #     except Exception as e:
    #         print(f"Error creating arrangements: {str(e)}")
    #         import traceback

    #         traceback.print_exc()
    #         return False

    # def _determine_match_quality(
    #     self, absent_category, replacement_category, absent_subject, replacement_subject
    # ):
    #     """
    #     Determine the quality of the match based on categories and subjects

    #     Priority for PGT: PGT (same subject) → TGT (same subject) → PGT (any free)
    #     Priority for TGT: TGT (same subject) → PRT (same subject) → TGT (any free)
    #     Priority for PRT: PRT (same subject) → TGT (same subject) → PRT (any free)
    #     """
    #     # Same category, same subject - Ideal match
    #     if (
    #         absent_category == replacement_category
    #         and absent_subject == replacement_subject
    #     ):
    #         return "Ideal"

    #     # For PGT teacher: TGT with same subject - Acceptable match
    #     if (
    #         absent_category == "PGT"
    #         and replacement_category == "TGT"
    #         and absent_subject == replacement_subject
    #     ):
    #         return "Acceptable"

    #     # For TGT teacher: PRT with same subject - Acceptable match
    #     if (
    #         absent_category == "TGT"
    #         and replacement_category == "PRT"
    #         and absent_subject == replacement_subject
    #     ):
    #         return "Acceptable"

    #     # For PRT teacher: TGT with same subject - Acceptable match
    #     if (
    #         absent_category == "PRT"
    #         and replacement_category == "TGT"
    #         and absent_subject == replacement_subject
    #     ):
    #         return "Acceptable"

    #     # Same category, different subject - Suboptimal match
    #     if absent_category == replacement_category:
    #         return "Suboptimal"

    #     # Different category, different subject - Last resort
    #     return "Last Resort"

    # def find_replacement_teacher(self, absent_teacher_id, period):
    #     """
    #     Find a suitable replacement teacher for a given period based on multi-level matching strategy

    #     Multi-Level Matching Strategy:
    #     1. First look for teachers in same category with same subject
    #     2. Extract subject from period class (e.g., "ENGLISH (XI B)" -> "ENGLISH")
    #     3. Look for teachers with matching subject
    #     4. Try lower category teachers (PGT->TGT->PRT or TGT->PRT or PRT->TGT)
    #     5. Fallback to any free teacher in the same category

    #     With workload balancing:
    #     - When multiple teachers are suitable, prioritize those with lower workload
    #     """
    #     try:
    #         schedules = self.load_teacher_schedules()
    #         users_df = pd.read_csv(self.users_file)

    #         # Get absent teacher's details from schedule
    #         absent_teacher_row = schedules[schedules["teacher_id"] == absent_teacher_id]
    #         if absent_teacher_row.empty:
    #             print(f"No schedule found for teacher ID: {absent_teacher_id}")
    #             return None, None, None, None

    #         absent_teacher = absent_teacher_row.iloc[0]
    #         subject = absent_teacher["subject"]  # Main subject of the teacher
    #         absent_teacher_name = absent_teacher["name"]

    #         # Get the class name for this period (e.g., "ENGLISH (XI B)")
    #         period_col = f"period{period}"
    #         class_name = absent_teacher[period_col]

    #         # Extract subject from class name if possible (e.g., "ENGLISH (XI B)" -> "ENGLISH")
    #         period_subject = None
    #         if class_name != "FREE":
    #             # Format 1: "SUBJECT (CLASS)"
    #             if "(" in class_name:
    #                 # Extract subject part before parenthesis: "ENGLISH (XI B)" -> "ENGLISH"
    #                 period_subject = class_name.split("(")[0].strip()

    #             # Format 2: "CLASS SUBJECT"
    #             else:
    #                 # Common class prefixes to remove
    #                 class_prefixes = [
    #                     "XI",
    #                     "XII",
    #                     "X-",
    #                     "IX-",
    #                     "VIII",
    #                     "VII",
    #                     "VI",
    #                     "V",
    #                     "IV",
    #                     "III",
    #                 ]

    #                 # First try by removing class prefixes
    #                 temp_class_name = class_name.upper()
    #                 for prefix in class_prefixes:
    #                     if temp_class_name.startswith(prefix):
    #                         # Remove the prefix and any following characters until we get to the subject
    #                         # e.g., "X-B MATHS" -> Remove "X-B " and get "MATHS"
    #                         parts = temp_class_name.split()
    #                         if len(parts) > 1:
    #                             # Extract everything except the first part (class identifier)
    #                             period_subject = " ".join(parts[1:])
    #                             break

    #                 # If not found by prefix, try to match with common subjects
    #                 if not period_subject:
    #                     # Common subjects to look for
    #                     common_subjects = [
    #                         "MATHS",
    #                         "MATH",
    #                         "ENGLISH",
    #                         "HINDI",
    #                         "SCIENCE",
    #                         "PHYSICS",
    #                         "CHEMISTRY",
    #                         "BIOLOGY",
    #                         "HISTORY",
    #                         "GEOGRAPHY",
    #                         "ECONOMICS",
    #                         "POLITICAL",
    #                         "COMPUTER",
    #                         "ACCOUNTANCY",
    #                         "BUSINESS",
    #                         "DRAWING",
    #                         "AI",
    #                         "SST",
    #                         "S.ST.",
    #                         "PHE",
    #                         "SANSKRIT",
    #                         "SKT",
    #                         "GK",
    #                         "M.SC",
    #                         "MSC",
    #                         "GAME",
    #                     ]

    #                     for subj in common_subjects:
    #                         if subj in class_name.upper():
    #                             period_subject = subj
    #                             break

    #                     # If still not found, use the whole class name
    #                     if not period_subject:
    #                         period_subject = class_name

    #         # Use period_subject if available, otherwise use teacher's general subject
    #         search_subject = period_subject if period_subject else subject
    #         print(
    #             f"Extracted period subject: {period_subject}, using search subject: {search_subject}"
    #         )

    #         # Get absent teacher's category from users.csv
    #         user_row = users_df[users_df["teacher_id"] == absent_teacher_id]
    #         if not user_row.empty:
    #             absent_category = user_row.iloc[0]["category"]
    #         else:
    #             # Fallback to category from schedule if not found in users.csv
    #             absent_category = absent_teacher["category"]

    #         print(
    #             f"Finding replacement for {absent_teacher_id} ({absent_teacher_name}), Category: {absent_category}, Subject: {search_subject}, Class: {class_name}"
    #         )

    #         # Get all free teachers for the period
    #         all_free_teachers = schedules[
    #             (schedules[f"period{period}"] == "FREE")
    #             & (schedules["teacher_id"] != absent_teacher_id)
    #         ]

    #         if all_free_teachers.empty:
    #             print(f"No free teachers available for period {period}")
    #             return None, None, None, None

    #         # Define the search pattern based on absent teacher's category
    #         if absent_category == "PGT":
    #             search_order = [
    #                 {
    #                     "category": "PGT",
    #                     "match_subject": True,
    #                     "quality": "Ideal - Same category, same subject",
    #                 },
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": True,
    #                     "quality": "Acceptable - Lower category, same subject",
    #                 },
    #                 {
    #                     "category": "PGT",
    #                     "match_subject": False,
    #                     "quality": "Suboptimal - Same category, any subject",
    #                 },
    #             ]
    #         elif absent_category == "TGT":
    #             search_order = [
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": True,
    #                     "quality": "Ideal - Same category, same subject",
    #                 },
    #                 {
    #                     "category": "PRT",
    #                     "match_subject": True,
    #                     "quality": "Acceptable - Lower category, same subject",
    #                 },
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": False,
    #                     "quality": "Suboptimal - Same category, any subject",
    #                 },
    #             ]
    #         elif absent_category == "PRT":
    #             search_order = [
    #                 {
    #                     "category": "PRT",
    #                     "match_subject": True,
    #                     "quality": "Ideal - Same category, same subject",
    #                 },
    #                 {
    #                     "category": "TGT",
    #                     "match_subject": True,
    #                     "quality": "Acceptable - Higher category, same subject",
    #                 },
    #                 {
    #                     "category": "PRT",
    #                     "match_subject": False,
    #                     "quality": "Suboptimal - Same category, any subject",
    #                 },
    #             ]
    #         else:
    #             # Default fallback if category is unknown
    #             search_order = [
    #                 {
    #                     "category": None,
    #                     "match_subject": True,
    #                     "quality": "Same subject match",
    #                 },
    #                 {
    #                     "category": None,
    #                     "match_subject": False,
    #                     "quality": "Any available teacher",
    #                 },
    #             ]

    #         # Add a fallback option for any free teacher (regardless of category or subject)
    #         search_order.append(
    #             {
    #                 "category": None,
    #                 "match_subject": False,
    #                 "quality": "Last resort - Any available teacher",
    #             }
    #         )

    #         # Perform the search according to the defined order
    #         for search_criteria in search_order:
    #             category = search_criteria["category"]
    #             match_subject = search_criteria["match_subject"]
    #             quality = search_criteria["quality"]

    #             filtered_teachers = all_free_teachers

    #             # Apply category filter if specified
    #             if category:
    #                 filtered_teachers = filtered_teachers[
    #                     filtered_teachers["category"] == category
    #                 ]

    #             # Apply subject filter if required
    #             if match_subject:
    #                 # First, filter teachers who have the subject capability
    #                 # This checks if at least one of the replacement teacher's subjects match with the absent teacher's subject
    #                 qualified_teachers = []

    #                 for _, teacher in filtered_teachers.iterrows():
    #                     teacher_subjects = str(teacher["subject"]).split(",")
    #                     teacher_subjects = [s.strip() for s in teacher_subjects]

    #                     # Check if period subject is in teacher's subjects list
    #                     is_qualified = False
    #                     for teacher_subject in teacher_subjects:
    #                         # Make a more strict comparison - exact subject match, not just substring
    #                         # For example, if period subject is "MATH", teacher should have "MATH" or "MATHS" in their subjects
    #                         teacher_subject_upper = teacher_subject.upper()
    #                         search_subject_upper = search_subject.upper()

    #                         # Normalize common subject variations for better matching
    #                         # MATH/MATHS
    #                         if (
    #                             "MATH" in teacher_subject_upper
    #                             and not "MATHEMATIC" in teacher_subject_upper
    #                         ):
    #                             teacher_subject_upper = "MATH"
    #                         if (
    #                             "MATH" in search_subject_upper
    #                             and not "MATHEMATIC" in search_subject_upper
    #                         ):
    #                             search_subject_upper = "MATH"

    #                         # SST/S.ST/SOCIAL STUDIES
    #                         if any(
    #                             x in teacher_subject_upper
    #                             for x in ["SST", "S.ST", "SOCIAL STUDIES"]
    #                         ):
    #                             teacher_subject_upper = "SST"
    #                         if any(
    #                             x in search_subject_upper
    #                             for x in ["SST", "S.ST", "SOCIAL STUDIES"]
    #                         ):
    #                             search_subject_upper = "SST"

    #                         # SANSKRIT/SKT
    #                         if any(
    #                             x in teacher_subject_upper for x in ["SANSKRIT", "SKT"]
    #                         ):
    #                             teacher_subject_upper = "SANSKRIT"
    #                         if any(
    #                             x in search_subject_upper for x in ["SANSKRIT", "SKT"]
    #                         ):
    #                             search_subject_upper = "SANSKRIT"

    #                         # POLITICAL/POLITICAL SCIENCE
    #                         if "POLITICAL" in teacher_subject_upper:
    #                             teacher_subject_upper = "POLITICAL"
    #                         if "POLITICAL" in search_subject_upper:
    #                             search_subject_upper = "POLITICAL"

    #                         # Computer Science/COMPUTER/CS
    #                         if any(
    #                             x in teacher_subject_upper for x in ["COMPUTER", "CS"]
    #                         ):
    #                             teacher_subject_upper = "COMPUTER"
    #                         if any(
    #                             x in search_subject_upper for x in ["COMPUTER", "CS"]
    #                         ):
    #                             search_subject_upper = "COMPUTER"

    #                         # M.SC/MSC
    #                         if any(x in teacher_subject_upper for x in ["M.SC", "MSC"]):
    #                             teacher_subject_upper = "MSC"
    #                         if any(x in search_subject_upper for x in ["M.SC", "MSC"]):
    #                             search_subject_upper = "MSC"

    #                         # Check for matches with following criteria:
    #                         # 1. Exact match (e.g., "MATH" matches "MATH")
    #                         # 2. Singular/plural matches (e.g., "MATH" matches "MATHS" or vice versa)
    #                         # 3. Multi-subject teacher case (e.g., if teacher has "MATH,PHYSICS" and we need "MATH")
    #                         if (
    #                             teacher_subject_upper == search_subject_upper
    #                             or f"{teacher_subject_upper}S" == search_subject_upper
    #                             or teacher_subject_upper == f"{search_subject_upper}S"
    #                             or
    #                             # Check if teacher subject contains multiple subjects and one of them matches
    #                             (
    #                                 teacher_subject_upper.find(",") > 0
    #                                 and any(
    #                                     subj.strip() == search_subject_upper
    #                                     for subj in teacher_subject_upper.split(",")
    #                                 )
    #                             )
    #                         ):
    #                             is_qualified = True
    #                             print(
    #                                 f"Subject match: Teacher's '{teacher_subject}' matches with period subject '{search_subject}'"
    #                             )
    #                             break

    #                     if is_qualified:
    #                         qualified_teachers.append(teacher)

    #                 if qualified_teachers:
    #                     # Create DataFrame from qualified teachers
    #                     filtered_teachers = pd.DataFrame(qualified_teachers)
    #                 elif match_subject:
    #                     # If no qualified teachers, keep the filtered_teachers empty to move to next search criteria
    #                     filtered_teachers = pd.DataFrame()

    #             if not filtered_teachers.empty:
    #                 # If we have multiple matching teachers, sort by workload if the feature is available
    #                 if len(filtered_teachers) > 1:
    #                     try:
    #                         # Get workload for each teacher
    #                         workloads = []
    #                         for _, teacher in filtered_teachers.iterrows():
    #                             teacher_id = teacher["teacher_id"]
    #                             # Check if workload tracking is available
    #                             if hasattr(self, "get_teacher_workload"):
    #                                 workload = self.get_teacher_workload(teacher_id)
    #                                 workloads.append(
    #                                     {"teacher_id": teacher_id, "workload": workload}
    #                                 )
    #                             else:
    #                                 # Fallback - just use the first teacher
    #                                 workloads.append(
    #                                     {
    #                                         "teacher_id": teacher["teacher_id"],
    #                                         "workload": 0,
    #                                     }
    #                                 )

    #                         # Sort by workload (ascending)
    #                         workloads.sort(key=lambda x: x["workload"])

    #                         # Get teacher with lowest workload
    #                         teacher_id = workloads[0]["teacher_id"]
    #                         selected_teacher = filtered_teachers[
    #                             filtered_teachers["teacher_id"] == teacher_id
    #                         ].iloc[0]

    #                         replacement_id = selected_teacher["teacher_id"]
    #                         replacement_category = selected_teacher["category"]
    #                         replacement_name = selected_teacher["name"]
    #                     except Exception as e:
    #                         # Fallback if workload balancing fails
    #                         print(
    #                             f"Workload balancing error: {str(e)}, using first available teacher"
    #                         )
    #                         replacement_id = filtered_teachers.iloc[0]["teacher_id"]
    #                         replacement_category = filtered_teachers.iloc[0]["category"]
    #                         replacement_name = filtered_teachers.iloc[0]["name"]
    #                 else:
    #                     # Just one teacher
    #                     replacement_id = filtered_teachers.iloc[0]["teacher_id"]
    #                     replacement_category = filtered_teachers.iloc[0]["category"]
    #                     replacement_name = filtered_teachers.iloc[0]["name"]

    #                 # Increment the workload counter for this teacher if feature is available
    #                 try:
    #                     if hasattr(self, "update_teacher_workload"):
    #                         self.update_teacher_workload(replacement_id)
    #                 except Exception as e:
    #                     print(
    #                         f"Could not update workload counter: {str(e)}"
    #                     )  # Just log error and continue

    #                 print(
    #                     f"Found replacement ({quality}): {replacement_id} ({replacement_name}, {replacement_category})"
    #                 )
    #                 return (
    #                     replacement_id,
    #                     replacement_category,
    #                     replacement_name,
    #                     absent_teacher_name,
    #                 )

    #         # If no replacement found after all search criteria
    #         print(f"No suitable replacement found for period {period}")
    #         return None, None, None, None

    #     except Exception as e:
    #         print(f"Error finding replacement: {str(e)}")
    #         import traceback

    #         traceback.print_exc()
    #         return None, None, None, None
    def find_replacement_teacher(self, absent_teacher_id, period):
        """
        Find a suitable replacement teacher for a given period based on multi-level matching strategy

        Multi-Level Matching Strategy:
        1. First look for teachers in same category with same subject
        2. Extract subject from period class (e.g., "ENGLISH (XI B)" -> "ENGLISH")
        3. Look for teachers with matching subject
        4. Try lower category teachers (PGT->TGT->PRT or TGT->PRT or PRT->TGT)
        5. Fallback to any free teacher in the same category

        With workload balancing:
        - When multiple teachers are suitable, prioritize those with lower workload
        """
        try:
            schedules = self.load_teacher_schedules()
            users_df = pd.read_csv(self.users_file)

            # Get absent teacher's details from schedule
            absent_teacher_row = schedules[schedules["teacher_id"] == absent_teacher_id]
            if absent_teacher_row.empty:
                print(f"No schedule found for teacher ID: {absent_teacher_id}")
                return None, None, None, None

            absent_teacher = absent_teacher_row.iloc[0]
            subject = absent_teacher["subject"]  # Main subject of the teacher
            absent_teacher_name = absent_teacher["name"]

            # Get the class name for this period (e.g., "ENGLISH (XI B)")
            period_col = f"period{period}"
            class_name = absent_teacher[period_col]

            # Extract subject from class name for various formats
            period_subject = None
            print(f"Extracting subject from class name: '{class_name}'")

            if class_name != "FREE":
                # Format 1: "SUBJECT (CLASS)"
                if "(" in class_name and ")" in class_name:
                    # Extract subject part before parenthesis: "ENGLISH (XI B)" -> "ENGLISH"
                    period_subject = class_name.split("(")[0].strip().upper()
                    print(f"Format 1 - Subject from '(CLASS)': {period_subject}")

                # Format 2: "(CLASS) SUBJECT"
                elif (
                    ")" in class_name and class_name.find(")") < class_name.find(" ")
                    if " " in class_name
                    else False
                ):
                    # Extract subject part after parenthesis: "(XI B) ENGLISH" -> "ENGLISH"
                    period_subject = class_name.split(")", 1)[1].strip().upper()
                    print(f"Format 2 - Subject after ')': {period_subject}")

                # Format 3: "CLASS SUBJECT" (e.g., "X-B PHYSICS", "IX A ENGLISH")
                else:
                    # Common class identifiers to detect
                    class_patterns = [
                        r"(^|\s)(XI{1,3})\s+[A-D](/[A-D])*\s+",  # XI A, XII B/C/D
                        r"(^|\s)(X|IX|V?II{1,3}|VI{0,1}|IV|V)[-\s]+[A-D](\s*\(\d-\d\))?\s+",  # X-B, IX-C, VIII B, VII A
                        r"(^|\s)(X|IX|V?II{1,3}|VI{0,1}|IV|V)\s+[A-D](\s*\(\d-\d\))?\s+",  # X A, IX C, VIII B, VII A
                    ]

                    import re

                    processed = False
                    for pattern in class_patterns:
                        # Try to match class identifier pattern and extract what comes after
                        match = re.search(pattern, class_name.upper())
                        if match:
                            # Get subject part after the class identifier
                            subject_part = re.sub(
                                pattern, "", class_name.upper()
                            ).strip()
                            if subject_part:
                                period_subject = subject_part
                                print(
                                    f"Format 3 - Subject after class identifier: {period_subject}"
                                )
                                processed = True
                                break

                    # If still not processed, try common subject matching
                    if not processed:
                        # Define common subject names
                        common_subjects = {
                            "MATHS": ["MATH", "MATHS", "MATHEMATICS"],
                            "PHYSICS": ["PHYSICS", "PHY"],
                            "CHEMISTRY": ["CHEMISTRY", "CHEM"],
                            "BIOLOGY": ["BIOLOGY", "BIO"],
                            "ENGLISH": ["ENGLISH", "ENG"],
                            "HINDI": ["HINDI"],
                            "SCIENCE": ["SCIENCE", "SCI"],
                            "ACCOUNTANCY": ["ACCOUNTANCY", "ACCOUNTS"],
                            "ECONOMICS": ["ECONOMICS", "ECO"],
                            "BUSINESS STUDIES": ["BUSINESS", "BUSINESS STUDIES"],
                            "COMPUTER SCIENCE": ["COMPUTER", "COMPUTER SCIENCE", "CS"],
                            "HISTORY": ["HISTORY", "HIST"],
                            "POLITICAL SCIENCE": [
                                "POLITICAL",
                                "POLITICAL SCIENCE",
                                "POL.SC",
                            ],
                            "PHE": ["PHE", "PHYSICAL EDUCATION"],
                            "SST": ["SST", "S.ST.", "SOCIAL STUDIES", "SOCIAL SCIENCE"],
                            "AI": ["AI", "ARTIFICIAL INTELLIGENCE"],
                            "SANSKRIT": ["SANSKRIT", "SKT"],
                            "GK": ["GK", "GENERAL KNOWLEDGE"],
                            "MSC": ["MSC", "M.SC.", "M.SC"],
                            "DRAWING": ["DRAWING", "DRAW"],
                            "GAME": ["GAME", "GAMES", "SPORTS"],
                        }

                        # Check if any common subject is present in the class name
                        cls_upper = class_name.upper()
                        for main_subject, variations in common_subjects.items():
                            for variation in variations:
                                if variation in cls_upper.split():
                                    period_subject = main_subject
                                    print(
                                        f"Format 4 - Common subject match: {period_subject}"
                                    )
                                    processed = True
                                    break
                            if processed:
                                break

                        # If still not processed, use the whole class name
                        if not processed:
                            period_subject = class_name.upper()
                            print(
                                f"Format 5 - Using full class name as subject: {period_subject}"
                            )

            print(f"Extracted period subject: {period_subject}")

            # Use period_subject if available, otherwise use teacher's general subject
            search_subject = period_subject if period_subject else subject
            print(
                f"Extracted period subject: {period_subject}, using search subject: {search_subject}"
            )

            # Get absent teacher's category from users.csv
            user_row = users_df[users_df["teacher_id"] == absent_teacher_id]
            if not user_row.empty:
                absent_category = user_row.iloc[0]["category"]
            else:
                # Fallback to category from schedule if not found in users.csv
                absent_category = absent_teacher["category"]

            print(
                f"Finding replacement for {absent_teacher_id} ({absent_teacher_name}), Category: {absent_category}, Subject: {search_subject}, Class: {class_name}"
            )

            # Get all free teachers for the period
            all_free_teachers = schedules[
                (schedules[f"period{period}"] == "FREE")
                & (schedules["teacher_id"] != absent_teacher_id)
            ]

            if all_free_teachers.empty:
                print(f"No free teachers available for period {period}")
                return None, None, None, None

            # Define the search pattern based on absent teacher's category
            if absent_category == "PGT":
                search_order = [
                    {
                        "category": "PGT",
                        "match_subject": True,
                        "quality": "Ideal - Same category, same subject",
                    },
                    {
                        "category": "TGT",
                        "match_subject": True,
                        "quality": "Acceptable - Lower category, same subject",
                    },
                    {
                        "category": "PGT",
                        "match_subject": False,
                        "quality": "Suboptimal - Same category, any subject",
                    },
                ]
            elif absent_category == "TGT":
                search_order = [
                    {
                        "category": "TGT",
                        "match_subject": True,
                        "quality": "Ideal - Same category, same subject",
                    },
                    {
                        "category": "PRT",
                        "match_subject": True,
                        "quality": "Acceptable - Lower category, same subject",
                    },
                    {
                        "category": "TGT",
                        "match_subject": False,
                        "quality": "Suboptimal - Same category, any subject",
                    },
                ]
            elif absent_category == "PRT":
                search_order = [
                    {
                        "category": "PRT",
                        "match_subject": True,
                        "quality": "Ideal - Same category, same subject",
                    },
                    {
                        "category": "TGT",
                        "match_subject": True,
                        "quality": "Acceptable - Higher category, same subject",
                    },
                    {
                        "category": "PRT",
                        "match_subject": False,
                        "quality": "Suboptimal - Same category, any subject",
                    },
                ]
            else:
                # Default fallback if category is unknown
                search_order = [
                    {
                        "category": None,
                        "match_subject": True,
                        "quality": "Same subject match",
                    },
                    {
                        "category": None,
                        "match_subject": False,
                        "quality": "Any available teacher",
                    },
                ]

            # Add a fallback option for any free teacher (regardless of category or subject)
            search_order.append(
                {
                    "category": None,
                    "match_subject": False,
                    "quality": "Last resort - Any available teacher",
                }
            )

            # Perform the search according to the defined order
            for search_criteria in search_order:
                category = search_criteria["category"]
                match_subject = search_criteria["match_subject"]
                quality = search_criteria["quality"]

                filtered_teachers = all_free_teachers

                # Apply category filter if specified
                if category:
                    filtered_teachers = filtered_teachers[
                        filtered_teachers["category"] == category
                    ]

                # Apply subject filter if required
                if match_subject:
                    # First, filter teachers who have the subject capability
                    # This checks if at least one of the replacement teacher's subjects match with the absent teacher's subject
                    qualified_teachers = []

                    for _, teacher in filtered_teachers.iterrows():
                        # Get teacher's subject list and normalize for matching
                        all_teacher_subjects = str(teacher["subject"]).upper().strip()
                        # Split multiple subjects if comma-separated
                        teacher_subjects_list = [
                            s.strip() for s in all_teacher_subjects.split(",")
                        ]

                        # Define subject mapping for standardization
                        subject_mapping = {
                            # Mathematics
                            "MATH": ["MATH", "MATHS", "MATHEMATICS"],
                            # Sciences
                            "PHYSICS": ["PHYSICS", "PHY"],
                            "CHEMISTRY": ["CHEMISTRY", "CHEM"],
                            "BIOLOGY": ["BIOLOGY", "BIO"],
                            "SCIENCE": ["SCIENCE", "SCI"],
                            # Languages
                            "ENGLISH": ["ENGLISH", "ENG"],
                            "HINDI": ["HINDI"],
                            "SANSKRIT": ["SANSKRIT", "SKT"],
                            # Commerce/Humanities
                            "ACCOUNTANCY": ["ACCOUNTANCY", "ACCOUNTS"],
                            "ECONOMICS": ["ECONOMICS", "ECO"],
                            "BUSINESS STUDIES": ["BUSINESS", "BUSINESS STUDIES", "BST"],
                            "HISTORY": ["HISTORY", "HIST"],
                            "POLITICAL SCIENCE": [
                                "POLITICAL",
                                "POLITICAL SCIENCE",
                                "POL.SC",
                            ],
                            "SOCIAL STUDIES": [
                                "SST",
                                "S.ST.",
                                "SOCIAL STUDIES",
                                "SOCIAL SCIENCE",
                            ],
                            # Tech/Computers
                            "ARTIFICIAL INTELLIGENCE": [
                                "AI",
                                "ARTIFICIAL INTELLIGENCE",
                            ],
                            # Others
                            "PHYSICAL EDUCATION": ["PHE", "PHYSICAL EDUCATION"],
                            "GENERAL KNOWLEDGE": ["GK", "GENERAL KNOWLEDGE"],
                            "MISC": ["MSC", "M.SC.", "M.SC"],
                            "DRAWING": ["DRAWING", "DRAW"],
                            "GAMES": ["GAME", "GAMES", "SPORTS"],
                        }

                        # Normalize the period subject we're looking for
                        period_subject_normalized = search_subject.upper().strip()

                        # Debug output
                        print(
                            f"Checking if teacher {teacher['name']} (ID: {teacher['teacher_id']}) with subjects: {all_teacher_subjects} can teach period subject: {period_subject_normalized}"
                        )

                        # Check if teacher can teach this subject
                        is_qualified = False

                        # Find the standardized form of the period subject
                        standardized_period_subject = None
                        for std_subject, variations in subject_mapping.items():
                            if period_subject_normalized in variations:
                                standardized_period_subject = std_subject
                                print(
                                    f"Normalized period subject {period_subject_normalized} to standard form: {standardized_period_subject}"
                                )
                                break
                            # Check for substring matches
                            for variation in variations:
                                if variation in period_subject_normalized:
                                    standardized_period_subject = std_subject
                                    print(
                                        f"Substring match: Normalized period subject {period_subject_normalized} to standard form: {standardized_period_subject}"
                                    )
                                    break
                            if standardized_period_subject:
                                break

                        # If we couldn't normalize the period subject, use as is
                        if not standardized_period_subject:
                            standardized_period_subject = period_subject_normalized
                            print(
                                f"Using original period subject: {standardized_period_subject}"
                            )

                        # Now check if any of the teacher's subjects can teach this standardized subject
                        for teacher_subject in teacher_subjects_list:
                            # Check if this teacher subject appears directly in the standardized form
                            direct_match = False
                            for std_subject, variations in subject_mapping.items():
                                if (
                                    teacher_subject in variations
                                    and std_subject == standardized_period_subject
                                ):
                                    direct_match = True
                                    print(
                                        f"MATCH: Teacher subject {teacher_subject} is a direct match for {standardized_period_subject}"
                                    )
                                    break

                                # Also check substring matches
                                for variation in variations:
                                    if (
                                        variation in teacher_subject
                                        or teacher_subject in variation
                                    ) and std_subject == standardized_period_subject:
                                        direct_match = True
                                        print(
                                            f"MATCH: Teacher subject {teacher_subject} is a substring match for {standardized_period_subject}"
                                        )
                                        break

                            if direct_match:
                                is_qualified = True
                                break

                        if is_qualified:
                            print(
                                f"QUALIFIED: Teacher {teacher['name']} (ID: {teacher['teacher_id']}) can teach {standardized_period_subject}"
                            )
                        else:
                            print(
                                f"NOT QUALIFIED: Teacher {teacher['name']} (ID: {teacher['teacher_id']}) cannot teach {standardized_period_subject}"
                            )

                        if is_qualified:
                            qualified_teachers.append(teacher)

                    if qualified_teachers:
                        # Create DataFrame from qualified teachers
                        filtered_teachers = pd.DataFrame(qualified_teachers)
                    elif match_subject:
                        # If no qualified teachers, keep the filtered_teachers empty to move to next search criteria
                        filtered_teachers = pd.DataFrame()

                if not filtered_teachers.empty:
                    # If we have multiple matching teachers, sort by workload if the feature is available
                    if len(filtered_teachers) > 1:
                        try:
                            # Get workload for each teacher
                            workloads = []
                            for _, teacher in filtered_teachers.iterrows():
                                teacher_id = teacher["teacher_id"]
                                # Check if workload tracking is available
                                if hasattr(self, "get_teacher_workload"):
                                    workload = self.get_teacher_workload(teacher_id)
                                    workloads.append(
                                        {"teacher_id": teacher_id, "workload": workload}
                                    )
                                else:
                                    # Fallback - just use the first teacher
                                    workloads.append(
                                        {
                                            "teacher_id": teacher["teacher_id"],
                                            "workload": 0,
                                        }
                                    )

                            # Sort by workload (ascending)
                            workloads.sort(key=lambda x: x["workload"])

                            # Get teacher with lowest workload
                            teacher_id = workloads[0]["teacher_id"]
                            selected_teacher = filtered_teachers[
                                filtered_teachers["teacher_id"] == teacher_id
                            ].iloc[0]

                            replacement_id = selected_teacher["teacher_id"]
                            replacement_category = selected_teacher["category"]
                            replacement_name = selected_teacher["name"]
                        except Exception as e:
                            # Fallback if workload balancing fails
                            print(
                                f"Workload balancing error: {str(e)}, using first available teacher"
                            )
                            replacement_id = filtered_teachers.iloc[0]["teacher_id"]
                            replacement_category = filtered_teachers.iloc[0]["category"]
                            replacement_name = filtered_teachers.iloc[0]["name"]
                    else:
                        # Just one teacher
                        replacement_id = filtered_teachers.iloc[0]["teacher_id"]
                        replacement_category = filtered_teachers.iloc[0]["category"]
                        replacement_name = filtered_teachers.iloc[0]["name"]

                    # Increment the workload counter for this teacher if feature is available
                    try:
                        if hasattr(self, "update_teacher_workload"):
                            self.update_teacher_workload(replacement_id)
                    except Exception as e:
                        print(
                            f"Could not update workload counter: {str(e)}"
                        )  # Just log error and continue

                    print(
                        f"Found replacement ({quality}): {replacement_id} ({replacement_name}, {replacement_category})"
                    )
                    return (
                        replacement_id,
                        replacement_category,
                        replacement_name,
                        absent_teacher_name,
                    )

            # If no replacement found after all search criteria
            print(f"No suitable replacement found for period {period}")
            return None, None, None, None

        except Exception as e:
            print(f"Error finding replacement: {str(e)}")
            import traceback

            traceback.print_exc()
            return None, None, None, None

    def create_arrangements(self, absent_teacher_id, current_date):
        """Create arrangements for an absent teacher based on teacher categories (PGT/TGT/PRT)"""
        print(
            f">>> DEBUG: Inside create_arrangements for teacher: {absent_teacher_id}, Date: {current_date}"
        )
        try:
            schedules = self.load_teacher_schedules()
            users_df = pd.read_csv(self.users_file)

            # Get absent teacher details
            absent_teacher = schedules[
                schedules["teacher_id"] == absent_teacher_id
            ].iloc[0]

            # Get absent teacher's name from schedule
            absent_teacher_name = absent_teacher["name"]  # Get teacher name

            # Get absent teacher's category from users.csv
            user_row = users_df[users_df["teacher_id"] == absent_teacher_id]
            if not user_row.empty:
                absent_category = user_row.iloc[0]["category"]
            else:
                # Fallback to category from schedule if not found in users.csv
                absent_category = absent_teacher["category"]

            print(
                f"Creating arrangements for {absent_teacher_id} ({absent_teacher_name}), Category: {absent_category}"
            )

            arrangements = []
            # Check each period
            for period in range(1, 8):  # 7 periods as per the schedule
                period_col = f"period{period}"
                class_name = absent_teacher[period_col]
                print(f">>> DEBUG: Checking Period {period}, Class: {class_name}")

                # Skip if the teacher has a free period
                if class_name == "FREE":
                    print(f"Teacher has free period {period}, no arrangement needed")
                    continue

                # Find a replacement teacher for this period
                replacement_result = self.find_replacement_teacher(
                    absent_teacher_id, period
                )
                if replacement_result is not None and len(replacement_result) == 4:
                    (
                        replacement_id,
                        replacement_category,
                        replacement_name,
                        absent_name,
                    ) = replacement_result

                    if replacement_id:
                        # Create an arrangement for this period
                        arrangement = {
                            "date": current_date,
                            "absent_teacher": absent_teacher_id,
                            "absent_name": absent_name,  # Add absent teacher name
                            "absent_category": absent_category,
                            "replacement_teacher": replacement_id,
                            "replacement_name": replacement_name,  # Add replacement teacher name
                            "replacement_category": replacement_category,
                            "class": class_name,
                            "period": period,
                            "status": "ASSIGNED",  # Changed from PENDING to ASSIGNED
                            "match_quality": self._determine_match_quality(
                                absent_category,
                                replacement_category,
                                absent_teacher["subject"],
                                schedules.loc[
                                    schedules["teacher_id"] == replacement_id, "subject"
                                ].iloc[0],
                            ),
                        }
                        print(f"Created arrangement: {arrangement}")
                        arrangements.append(arrangement)
                    else:
                        print(f"Could not find replacement for period {period}")
                else:
                    print(f"Failed to get replacement information for period {period}")

            # Save the created arrangements
            if arrangements:
                self._save_arrangements(arrangements)
                print(f"Saved {len(arrangements)} arrangements for {absent_teacher_id}")
                return True
            else:
                print(f"No arrangements created for {absent_teacher_id}")
                return False

        except Exception as e:
            print(f"Error creating arrangements: {str(e)}")
            import traceback

            traceback.print_exc()
            return False

    def _determine_match_quality(
        self, absent_category, replacement_category, absent_subject, replacement_subject
    ):
        """
        Determine the quality of the match based on categories and subjects

        Priority for PGT: PGT (same subject) → TGT (same subject) → PGT (any free)
        Priority for TGT: TGT (same subject) → PRT (same subject) → TGT (any free)
        Priority for PRT: PRT (same subject) → TGT (same subject) → PRT (any free)
        """
        # Same category, same subject - Ideal match
        if (
            absent_category == replacement_category
            and absent_subject == replacement_subject
        ):
            return "Ideal"

        # For PGT teacher: TGT with same subject - Acceptable match
        if (
            absent_category == "PGT"
            and replacement_category == "TGT"
            and absent_subject == replacement_subject
        ):
            return "Acceptable"

        # For TGT teacher: PRT with same subject - Acceptable match
        if (
            absent_category == "TGT"
            and replacement_category == "PRT"
            and absent_subject == replacement_subject
        ):
            return "Acceptable"

        # For PRT teacher: TGT with same subject - Acceptable match
        if (
            absent_category == "PRT"
            and replacement_category == "TGT"
            and absent_subject == replacement_subject
        ):
            return "Acceptable"

        # Same category, different subject - Suboptimal match
        if absent_category == replacement_category:
            return "Suboptimal"

        # Different category, different subject - Last resort
        return "Last Resort"

    def _save_arrangements(self, new_arrangements):
        """Save new arrangements to the arrangements file"""
        try:
            # Read existing arrangements
            if os.path.exists(self.arrangements_file):
                arrangements_df = pd.read_csv(self.arrangements_file)
            else:
                columns = [
                    "date",
                    "absent_teacher",
                    "absent_name",
                    "absent_category",
                    "replacement_teacher",
                    "replacement_name",
                    "replacement_category",
                    "class",
                    "period",
                    "status",
                    "match_quality",
                ]
                arrangements_df = pd.DataFrame(columns=columns)

            # Convert new arrangements to DataFrame
            new_arrangements_df = pd.DataFrame(new_arrangements)

            # Append new arrangements
            arrangements_df = pd.concat(
                [arrangements_df, new_arrangements_df], ignore_index=True
            )

            # Save to file
            arrangements_df.to_csv(self.arrangements_file, index=False)
            return True
        except Exception as e:
            print(f"Error saving arrangements: {str(e)}")
            return False

    def mark_attendance(self, teacher_id, status, timestamp, is_auto=False):
        """Mark attendance for a teacher and create arrangements if absent"""
        if status not in ["present", "absent"]:
            return  # Skip if status is invalid or teacher not selected
        try:
            attendance_df = pd.read_csv(self.attendance_file)
            new_attendance = pd.DataFrame(
                {
                    "teacher_id": [teacher_id],
                    "date": [timestamp.split()[0]],
                    "status": [status],
                    "timestamp": [timestamp],
                    "is_auto": [is_auto],
                }
            )
            attendance_df = pd.concat(
                [attendance_df, new_attendance], ignore_index=True
            )
            attendance_df.to_csv(self.attendance_file, index=False)

            # Create arrangements if teacher is marked absent
            if status == "absent":
                print(
                    f">>> DEBUG: Teacher {teacher_id} marked absent. Calling create_arrangements for date {timestamp.split()[0]}..."
                )
                self.create_arrangements(teacher_id, timestamp.split()[0])

            return True
        except Exception as e:
            print(f"Error marking attendance: {str(e)}")
            return False

    def get_user_details(self, username):
        """Get user details by username"""
        try:
            users_df = pd.read_csv(self.users_file)
            user = users_df[users_df["username"] == username]
            if not user.empty:
                return user.iloc[0].to_dict()
        except Exception:
            pass
        return None

    def get_attendance(self, teacher_id, date_str):
        """Get attendance for a teacher on a specific date"""
        try:
            attendance_df = pd.read_csv(self.attendance_file)
            record = attendance_df[
                (attendance_df["teacher_id"] == teacher_id)
                & (attendance_df["date"] == date_str)
            ]
            if not record.empty:
                return record.iloc[0].to_dict()
        except Exception:
            pass
        return None

    def has_attendance(self, teacher_id, date_str):
        """Check if attendance is marked for a teacher on a specific date"""
        return self.get_attendance(teacher_id, date_str) is not None

    def get_present_teachers(self, date_str):
        """Get list of present teachers for a specific date"""
        try:
            attendance_df = pd.read_csv(self.attendance_file)
            present = attendance_df[
                (attendance_df["date"] == str(date_str))
                & (attendance_df["status"] == "present")
            ]
            return present["teacher_id"].tolist()
        except Exception:
            return []

    def get_absent_teachers(self, date_str):
        """Get list of absent teachers for a specific date"""
        try:
            attendance_df = pd.read_csv(self.attendance_file)
            absent = attendance_df[
                (attendance_df["date"] == str(date_str))
                & (attendance_df["status"] == "absent")
            ]
            return absent["teacher_id"].tolist()
        except Exception:
            return []

    def get_recent_attendance(self, limit=20):
        """Get recent attendance records"""
        try:
            attendance_df = pd.read_csv(self.attendance_file)
            return attendance_df.sort_values("timestamp", ascending=False).head(limit)
        except Exception:
            return pd.DataFrame()

    def get_todays_arrangements(self):
        """Get arrangements for today"""
        try:
            arrangements_df = pd.read_csv(self.arrangements_file)
            today = date.today()
            return arrangements_df[arrangements_df["date"] == str(today)]
        except Exception:
            return pd.DataFrame()

    def suspend_arrangements(self, date):
        """Suspend arrangements for a specific date"""
        try:
            suspended_df = pd.read_csv(self.suspended_dates_file)
            if str(date) not in suspended_df["date"].values:
                suspended_df = pd.concat(
                    [suspended_df, pd.DataFrame({"date": [str(date)]})],
                    ignore_index=True,
                )
                suspended_df.to_csv(self.suspended_dates_file, index=False)
            return True
        except Exception:
            return False

    def resume_arrangements(self, date):
        """Resume arrangements for a specific date"""
        try:
            suspended_df = pd.read_csv(self.suspended_dates_file)
            suspended_df = suspended_df[suspended_df["date"] != str(date)]
            suspended_df.to_csv(self.suspended_dates_file, index=False)
            return True
        except Exception:
            return False

    def is_arrangement_suspended(self, date):
        """Check if arrangements are suspended for a specific date"""
        try:
            suspended_df = pd.read_csv(self.suspended_dates_file)
            return str(date) in suspended_df["date"].values
        except Exception:
            return False

    def get_todays_attendance(self):
        """Get today's attendance records"""
        try:
            attendance_df = pd.read_csv(self.attendance_file)
            today = date.today()
            return attendance_df[attendance_df["date"] == str(today)]
        except Exception as e:
            print(f"Error getting today's attendance: {str(e)}")
            return pd.DataFrame()

    def get_all_teachers(self):
        """Get list of all teachers"""
        try:
            users_df = pd.read_csv(self.users_file)
            teachers = users_df[users_df["role"] == "teacher"]
            return teachers.to_dict("records")
        except Exception:
            return []

    def create_manual_arrangement(
        self,
        absent_teacher_id,
        replacement_teacher_id,
        period,
        class_name,
        current_date=None,
    ):
        """Create a manual arrangement for a specific period"""
        try:
            # Use today's date if not specified
            if current_date is None:
                current_date = str(date.today())

            users_df = pd.read_csv(self.users_file)

            # Get absent teacher's category
            absent_teacher_details = users_df[
                users_df["teacher_id"] == absent_teacher_id
            ]
            if not absent_teacher_details.empty:
                absent_category = absent_teacher_details.iloc[0]["category"]
            else:
                absent_category = "UNKNOWN"

            # Get replacement teacher's category
            replacement_details = users_df[
                users_df["teacher_id"] == replacement_teacher_id
            ]
            replacement_category = "UNKNOWN"
            if not replacement_details.empty:
                replacement_category = replacement_details.iloc[0]["category"]

            # Determine assignment quality based on category matching
            status = "manually_assigned"
            if absent_category == replacement_category:
                match_quality = "ideal"
            elif absent_category == "PGT" and replacement_category == "TGT":
                match_quality = "acceptable"
            elif absent_category == "TGT" and replacement_category == "PRT":
                match_quality = "acceptable"
            else:
                match_quality = "suboptimal"

            # Create and save the arrangement
            arrangement = {
                "date": current_date,
                "absent_teacher": absent_teacher_id,
                "absent_category": absent_category,
                "replacement_teacher": replacement_teacher_id,
                "replacement_category": replacement_category,
                "class": class_name,
                "period": period,
                "status": status,
                "match_quality": match_quality,
            }

            # Create a new dataframe with the arrangement
            arrangement_df = pd.DataFrame([arrangement])

            # Read existing arrangements
            existing_df = pd.read_csv(self.arrangements_file)

            # Add new columns to existing dataframe if they don't exist
            for col in arrangement_df.columns:
                if col not in existing_df.columns:
                    existing_df[col] = ""

            # Concatenate and save
            updated_df = pd.concat([existing_df, arrangement_df], ignore_index=True)
            updated_df.to_csv(self.arrangements_file, index=False)

            print(
                f"Created manual arrangement: {absent_teacher_id} replaced by {replacement_teacher_id} for period {period}, class {class_name}"
            )
            return True

        except Exception as e:
            print(f"Error creating manual arrangement: {str(e)}")
            import traceback

            traceback.print_exc()
            return False

    # def get_todays_arrangement(self):
    #     """Get all arrangements"""
    #     try:
    #         arrangements_df = pd.read_csv(self.arrangements_file)
    #         return arrangements_df.to_dict("records")
    #     except Exception:
    #         return []
    def update_teacher_workload(self, teacher_id, increment=1):
        """Update the workload counter for a teacher"""
        print(f"--- DEBUG: Inside update_teacher_workload for {teacher_id} ---")
        try:
            # Create the workload file if it doesn't exist
            if not os.path.exists(self.workload_file):
                workload_df = pd.DataFrame(columns=["teacher_id", "workload_count"])
                workload_df.to_csv(self.workload_file, index=False)

            # Read current workload counters
            workload_df = pd.read_csv(self.workload_file)

            # Check if teacher already exists in workload counter
            if teacher_id in workload_df["teacher_id"].values:
                # Update existing teacher's count
                current_count = workload_df.loc[
                    workload_df["teacher_id"] == teacher_id, "workload_count"
                ].iloc[0]
                workload_df.loc[
                    workload_df["teacher_id"] == teacher_id, "workload_count"
                ] = (current_count + increment)
            else:
                # Add new teacher with initial count
                new_row = pd.DataFrame(
                    {"teacher_id": [teacher_id], "workload_count": [increment]}
                )
                workload_df = pd.concat([workload_df, new_row], ignore_index=True)

            # Save updated workload counters
            workload_df.to_csv(self.workload_file, index=False)
            return True
        except Exception as e:
            print(f"Error updating teacher workload: {str(e)}")
            return False

    def get_teacher_workload(self, teacher_id):
        """Get the current workload count for a teacher"""
        print(f"--- DEBUG: Inside get_teacher_workload for {teacher_id} ---")
        try:
            if not os.path.exists(self.workload_file):
                return 0

            workload_df = pd.read_csv(self.workload_file)
            if teacher_id in workload_df["teacher_id"].values:
                return workload_df.loc[
                    workload_df["teacher_id"] == teacher_id, "workload_count"
                ].iloc[0]
            return 0
        except Exception as e:
            print(f"Error getting teacher workload: {str(e)}")
            return 0
