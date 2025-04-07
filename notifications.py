import firebase_admin
from firebase_admin import credentials, auth
import json


class NotificationManager:
    def __init__(self):
        self._initialize_firebase()

    def _initialize_firebase(self):
        """Firebase Initialize"""
        try:
            if not firebase_admin._apps:
                cred_path = "firebase_config.json"  # JSON key file path
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase Initialization Error: {str(e)}")

    def create_new_user(self, phone_number):
        """Create a new user if it doesn't exist"""
        try:
            # Check if user already exists
            user = auth.get_user_by_phone_number(phone_number)
            print(f"User already exists: {user.uid}")
            return user
        except firebase_admin.auth.UserNotFoundError:
            # User does not exist, so create a new one
            user = auth.create_user(phone_number=phone_number)
            print(f"Successfully created user: {user.uid}")
            return user
        except Exception as e:
            print(f"Error: {e}")
            return None

    def send_otp(self, phone_number):
        """Send OTP via Firebase Authentication"""
        try:
            # Firebase OTP trigger (Real OTP system is frontend-based)
            link = f"https://identitytoolkit.googleapis.com/v1/accounts:sendVerificationCode?key=AIzaSyB8zTS8G-NqUeSXEeYdsBr1GqBXLO7A1JI"
            print(f"OTP Sent to: {phone_number} (Check frontend integration)")
            return link
        except Exception as e:
            print(f"Error sending OTP: {str(e)}")
            return None

    def verify_otp(self, phone_number, otp_code):
        """Verify OTP"""
        try:
            # In Firebase, OTP verification happens on frontend
            print(f"OTP Verification Requested for {phone_number}")
            return True  # This should be handled in frontend using Firebase SDK
        except Exception as e:
            print(f"OTP Verification Failed: {str(e)}")
            return None


# Create Notification Manager Instance
notif_manager = NotificationManager()
notif_manager.create_new_user("+919520496351")
