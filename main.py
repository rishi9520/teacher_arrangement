import streamlit as st

st.set_page_config(
    page_title="Teacher Arrangement System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)
import pandas as pd
import os
import pathlib
from streamlit_lottie import st_lottie
import re
import json
from utils.auth import check_password, register_user, send_password_reset_otp, reset_password, get_user_role
from data_manager import DataManager
from utils.theme import initialize_theme, toggle_theme, apply_theme
from components.dashboard import render_dashboard
from components.admin_controls import render_admin_page
from components.reports import render_reports_page
from components.arrangements import render_arrangements_page
from components.schedule_manager import render_schedule_manager_page
from components.substitute_pool import render_substitute_pool_page
from components.coverage_tracking import render_coverage_tracking_page

# from components.contact import render_contact_page
from components.legal_pages import render_terms_and_conditions, render_contact_page

# import firebase_admin
from streamlit.components.v1 import html


def load_svg(file_path):
    with open(file_path, "r") as f:
        return f.read()


def serve_static_file(filename):
    filepath = os.path.join("static", filename)
    with open(filepath, "r", encoding="utf-8") as file:
        st.markdown(
            f'<script type="application/json" id="{filename}">{file.read()}</script>',
            unsafe_allow_html=True,
        )


serve_static_file("manifest.json")


# Helper function to wrap SVG with styles
def svg_with_style(svg_content, color="currentColor", size=24):
    colored_svg = svg_content.replace('stroke="currentColor"', f'stroke="{color}"')
    return f"""<div style="display: inline-block; width: {size}px; height: {size}px;">{colored_svg}</div>"""


# Load a lottie animation file
def load_lottie_file(filepath):
    try:
        if pathlib.Path(filepath).exists():
            with open(filepath, "r") as f:
                return json.load(f)
        else:
            return None
    except Exception as e:
        print(f"Error loading animation: {e}")
        return None


if "initialized" not in st.session_state:
    st.session_state["initialized"] = True

st.markdown(
    """
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js')
        .then(() => console.log('Service Worker Registered'))
        .catch(err => console.log('Service Worker Registration Failed:', err));
    }
</script>
""",
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <style>
     /* Default header styling */
    header[data-testid="stHeader"] {{
        display: flex ;
        background: linear-gradient(45deg, #1E3A8A, #3B82F6);
        padding: 10px !important;
        box-shadow: 0 0 10px rgba(0,0,0,0. 1) !important;
        height:50px;
        align-items: center;
        text-align:center;
        justy
        }}
    button[data-testid="stBaseButton-secondaryFormSubmit"] {{
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        color: white !important; /* Optional: Change text color for better contrast */
        border: none !important; /* Optional: Remove border if needed */
}}    
    header[data-testid="stHeader"] span {{
        display: flex ;
        color: white !important ;
        }}       
    svg {{
        fill:black!important;  /* Change to any color */
    }}  

        section[data-testid="stSidebar"] img {{
        margin-top: -40px !important;
        margin-left: 70px;
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.3));
        transition: all 0.3s ease;
    }}
    .custom-image {{
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.3));
        transition: all 0.3s ease;
    }}
    
    .custom-image:hover {{
     transform: scale(1.05);
    }}

    section[data-testid="stSidebar"] img:hover {{
        transform: scale(1.05);
    }}
     /* Sidebar background gradient */
    [data-testid="stSidebar"] {{
            position: fixed !important;
            height: 100vh !important;
            top: 0;
            left: 0;
            width: 300px !important; 
            background: linear-gradient(135deg, #4568dc, #b06ab3)!important;
            color: #141212 ;
            overflow-x: auto !important; /* Scroll enable */
    }}
        .st-bde5z3 .st-bpb {{
        background-color: #4CAF50 !important; /* Green */
        color: white !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }}

        div[data-testid="stAppViewContainer"] {{
            margin-left: 259px ;
            margin-right:;
            margin-top:-20px;
        }}

    

# section[data-testid="stSidebar"] {{
#     display: flex !important;
#     flex-direction: column; /* Ensure vertical stacking */
#     align-items: center !important; /* Center the content horizontally */
# }}
    section[data-testid="stSidebar"] img {{
    margin-top: -40px!important;
    margin-left:70px;
    }}
    [data-testid="stSidebar"] button {{
    background-color:#FFFFFF1A !important;
    font-weight: 700 !important;
}}
\
.st-emotion-cache-fvlxsx p {{
    font-weight: bold;
}}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <script>
    window.onload = function() {
        var buttons = document.querySelectorAll('button[kind="secondary"].st-emotion-cache-1r6p0uf.e1d5ycv52');
        buttons.forEach(function(button) {
            button.style.backgroundColor = 'green';
            button.style.color = 'white';
            button.style.fontWeight = 'bold';
        });
    };
    </script>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
            <style>
                div[data-testid="stHorizontalBlock"] button {
                    font-weight: bold !important;
                }
                button[kind="secondary"].st-emotion-cache-1r6p0uf.e1d5ycv52 p {
                       /* Aapka desired font color */
                font-weight: 600 !important;   /* Bold font */
                font-size:17px
} 
button[data-testid="stBaseButton-headerNoPadding"] svg.st-emotion-cache-1b2ybtsex0cdmw0 {
    fill: white !important;
}         
            </style>
        """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        body { font-family: 'Poppins', sans-serif; }

        * {
            color: #2E2E2E; /* Dark Gray */
        }
        .stButton > button {
            font-weight: 700 !important;
            color: #d32f2f !important;
            background-color:#;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        button {
            font-weight: 700;}
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            color:d32f2f;
        }

        .stTextInput > div > div > input {
            background-color: #E0E0E0 ;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: #2e7d32;
            box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.2);
        }

        .error-message {
            color: #FFD700;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.image(
    "attached_assets/logo.png",
    width=100,
)

# # Ya phir header me logo lagane ke liye
# st.image("attached_assets/logo.png", )


# Lottie Animation Function
# def load_lottie_file(filepath: str):
#     with open(filepath, "r") as f:
#         return json.load(f)


# lottie_animation = load_lottie_file("attached_assets/lottie_animation.json")
# st_lottie(lottie_animation, height=300)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "data_manager" not in st.session_state:
    st.session_state.data_manager = DataManager()
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"
if "reset_password_mode" not in st.session_state:
    st.session_state.reset_password_mode = False
if "reset_otp" not in st.session_state:
    st.session_state.reset_otp = None
if "reset_phone" not in st.session_state:
    st.session_state.reset_phone = None

# Initialize theme
initialize_theme()
apply_theme()

with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; margin-bottom: 20px;margin-left:8px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="sidebar-icon" viewBox="0 0 16 16">
                <path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3a.5.5 0 0 0 .372 0L14 7.14V13a1 1 0 0 0-1 1v2h3v-2a1 1 0 0 0-1-1V6.739l.686-.275a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/>
                <path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .294.605l4.5 1.8a.5.5 0 0 0 .372 0l4.5-1.8a.5.5 0 0 0 .294-.605l-.5-1.7a.5.5 0 0 0-.656-.327L8 10.466 4.176 9.032Z"/>
            </svg>
            <h2 style="margin: 0;margin-left:10px; padding: 0; background:transparent;">Teacher Attendance</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.authenticated:
        if "dark_mode" not in st.session_state:
            st.session_state.dark_mode = False  # Default light mode

        # Toggle theme function
        def toggle_theme():
            st.session_state.dark_mode = not st.session_state.dark_mode

        # Theme ke hisaab se icon, text aur font style select karna
        if st.session_state.dark_mode:
            icon = ":material/light_mode:"  # Sun icon
            button_text = "Enable Light Mode"
            background_color = "#121212"
            text_color = "#E0E0E0"
            font_family = "'Fira Code', monospace"  # Dark Mode ke liye alag font
        else:
            icon = ":material/dark_mode:"  # Moon icon
            button_text = "Enable Dark Mode"
            background_color = "#f2f2f2"
            text_color = "#333333"
            font_family = "'Inter', sans-serif"  # Light Mode ke liye alag font

        # Toggle button
        if st.button(
            f"{icon} {button_text}",
            key="toggle_theme",
            use_container_width=True,
            on_click=toggle_theme,
        ):
            st.rerun()  # UI update karne ke liye page reload karna

        # Background, text color, aur font style apply karna
        theme_style = f"""
    <style>
        body, .main, .stApp {{
            background-color: {background_color} !important;
            color: {text_color} !important;
            font-family: {font_family} !important;
        }}
        .stButton>button {{
            # background-color: #444 !important;
            color: white !important;
            font-size: 16px !important;
            font-weight: bold !important;
            border-radius: 5px;
        }}
        # .stButton>button:hover {{
        #   background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        # }}
    </style>
"""
        st.markdown(theme_style, unsafe_allow_html=True)

        st.divider()
        # Navigation
        st.markdown(
            "<h2 style='text-align: center;background:transparent;'>Navigation</h2>",
            unsafe_allow_html=True,
        )
        # (Aapka pages dictionary yahaan...)
        pages = {
            "dashboard": (":material/dashboard:", "Dashboard"),
            "admin": (":material/admin_panel_settings:", "Administrative Controls"),
            "arrangements": (":material/swap_horiz:", "Arrangements"),
            "reports": (":material/bar_chart:", "Reports"),
            "schedule_manager": (":material/edit_calendar:", "Schedule Manager"),
            "substitute_pool": (":material/people_alt:", "Substitute Teachers"),
            "coverage_tracking": (":material/analytics:", "Class Coverage"),
            "terms": (":material/gavel:", "Terms & Conditions"),
            "contact": (":material/contact_phone:", "Contact Us"),
        }

        for page, (icon, label_text) in pages.items():
            display_label = f"{icon} {label_text}"
            if st.button(display_label, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
            # st.markdown("</div>", unsafe_allow_html=True)
        st.divider()
        st.markdown(
            """
                <style>
                .profile-card {
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border-radius: 16px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    color: white;
                    position: relative;
                    overflow: hidden;
                    transition: all 0.3s ease;
                }
                
                .profile-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
                }
                
                .profile-card::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
                    opacity: 0;
                    transition: opacity 0.5s ease;
                    z-index: 0;
                    pointer-events: none;
                }
                
                .profile-card:hover::before {
                    opacity: 1;
                }
                
                .profile-header {
                    display: flex;
                    align-items: center;
                    margin-bottom: 20px;
                    position: relative;
                    z-index: 1;
                }
                
                .profile-avatar {
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #4568dc, #b06ab3);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 15px;
                    font-size: 24px;
                    font-weight: 700;
                    color: white;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                    border: 3px solid rgba(255, 255, 255, 0.2);
                }
                
                .profile-title {
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin: 0;
                    color: white;
                    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                }

                .profile-subtitle {
                    font-size: 0.9rem;
                    opacity: 0.8;
                    margin: 5px 0 0 0;
                }
               
                 </style>
                """,
            unsafe_allow_html=True,
        )
        # User profile
        user_details = st.session_state.data_manager.get_user_details(
            st.session_state.user
        )
        first_letter = user_details["name"][0].upper() if user_details["name"] else "U"
        if user_details is not None:

            st.markdown(
                f"""<div class="profile-card">
                    <div class="profile-header">
                        <div class="profile-avatar">{first_letter}</div>
                        <div>
                            <h2 class="profile-title">{user_details['name']}</h2>
                            <p class="profile-subtitle">{user_details.get('role', 'teacher').title()}</p>
                        </div>
                    </div><div style='padding: 15px; border-radius: 10px;
                  margin-bottom: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);'>
               <h3>  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px;">
                        <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"/>
                    </svg><strong > Profile </strong></h3> 
               <p> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px;">
                        <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                    </svg>
                    <strong>Name:{user_details['name']}</strong> </p>
              <p> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px;">
                        <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>
                    </svg>
                    <strong>ID:{user_details['teacher_id']} </strong> </p>
               <p> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px;">
                        <path d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.568 17.568 0 0 0 4.168 6.608 17.569 17.569 0 0 0 6.608 4.168c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.678.678 0 0 0-.58-.122l-2.19.547a1.745 1.745 0 0 1-1.657-.459L5.482 8.062a1.745 1.745 0 0 1-.46-1.657l.548-2.19a.678.678 0 0 0-.122-.58L3.654 1.328zM1.884.511a1.745 1.745 0 0 1 2.612.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.678.678 0 0 0 .178.643l2.457 2.457a.678.678 0 0 0 .644.178l2.189-.547a1.745 1.745 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.634 18.634 0 0 1-7.01-4.42 18.634 18.634 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877L1.885.511z"/>
                    </svg>
                      <strong>Phone: {user_details['phone']} </strong> </p>
               <p>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px;">
                        <path d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"/>
                    </svg>
                    <strong> Role: {user_details.get('role', 'teacher').title()}</strong></p>

            """,
                unsafe_allow_html=True,
            )
            get_user_role = user_details.get("role", "teacher")  # Role fetch karna

        # Logout
        logout_icon = ":material/logout:"
        logout_label_text = "Logout"
        # Combine icon and text for the display label
        display_logout_label = f"{logout_icon} {logout_label_text}"
        # Add a unique key, e.g., "logout_button_key"
        if st.sidebar.button(
            display_logout_label,
            type="secondary",  # You have set it to secondary
            use_container_width=True,
            key="logout_button_key",  # ADD THIS KEY
        ):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()


# Main content
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <style>
        div[data-testid="stAppViewContainer"] {
            margin-top: -180px !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
if not st.session_state.authenticated:
    lottie_animation = load_lottie_file("attached_assets/lottie_animation.json")
    st_lottie(lottie_animation, height=130, key="dashboard_lottie")
    st.markdown(
        """
            
                <div style="text-align: center; margin-top: 20px;">
                    <h1 style="font-weight: 700;
                    background: linear-gradient(90deg, #1E3A8A, #3B82F6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                     display: inline-block; /* Important for text gradient */">Teacher Arrangement System</h1>
                    <p style=" font-weight: 600;
            color: #6c7293;
            font-size: 1.1rem;">"A comprehensive solution for attendance management and arrangement planning"</p>
                </div>
                """,
        unsafe_allow_html=True,
    )

    if st.session_state.reset_password_mode:
        # Password Reset Flow
        if st.session_state.reset_otp is None:
            # Step 1: Enter phone number
            with st.form("reset_password_form_1"):
                phone = st.text_input("Enter your registered phone number")
                submitted = st.form_submit_button("Send OTP")

                if submitted:
                    otp = send_password_reset_otp(phone)
                    if otp:
                        st.session_state.reset_otp = otp
                        st.session_state.reset_phone = phone
                        st.success("OTP sent successfully!")
                        st.rerun()
                    else:
                        st.error("Phone number not found or SMS service error!")
        else:
            # Step 2: Verify OTP and set new password
            with st.form("reset_password_form_2"):
                entered_otp = st.text_input("Enter OTP")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submitted = st.form_submit_button("Reset Password")

                if submitted:
                    if entered_otp == st.session_state.reset_otp:
                        if new_password == confirm_password:
                            if reset_password(
                                st.session_state.reset_phone, new_password
                            ):
                                st.success("Password reset successful! Please login.")
                                # Reset the password reset flow
                                st.session_state.reset_password_mode = False
                                st.session_state.reset_otp = None
                                st.session_state.reset_phone = None
                                st.rerun()
                            else:
                                st.error("Failed to reset password!")
                        else:
                            st.error("Passwords do not match!")
                    else:
                        st.error("Invalid OTP!")

        # Back to login
        if st.button("Back to Login"):
            st.session_state.reset_password_mode = False
            st.session_state.reset_otp = None
            st.session_state.reset_phone = None
            st.rerun()
    else:
        # Normal Login/Register Flow
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted:
                    if check_password(username, password):
                        st.session_state.authenticated = True
                        st.session_state.user = username
                        st.session_state.role = get_user_role(username)
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

            # Forgot Password link
            if st.button("Forgot Password?"):
                st.session_state.reset_password_mode = True
                st.rerun()

        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                name = st.text_input("Full Name")
                phone = st.text_input("Phone Number")
                teacher_id = st.text_input("Teacher ID")
                role = st.selectbox("Role", ["teacher", "admin"])

                submitted = st.form_submit_button("Register", use_container_width=True)
                # Users.csv ka path
                users_file = "attached_assets/users.csv"

                if not os.path.exists("attached_assets/users.csv"):
                    print("⚠️ users.csv file NOT FOUND! Creating a new one...")
                # CSV file ko DataFrame me load karo
                existing_users_df = pd.read_csv(users_file, dtype={"phone": str})

                # Data check karne ke liye print karo
                # print(existing_users_df.head())  # Pehle 5 rows dekho
                # Sirf username aur phone number wale columns ko extract karo
                user_info = existing_users_df[["username", "phone", "teacher_id"]]

                def is_username_taken(username):
                    return username in existing_users_df["username"].values

                # Function to check phone number validity
                def is_valid_phone(phone):
                    return (
                        phone.isdigit()
                        and len(phone) == 10
                        and phone not in existing_users_df["phone"].values
                    )

                # Function to check password strength
                def is_valid_password(password):
                    return len(password) >= 8

                # Function to validate teacher ID format
                def is_valid_teacher_id(teacher_id):
                    pattern = r"^T\d{3}$"  # "T" ke baad exactly 3 digits
                    return (
                        bool(re.fullmatch(pattern, teacher_id))
                        and teacher_id not in existing_users_df["teacher_id"].values
                    )

                if submitted:
                    errors = []
                    if (
                        not new_username
                        or not new_password
                        or not name
                        or not phone
                        or not teacher_id
                        or not role
                    ):
                        errors.append("❌  Please fill all reqirements!")

                        # Username validation
                    if is_username_taken(new_username):
                        errors.append(
                            "❌ This username is already taken. Please choose another."
                        )

                        # Phone validation
                    if not is_valid_phone(phone):
                        errors.append(
                            "❌ Enter a valid 10-digit phone number that is not already registered."
                        )

                        # Password validation
                    if not is_valid_password(new_password):
                        errors.append("❌ Password must be at least 8 characters long.")

                    if not is_valid_teacher_id(teacher_id):
                        errors.append(
                            "❌ Invalid Teacher ID! It should be in 'T000' format and unique."
                        )

                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        # ✅ **Register the user (important step)**
                        if register_user(
                            new_username, new_password, name, phone, teacher_id, role
                        ):
                            st.success("✅ Registration successful! Please login.")
                        else:
                            st.error(
                                "❌ Registration failed. Username might already exist."
                            )

else:
    # Render current page
    if st.session_state.current_page == "dashboard":
        render_dashboard(st.session_state.data_manager)
    elif st.session_state.current_page == "admin":
        render_admin_page(st.session_state.data_manager)
    elif st.session_state.current_page == "arrangements":
        render_arrangements_page(st.session_state.data_manager)
    elif st.session_state.current_page == "reports":
        render_reports_page(st.session_state.data_manager)
    elif st.session_state.current_page == "schedule_manager":
        render_schedule_manager_page(st.session_state.data_manager)
    elif st.session_state.current_page == "substitute_pool":
        render_substitute_pool_page()
    elif st.session_state.current_page == "coverage_tracking":
        render_coverage_tracking_page(st.session_state.data_manager)
    elif st.session_state.current_page == "contact":
        render_contact_page()
    elif st.session_state.current_page == "terms":
        render_terms_and_conditions()
