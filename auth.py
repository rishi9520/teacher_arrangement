import hashlib
import pandas as pd
import os
from notifications import NotificationManager
import firebase_admin
from firebase_admin import credentials, auth

notification_manager = NotificationManager()


def send_password_reset_otp(phone_number):
    """Send OTP to Phone for Password Reset"""
    return notification_manager.send_otp(phone_number)


def verify_password_reset_otp(session_info, otp):
    """Verify OTP"""
    return notification_manager.verify_otp(session_info, otp)


def reset_password(phone_number, new_password):
    """Reset Password after OTP Verification"""
    try:
        user = auth.get_user_by_phone_number(phone_number)
        auth.update_user(user.uid, password=new_password)
        return True
    except Exception as e:
        print(f"Error resetting password: {str(e)}")
        return False


def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(username, password):
    """Verify username and password"""
    try:
        users_df = pd.read_csv("attached_assets/users.csv")
        user = users_df[users_df["username"] == username]
        if not user.empty:
            return user.iloc[0]["password"] == hash_password(password)
    except Exception:
        pass
    return False


def register_user(username, password, name, phone, teacher_id, role):
    """Register a new user"""
    try:
        # Create users.csv if it doesn't exist
        if not os.path.exists("attached_assets/users.csv"):
            pd.DataFrame(
                columns=["username", "password", "name", "phone", "teacher_id", "role"]
            ).to_csv("attached_assets/users.csv", index=False)

        users_df = pd.read_csv("attached_assets/users.csv")

        # Check if username exists
        if username in users_df["username"].values:
            return False

        # Add new user
        new_user = pd.DataFrame(
            {
                "username": [username],
                "password": [hash_password(password)],
                "name": [name],
                "phone": [phone],
                "teacher_id": [teacher_id],
                "role": [role],
            }
        )

        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv("attached_assets/users.csv", index=False)
        return True

    except Exception as e:
        print(f"Error registering user: {str(e)}")
        return False


# def send_password_reset_otp(phone):
#     """Send OTP for password reset using Firebase"""
#     try:
#         # Generate verification code through Firebase
#         session_info = notification_manager.get_verification_code(phone)
#         if session_info:
#             return session_info
#     except Exception:
#         pass
#     return None

# def verify_reset_otp(session_info, code):
#     """Verify OTP using Firebase"""
#     try:
#         phone_number = notification_manager.verify_phone_number(session_info, code)
#         return phone_number is not None
#     except Exception:
#         return False

# def reset_password(phone, new_password):
#     """Reset user password after OTP verification"""
#     try:
#         users_df = pd.read_csv('attached_assets/users.csv')
#         mask = users_df['phone'] == phone
#         if mask.any():
#             users_df.loc[mask, 'password'] = hash_password(new_password)
#             users_df.to_csv('attached_assets/users.csv', index=False)
#             return True
#     except Exception:
#         pass
#     return False


def get_user_role(username):
    """Get user role"""
    try:
        users_df = pd.read_csv("attached_assets/users.csv")
        user = users_df[users_df["username"] == username]
        if not user.empty:
            return user.iloc[0]["role"]
    except Exception:
        pass
    return None
