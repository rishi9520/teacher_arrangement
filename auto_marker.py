import schedule
import time
import threading
import pandas as pd
from datetime import datetime
import os


class AutoMarker:
    def __init__(self, data_manager, ui_update_callback=None):
        self.data_manager = data_manager
        self.ui_update_callback = (
            ui_update_callback  # UI ko update karne ke liye callback
        )
        self.timing_file = "configs/timing.csv"
        self.running = False
        self._init_configs()

    def _init_configs(self):
        """Initialize configuration files if they don't exist"""
        if not os.path.exists("configs"):
            os.makedirs("configs")

        if not os.path.exists(self.timing_file):
            pd.DataFrame(
                {"hour": [14], "minute": [0], "enabled": [True]}  # Default 2 PM
            ).to_csv(self.timing_file, index=False)

    def get_timing(self):
        """Get current auto-mark timing"""
        try:
            df = pd.read_csv(self.timing_file)
            if not df.empty:
                return {
                    "hour": int(df.iloc[0]["hour"]),
                    "minute": int(df.iloc[0]["minute"]),
                    "enabled": bool(df.iloc[0]["enabled"]),
                }
        except Exception as e:
            print(f"Error reading timing file: {e}")

        return {"hour": 14, "minute": 0, "enabled": True}  # Default

    def set_timing(self, hour, minute, enabled=True):
        """Set auto-mark timing"""
        pd.DataFrame({"hour": [hour], "minute": [minute], "enabled": [enabled]}).to_csv(
            self.timing_file, index=False
        )
        self.restart_scheduler()

    def mark_absences(self):
        """Mark all unmarked teachers as absent"""
        timing = self.get_timing()
        if not timing["enabled"]:
            print("Auto-marking disabled.")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        teachers = self.data_manager.get_all_teachers()

        if not teachers:
            print("No teachers found!")
            return

        for teacher in teachers:
            if self.data_manager.has_attendance(teacher["teacher_id"], today):
                print(f"Attendance already marked for {teacher['teacher_id']}")
                continue

            print(f"Marking {teacher['teacher_id']} as absent.")
            self.data_manager.mark_attendance(
                teacher["teacher_id"],
                "absent",
                f"{today} {datetime.now().strftime('%H:%M:%S')}",
                is_auto=True,
            )

        # ✅ UI ko update karo
        if self.ui_update_callback:
            self.ui_update_callback()

    def schedule_job(self):
        """Schedule the auto-marking job"""
        timing = self.get_timing()
        job_time = f"{timing['hour']:02d}:{timing['minute']:02d}"
        print(f"Scheduling auto-marking at {job_time}")

        schedule.clear()  # Ensure only one job is scheduled at a time
        schedule.every().day.at(job_time).do(self.mark_absences)

    def start(self):
        """Start the auto-marker thread"""
        if not self.running:
            print("Starting AutoMarker...")
            self.running = True
            self.schedule_job()
            threading.Thread(target=self._run_scheduler, daemon=True).start()

    def stop(self):
        """Stop the auto-marker"""
        print("Stopping AutoMarker...")
        self.running = False

    def restart_scheduler(self):
        """Restart the scheduler with new timing"""
        print("Restarting scheduler...")
        schedule.clear()
        self.schedule_job()

    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            for _ in range(30):  # Instead of time.sleep(30)
                if not self.running:
                    return
                time.sleep(1)
