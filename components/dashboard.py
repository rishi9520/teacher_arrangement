import streamlit as st
from data_manager import DataManager
import pandas as pd
from datetime import datetime, date, time
import json
import os
import plotly.graph_objects as go
import plotly.express as px
import logging
import calendar
from streamlit_lottie import st_lottie

# from PIL import Image
# import rembg


def get_calendar_dates():
    if "calendar_date" not in st.session_state:
        st.session_state.calendar_date = datetime.now()
    return st.session_state.calendar_date


def change_month(delta):
    current = get_calendar_dates()
    new_date = current.replace(day=1)
    if delta > 0:
        # Move to next month
        if new_date.month == 12:
            new_date = new_date.replace(year=new_date.year + 1, month=1)
        else:
            new_date = new_date.replace(month=new_date.month + 1)
    else:
        # Move to previous month
        if new_date.month == 1:
            new_date = new_date.replace(year=new_date.year - 1, month=12)
        else:
            new_date = new_date.replace(month=new_date.month - 1)
    st.session_state.calendar_date = new_date


def generate_calendar_days(current_date):
    cal = calendar.monthcalendar(current_date.year, current_date.month)
    html = ""
    today = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year

    # First add weekday headers
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for weekday in weekdays:
        html += f'<div class="calendar-weekday">{weekday}</div>'

    # Then add days
    for week in cal:
        for day in week:
            if day == 0:
                html += '<div class="calendar-day empty"></div>'
            elif (
                day == today
                and current_date.month == current_month
                and current_date.year == current_year
            ):
                html += f'<div class="calendar-day today">{day}</div>'
            else:
                html += f'<div class="calendar-day">{day}</div>'

    return html


def render_dashboard(data_manager):
    """Render the dashboard page"""
    user_details = data_manager.get_user_details(st.session_state.user)
    if not user_details:
        st.error("User details not found!")
        return

    today = date.today()
    current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format with AM/PM

    # Load and display Lottie animation
    def load_lottie_file(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    auto_timing = data_manager.get_arrangement_time()
    if auto_timing and isinstance(auto_timing, tuple) and len(auto_timing) == 2:
        auto_hour, auto_minute = auto_timing
    else:
        auto_hour, auto_minute = 10, 30  # Default

    # Today's date
    today_date = datetime.now().strftime("%A, %B %d, %Y")

    col_welcome, col_animation = st.columns([3, 1])

    with col_welcome:
        st.markdown(
            f"""
        <style>
        .logo-container {{
            display: flex;
            align-items: center;
            text-align:left;
            margin-top: -100px;
            animation: fadeInUp 0.8s ease-out forwards;
        }}
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .logo-container img {{
            width: 50px;
            height: 50px;
            margin-right: 10px;
        }}
        .welcome-text {{
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #1E3A8A, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }}
        iframe.st-emotion-cache-1tvzk6f.e1begtbc0 {{
        /* margin-top: -130px !important; /* Isko abhi comment karte hain */
        transform: translateY(-110px) !important; /* Iski jagah yeh try karein */
        margin-bottom: -150px !important; /* Yeh theek hai agar neeche ka space kam kar raha hai */
        padding-right: 0 !important; /* "none" ki jagah "0" use karein */
        display: block !important; /* Ensures it behaves like a block, helps with margins */
        position: relative; /* Can help ensure transform and margins behave as expected */
        z-index: 1;
        
        }}
        .welcome-subtext {{
            font-weight: 600;
            color: #6c7293;
            font-size: 1.1rem;
        }}
        </style>
        <div class="logo-container">
            <div>
                <h1 class="welcome-text">Hi, welcome back!</h1>
                <p class="welcome-subtext">Your teacher analytics dashboard - {today.strftime('%A, %d %B %Y')}</p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_animation:
        try:
            lottie_animation = load_lottie_file("attached_assets/lottie_animation.json")
            st_lottie(lottie_animation, height=120, key="dashboard_lottie")
        except Exception as e:
            st.write("🏫")

    # Get current user's details

    stat_styles = """
      <style>
    /* Common Card Styles */
    .stat-card {
        text-align: left;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        padding: 1.8rem;
        display: flex;
        justify-content: space-between;
        font-weight: 600;
        # border-radius: 1rem;
        margin-bottom: 25px;
        opacity: 1;
        transform: translateY(0);
        overflow: hidden;
        position: relative;
    }
    
    .stat-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0);
        transition: all 0.3s ease;
        z-index: 1;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.25);
    }
    
    .stat-card:hover:before {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stat-content {
        flex-grow: 1;
        position: relative;
        z-index: 2;
    }
    
    .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover .stat-icon {
        transform: scale(1.1) rotate(10deg);
        background-color: rgba(255, 255, 255, 0.3);
    }
    
    .card-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 30px;
        margin-top: 40px;
    }

    /* Animation Effects with enhanced gradients */
    .total-teachers {
        background: linear-gradient(135deg, #FF8F00, #FFC107);
        animation: pulse 2s infinite alternate;
    }

    .present-today {
        background: linear-gradient(135deg, #E91E63, #F06292);
        animation: pulse 2.3s infinite alternate;
    }

    .absent-today {
        background: linear-gradient(135deg, #2196F3, #64B5F6);
        animation: pulse 2.6s infinite alternate;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2) {
        # background-color: white !important;
        box-sizing: border-box !important;
        /* Resetting potential Streamlit margins/paddings that interfere */
         /* Adjust if there's unwanted external spacing */
        # margin-right: -50px !important;
        margin-left:10px !important;
        boarder-radius:none !important;
    }
    /* Core CSS with modern styling and animations */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Animation keyframes */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideInFromLeft {
            from { transform: translateX(-30px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideInFromRight {
            from { transform: translateX(30px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 8px 16px rgba(0,0,0,0.15); }
            100% { box-shadow: 0 12px 24px rgba(0,0,0,0.25); }
        }
    .feature1-card {
            background: white;
            border-radius: 16px; 
            padding: 25px;
            margin: 15px 0;
            box-shadow: 
                0 10px 15px -3px rgba(0, 0, 0, 0.1),
                0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            transform-style: preserve-3d;
            perspective: 1000px;
            position: relative;
            border: 1px solid rgba(209, 213, 219, 0.3);
        }
        
        .feature1-card:hover {
            transform: translateY(-10px) rotateX(5deg) rotateY(5deg);
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .feature1-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 16px;
            background: linear-gradient(
                135deg, 
                rgba(255, 255, 255, 0.3) 0%, 
                rgba(255, 255, 255, 0) 50%
            );
            z-index: 1;
            pointer-events: none;
        }
        
        .feature1-icon {
            background: linear-gradient(135deg, #667eea, #764ba2);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        
        .feature1-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #1a202c;
            position: relative;
            z-index: 2;
        }
        
        .feature1-description {
            line-height: 1.6;
            position: relative;
            z-index: 2;
            font-weight: 600;
            color: #6c7293;
            font-size: 1.1rem;"
        }
          /* Attendance timing notification */
        .auto-absent-notice {
            background: linear-gradient(135deg, #FEF3C7, #FEF9C3);
            border-left: 5px solid #F59E0B;
            padding: 16px 20px;
            border-radius: 8px;
            margin: 30px 0;
            display: flex;
            align-items: center;
        }
        
        .notice-icon {
            min-width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #FEF3C7;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 16px;
            border: 2px solid #F59E0B;
        }
        
        .notice-content {
            flex: 1;
        }
        
        .notice-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #92400E;
            margin: 0 0 5px 0;
        }
        
        .notice-text {
            font-size: 0.95rem;
            color: #92400E;
            margin: 0;
            opacity: 0.9;
        }
</style>
    """
    st.markdown(stat_styles, unsafe_allow_html=True)
    # input_image = Image.open("lottie_animation.png")
    # output_image = rembg.remove(input_image)
    # output_image.save("transparent_lottie.png")
    # auto_timing = data_manager.get_arrangement_time()
    # if auto_timing and isinstance(auto_timing, tuple) and len(auto_timing) == 2:
    #     auto_hour, auto_minute = auto_timing
    # else:
    #     auto_hour, auto_minute = 10, 30  # Default

    # Today's date
    timing_df = pd.read_csv("configs/timing.csv")
    auto_hour_from_csv = int(timing_df.loc[0, "hour"])  # Column 'hour' se value
    auto_minute_from_csv = int(timing_df.loc[0, "minute"])
    today_date = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(
        f"""
        <div class="auto-absent-notice">
            <div class="notice-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#F59E0B" viewBox="0 0 16 16">
                  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                </svg>
            </div>
            <div class="notice-content">
                <h3 class="notice-title">Auto-Absent Marking Reminder</h3>
                <p class="notice-text">
                    Teachers who have not marked their attendance by <b>{auto_hour_from_csv:02d}:{auto_minute_from_csv:02d}</b> will be automatically marked as absent.
                    Please ensure all staff members record their attendance before this time.
                </p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    # Statistics
    (
        col1,
        col2,
    ) = st.columns({1.6, 3})

    total_teachers = len(data_manager.get_all_teachers())
    present_today = len(data_manager.get_present_teachers(today))
    absent_today = len(data_manager.get_absent_teachers(today))
    # total_arrangement = len(data_manager.get_today_arrangement(today))

    with col1:
        st.markdown(
            f"""
             <div class="stat-card total-teachers"><div class="stat-content">
            <h5  style='color: #f0f2f6;margin-bottom:-25px;'>School</h5>
            <h2 style='color: #f0f2f6;'>{total_teachers +1 }</h2>
            <h5  style='color: #f0f2f6;margin-top:-10px;'>Total Teachers</h5></div>
             <div class="stat-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 16 16">
                    <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"/>
                </svg>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
             <div class='stat-card present-today'><div class="stat-content">
           <h5 style='color: #f0f2f6; margin-bottom:-25px;'>Present</h5>
            <h2 style='color: #f0f2f6;'>{present_today}</h2>
             <h5 style='color: #f0f2f6;margin-top:-10px;'>Teachers in today</h5>
              </div>
               <div class="stat-icon">
               <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 16 16">
                    <path d="M4.968 9.75a.5.5 0 1 0-.866.5A4.498 4.498 0 0 0 8 12.5a4.5 4.5 0 0 0 3.898-2.25.5.5 0 1 0-.866-.5A3.498 3.498 0 0 1 8 11.5a3.498 3.498 0 0 1-3.032-1.75zM7 5.116V5a1 1 0 0 0-1-1H3.28a1 1 0 0 0-.97 1.243l.311 1.242A2 2 0 0 0 4.561 8H5a2 2 0 0 0 2-2V5.116c.115.063.245.1.352.1h.195c.108 0 .237-.037.352-.1V6a3 3 0 0 1-3 3H4.561a3 3 0 0 1-2.9-2.265L1.35 5.493a2 2 0 0 1 1.93-2.486H6a2 2 0 0 1 2 2v.1c-.107-.063-.237-.1-.352-.1h-.195c-.107 0-.237.037-.352.1z"/>
                    <path d="M14 9.752a33.244 33.244 0 0 1-.337 3.162l-.33-.007a32.822 32.822 0 0 1-.316-3.145c-.13.281-.238.555-.324.82-.14-.006-.282-.005-.424.001a4.46 4.46 0 0 0 .54-1.897 4.5 4.5 0 0 0-3.898-2.25.5.5 0 1 0 .866.5A3.498 3.498 0 0 1 12.5 8c0 .743-.227 1.433-.618 2 .038-.875.052-1.747.041-2.603-.02-1.048-.141-1.945-.367-2.723C11.16 3.564 10.505 3 10 3c-.469 0-1.056.496-1.325 1.347-.895-.305-1.718-.514-2.426-.514-.713 0-1.16.291-1.198.313a.5.5 0 1 0 .5.863c.267-.16.58-.296 1.08-.296.535 0 1.248.179 2.04.456l.008-.8c0-.598.476-1.1 1.074-1.1.873 0 1.076.84 1.152 1.335.15.633.256 1.461.274 2.443.022 1.204-.03 2.448-.106 3.604l-.219.05a.5.5 0 1 0 .104.994l1.483-.307a.5.5 0 1 0-.203-.979l-.072.013z"/>
                </svg>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
             <div class='stat-card absent-today'><div class="stat-content">

           <h5 style='color: #f0f2f6;margin-bottom:-25px;'>Absent</h5>
            <h2 style='color: #f0f2f6;'>{absent_today}</h2>
            <h5 style='color: #f0f2f6;margin-top:-10px;'>Teachers out today</h5>
        </div>
        <div class="stat-icon"> <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 16 16">
                    <path d="M8 2a.5.5 0 0 1 .5.5V4a.5.5 0 0 1-1 0V2.5A.5.5 0 0 1 8 2zM3.732 3.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707zM2 8a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 8zm9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5zm.754-4.246a.389.389 0 0 0-.527-.02L7.547 9.31a.91.91 0 1 0 1.302 1.258l3.434-4.297a.389.389 0 0 0-.029-.518z"/>
                    <path fill-rule="evenodd" d="M0 10a8 8 0 1 1 15.547 2.661c-.442 1.253-1.845 1.602-2.932 1.25C11.309 13.488 9.475 13 8 13c-1.474 0-3.31.488-4.615.911-1.087.352-2.49.003-2.932-1.25A7.988 7.988 0 0 1 0 10zm8-7a7 7 0 0 0-6.603 9.329c.203.575.923.876 1.68.63C4.397 12.533 6.358 12 8 12s3.604.532 4.923.96c.757.245 1.477-.056 1.68-.631A7 7 0 0 0 8 3z"/>
                </svg>
            </div>

        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        # st.markdown(
        #     """
        # <style>
        # .custom-container {

        #     boarder-radius:none;
        #     # padding: 20px;
        # }
        # </style>
        # """,
        #     unsafe_allow_html=True,
        # )
        # with st.container():
        #     st.markdown(
        #         """
        #     <div class="custom-container" style=" text-align: center; margin-bottom: 30px; font-size: 30px; font-weight: 700;">
        #         <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px;">
        #             <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
        #         </svg>
        #         Mark Today's Attendance

        #     """,
        #         unsafe_allow_html=True,
        #     )
        #     # Check if attendance already marked
        #     attendance = data_manager.get_attendance(
        #         user_details["teacher_id"], str(today)
        #     )

        #     if attendance:
        #         status = attendance["status"]
        #         time = datetime.strptime(
        #             attendance["timestamp"].split()[1], "%H:%M:%S"
        #         ).strftime("%I:%M %p")
        #         st.success(
        #             f"🟢Your attendance for today is already marked as '{status}' at {time}"
        #         )
        #     else:
        #         # Quick attendance marking
        #         if st.button(
        #             "✅ Mark Present", type="secondary", use_container_width=True
        #         ):
        #             timestamp = f"{today} {datetime.now().strftime('%H:%M:%S')}"
        #             if data_manager.mark_attendance(
        #                 user_details["teacher_id"], "present", timestamp
        #             ):
        #                 st.success("Attendance marked as present!")
        #                 st.rerun()
        #             else:
        #                 st.error("Failed to mark attendance!")
        st.image(
            "image.png",
            width=1000,
        )
        # lottie_animation = load_lottie_file("attached_assets/lottie_animation.json")
        # st_lottie(lottie_animation, height=730, width=650, key="dashboard_lottie_image")
        # st.markdown(
        #     """
        #     <style>
        #     .features-container {
        #         padding: 20px;
        #         margin-bottom: 30px;
        #         transition: all 0.3s ease;
        #     }

        #     .features-title {
        #         color: #2C3E50;
        #         margin-bottom: 25px;
        #         text-align: center;
        #         font-size: 1.8rem;
        #         font-weight: 700;
        #         position: relative;
        #         padding-bottom: 15px;
        #     }

        #     .features-title:after {
        #         content: '';
        #         position: absolute;
        #         width: 100%;
        #         height: 4px;
        #         border-radius: 2px;
        #         background: linear-gradient(90deg, #4568dc, #b06ab3);
        #         left: 50%;
        #         top:70px;

        #         transform: translateX(-50%);
        #     }

        #     .features-grid {
        #         display: grid;
        #         margin-bottom:20px !important;
        #         grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        #         gap: 25px;
        #     }

        #     .feature-card {
        #         padding: 25px;
        #         border-radius: 12px;
        #         transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        #         position: relative;
        #         overflow: hidden;
        #         border: 1px solid rgba(255, 255, 255, 0.3);
        #         box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        #         z-index: 1;
        #     }

        #     .feature-card:before {
        #         content: '';
        #         position: absolute;
        #         width: 100%;
        #         height: 100%;
        #         top: 0;
        #         left: 0;
        #         background: rgba(255, 255, 255, 0.1);
        #         z-index: -1;
        #         opacity: 0;
        #         transition: opacity 0.3s ease;
        #     }

        #     .feature-card:hover {
        #         transform: translateY(-10px);
        #         box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        #     }

        #     .feature-card:hover:before {
        #         opacity: 1;
        #     }

        #     .feature-card h3 {
        #         font-size: 1.3rem;
        #         font-weight: 700;
        #         margin-bottom: 15px;

        #         position: relative;
        #         display: flex;
        #         align-items: center;
        #     }

        #     .feature-icon {
        #         margin-right: 10px;
        #         font-size: 1.4rem;
        #         background: rgba(255, 255, 255, 0.25);
        #         width: 40px;
        #         height: 40px;
        #         display: flex;
        #         align-items: center;
        #         justify-content: center;
        #         border-radius: 50%;
        #         transition: all 0.3s ease;
        #     }

        #     .feature-card:hover .feature-icon {
        #         transform: scale(1.1) rotate(10deg);
        #     }

        #     .feature-card ul {
        #         list-style-type: none;
        #         padding-left: 0;
        #         margin-top: 15px;
        #     }

        #     .feature-card li {
        #         padding: 5px 0;
        #         position: relative;
        #         padding-left: 25px;
        #         transition: transform 0.2s ease;
        #     }

        #     .feature-card li:before {
        #         content: '•';
        #         position: absolute;
        #         left: 0;
        #         color: rgba(255, 255, 255, 0.8);
        #         font-size: 1.5em;
        #         line-height: 1em;
        #         transition: all 0.2s ease;
        #     }

        #     .feature-card li:hover {
        #         transform: translateX(5px);
        #     }

        #     .feature-card li:hover:before {
        #         transform: scale(1.2);
        #     }

        #     .attendance-card {
        #         background: linear-gradient(135deg, #43A047, #66BB6A);
        #         color: white;
        #     }

        #     .analytics-card {
        #         background: linear-gradient(135deg, #1976D2, #42A5F5);
        #         color: white;
        #     }

        #     .arrangements-card {
        #         background: linear-gradient(135deg, #F57C00, #FFB74D);
        #         color: white;
        #     }

        #     .admin-card {
        #        background: linear-gradient(135deg, #F57C00, #FFB74D);
        #         color: white;
        #         }
        #     </style>

        #     <div class="features-container">
        #         <h2 class="features-title">✨ Key Features</h2>
        #         <div class="features-grid">
        #             <div class="feature-card analytics-card">
        #                 <h3>
        #                     <div class="feature-icon">📊</div>
        #                     Analytics & Reports
        #                 </h3>
        #                 <ul>
        #                     <li>Detailed attendance analytics</li>
        #                     <li>Teacher performance insights</li>
        #                     <li>Customizable reporting</li>
        #                 </ul>
        #             </div>
        #             <div class="feature-card admin-card">
        #                 <h3>
        #                     <div class="feature-icon">⚙️</div>
        #                     Administrative Tools
        #                 </h3>
        #                 <ul>
        #                     <li>User management</li>
        #                     <li>Role-based access control</li>
        #                     <li>System configuration</li>
        #                     <li>Real-time tracking</li>
        #                 </ul>
        #             </div>
        #         </div>
        #     </div>
        #      """,
        #     unsafe_allow_html=True,
        # )
        # st.markdown(
        #     """</div>
        #            """,
        #     unsafe_allow_html=True,
        # )

    # Features Overview Section with improved animation and hover effects
    st.markdown(
        "<h2 style='margin-top: 40px; margin-bottom: 20px; font-size: 24px;'>Management Features</h2>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature1-card">
                <div class="feature1-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 16 16">
                        <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"/>
                    </svg>
                </div>
                <h3 class="feature1-title">Teacher Attendance</h3>
                <p class="feature1-description">
                    Mark and track teacher attendance with real-time updates.
                    View historical attendance patterns and identify trends.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature1-card">
                <div class="feature1-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 16 16">
                        <path d="M0 5a5.002 5.002 0 0 0 4.027 4.905 6.46 6.46 0 0 1 .544-2.073C3.695 7.536 3.132 6.864 3 5.91h-.5v-.426h.466V5.05c0-.046 0-.093.004-.135H2.5v-.427h.511C3.236 3.24 4.213 2.5 5.681 2.5c.316 0 .59.031.819.085v.733a3.46 3.46 0 0 0-.815-.082c-.919 0-1.538.466-1.734 1.252h1.917v.427h-1.98c-.003.046-.003.097-.003.147v.422h1.983v.427H3.93c.118.602.468 1.03 1.005 1.229a6.5 6.5 0 0 1 4.97-3.113A5.002 5.002 0 0 0 0 5zm16 5.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0zm-7.75 1.322c.069.835.746 1.485 1.964 1.562V14h.54v-.62c1.259-.086 1.996-.74 1.996-1.69 0-.865-.563-1.31-1.57-1.54l-.426-.1V8.374c.54.06.884.347.966.745h.948c-.07-.804-.779-1.433-1.914-1.502V7h-.54v.629c-1.076.103-1.808.732-1.808 1.622 0 .787.544 1.288 1.45 1.493l.358.085v1.78c-.554-.08-.92-.376-1.003-.787H8.25zm1.96-1.895c-.532-.12-.82-.364-.82-.732 0-.41.311-.719.824-.809v1.54h-.005zm.622 1.044c.645.145.943.38.943.796 0 .474-.37.8-1.02.86v-1.674l.077.018z"/>
                    </svg>
                </div>
                <h3 class="feature1-title">Class Arrangements</h3>
                <p class="feature1-description">
                    Automatically generate intelligent class arrangements for absent teachers.
                    Ensure no class goes uncovered with smart teacher selection.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature1-card">
                <div class="feature1-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 16 16">
                        <path d="M14.5 3a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h13zm-13-1A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-13z"/>
                        <path d="M7 5.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm-1.496-.854a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 1 1 .708-.708l.146.147 1.146-1.147a.5.5 0 0 1 .708 0zM7 9.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm-1.496-.854a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 0 1 .708-.708l.146.147 1.146-1.147a.5.5 0 0 1 .708 0z"/>
                    </svg>
                </div>
                <h3 class="feature1-title">SMS Notifications</h3>
                <p style="margin-top:10px;"class="feature1-description">
                    Automatically notify teachers about their attendance status and arrangements.
                    Real-time communication ensures everyone stays informed.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if "data_manager" not in st.session_state:
        st.session_state.data_manager = DataManager()

    st.markdown(
        """<div class="card-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px;">
                <path d="M15 14s1 0 1-1-1-4-5-4-5 3-5 4 1 1 1 1h8Zm-7.978-1A.261.261 0 0 1 7 12.996c.001-.264.167-1.03.76-1.72C8.312 10.629 9.282 10 11 10c1.717 0 2.687.63 3.24 1.276.593.69.758 1.457.76 1.72l-.008.002a.274.274 0 0 1-.014.002H7.022ZM11 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM6.936 9.28a5.88 5.88 0 0 0-1.23-.247A7.35 7.35 0 0 0 5 9c-4 0-5 3-5 4 0 .667.333 1 1 1h4.216A2.238 2.238 0 0 1 5 13c0-1.01.377-2.042 1.09-2.904.243-.294.526-.569.846-.816ZM4.92 10A5.493 5.493 0 0 0 4 13H1c0-.26.164-1.03.76-1.724.545-.636 1.492-1.256 3.16-1.275ZM1.5 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0Zm3-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z"/>
            </svg>
            Arrangements
        </div>""",
        unsafe_allow_html=True,
    )

    if not data_manager.is_arrangement_suspended(today):
        arrangements = data_manager.get_todays_arrangements()
        if not arrangements.empty:
            st.dataframe(
                arrangements,
                column_config={
                    "absent_teacher": "Absent Teacher",
                    "replacement_teacher": "Replacement Teacher",
                    "class": "Class",
                    "period": "Period",
                    "status": "Status",
                },
                hide_index=True,
            )
        else:
            st.info("No arrangements required")
    else:
        st.warning

    # Weekly attendance summary (for admins)
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.role == "admin":
            st.markdown(
                """<div class="card-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px;">
                    <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                    <path d="M6.854 8.146a.5.5 0 1 0-.708.708L7.293 10H4.5a.5.5 0 0 0 0 1h2.793l-1.147 1.146a.5.5 0 0 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2M8 13a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                </svg>
                Weekly Summary
            </div>""",
                unsafe_allow_html=True,
            )

            # Get data for the past week
            end_date = today
            start_date = end_date - pd.Timedelta(days=6)
            weekly_data = data_manager.get_attendance_report(
                str(start_date), str(end_date)
            )

            if not weekly_data.empty:
                # Group by date and status
                summary = (
                    weekly_data.groupby(["date", "status"])
                    .size()
                    .reset_index(name="count")
                )
                pivot_data = summary.pivot(
                    index="date", columns="status", values="count"
                ).reset_index()

                # Fill NaN with 0
                if "present" not in pivot_data.columns:
                    pivot_data["present"] = 0
                if "absent" not in pivot_data.columns:
                    pivot_data["absent"] = 0

                pivot_data = pivot_data.fillna(0)

                # Create a bar chart
                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=pivot_data["date"],
                        y=pivot_data["present"],
                        name="Present",
                        marker_color="#2e7d32",
                    )
                )

                fig.add_trace(
                    go.Bar(
                        x=pivot_data["date"],
                        y=pivot_data["absent"],
                        name="Absent",
                        marker_color="#d32f2f",
                    )
                )

                fig.update_layout(
                    barmode="stack",
                    title="Weekly Attendance",
                    xaxis_title="Date",
                    yaxis_title="Number of Teachers",
                    legend=dict(
                        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                    ),
                    margin=dict(l=0, r=0, t=40, b=0),
                    height=350,
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the past week.")
    with col2:
        if st.session_state.role == "admin":
            st.markdown(
                """<div class="card-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px; vertical-align: middle;">
  <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
</svg>
                Manual Vs Auto Absent
            </div>""",
                unsafe_allow_html=True,
            )
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        # --- Data Loading and Preparation (Inside Column 2) ---
        try:
            attendance_df = pd.read_csv("attendance.csv")
            logging.info("Successfully loaded attendance.csv for col2 chart")
        except FileNotFoundError:
            st.error("⚠️ `attendance.csv` not found.")
            logging.error("attendance.csv not found in col2.")
            # If file not found, stop processing for this column
            attendance_df = None  # Indicate failure
        except pd.errors.EmptyDataError:
            st.warning("⚠️ `attendance.csv` is empty.")
            logging.warning("attendance.csv is empty in col2.")
            attendance_df = None  # Indicate failure
        except Exception as e:
            st.error(f"⚠️ Error reading attendance.csv: {e}")
            logging.error(f"Error reading attendance.csv in col2: {e}")
            attendance_df = None  # Indicate failure

        # Proceed only if data loaded successfully
        if attendance_df is not None:
            # --- Data Validation ---
            if (
                "is_auto" not in attendance_df.columns
                or "date" not in attendance_df.columns
            ):
                st.error("⚠️ Required columns ('is_auto', 'date') missing.")
                logging.error("Missing required columns in attendance.csv for col2")
                marking_df = pd.DataFrame()  # Ensure marking_df exists but is empty
            else:
                # --- (Rest of your data filtering, grouping, merging code...) ---
                # Ensure 'is_auto' is boolean
                try:
                    attendance_df["is_auto"] = attendance_df["is_auto"].astype(bool)
                except Exception as e:
                    st.warning(f"⚠️ Issue converting 'is_auto' to boolean: {e}")
                    attendance_df["is_auto"] = attendance_df["is_auto"].apply(
                        lambda x: str(x).strip().lower() == "true"
                    )

                auto_marked_df = attendance_df[attendance_df["is_auto"] == True].copy()
                manual_marked_df = attendance_df[
                    attendance_df["is_auto"] == False
                ].copy()

                # --- Aggregation ---
                if not auto_marked_df.empty:
                    auto_marked_counts = (
                        auto_marked_df.groupby("date")
                        .size()
                        .reset_index(name="auto_marked")
                    )
                else:
                    auto_marked_counts = pd.DataFrame(columns=["date", "auto_marked"])

                if not manual_marked_df.empty:
                    manual_marked_counts = (
                        manual_marked_df.groupby("date")
                        .size()
                        .reset_index(name="manual_marked")
                    )
                else:
                    manual_marked_counts = pd.DataFrame(
                        columns=["date", "manual_marked"]
                    )

                # --- Merging ---
                if not auto_marked_counts.empty and not manual_marked_counts.empty:
                    marking_df = pd.merge(
                        auto_marked_counts, manual_marked_counts, on="date", how="outer"
                    )
                elif not auto_marked_counts.empty:
                    marking_df = auto_marked_counts
                    marking_df["manual_marked"] = 0
                elif not manual_marked_counts.empty:
                    marking_df = manual_marked_counts
                    marking_df["auto_marked"] = 0
                else:
                    marking_df = pd.DataFrame()  # Empty

                if not marking_df.empty:
                    marking_df = marking_df.fillna(0)
                    marking_df[["auto_marked", "manual_marked"]] = marking_df[
                        ["auto_marked", "manual_marked"]
                    ].astype(int)

                    try:
                        marking_df["date"] = pd.to_datetime(marking_df["date"])
                        marking_df = marking_df.sort_values(by="date")
                    except Exception as e:
                        st.warning(f"⚠️ Date parsing issue: {e}.")
                        logging.warning(f"Date parsing error in col2: {e}")

                    marking_df = marking_df.tail(7)
                # --- End of Data Processing ---

            # --- Chart Creation and Display (Inside Column 2) ---
            if not marking_df.empty:

                # Create Plotly figure
                fig1 = px.bar(
                    marking_df,
                    x="date",
                    y=["manual_marked", "auto_marked"],
                    labels={"value": "Number of Records", "variable": "Marking Type"},
                    color_discrete_map={
                        "manual_marked": "#0ea5e9",
                        "auto_marked": "#f59e0b",
                    },
                    barmode="stack",
                )

                # Update layout
                fig1.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Number of Records",
                    legend_title="Marking Type",
                    height=350,
                    margin=dict(
                        t=30, l=0, r=0, b=0
                    ),  # Reduce top margin slightly if needed
                    xaxis=dict(tickformat="%b %d, %Y"),
                    legend=dict(
                        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                    ),
                )

                # Display chart *inside* the 'with col2:' block
                st.plotly_chart(fig1, use_container_width=True)
            else:
                # Display message *inside* the column if no data
                st.info("ℹ️ Not enough data for Manual vs Auto-Marked chart.")
                logging.info("marking_df empty in col2, chart not shown.")

    # Custom CSS for the teacher attendance table
    st.markdown(
        """
<style>
    .teacher-card {
        background: linear-gradient(135deg, #ffffff, #e3f2fd);
        border-radius: 16px;
        padding: 18px;
        margin: 15px 0;
        border: 1px solid rgba(209, 217, 230, 0.5);
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .teacher-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 197, 253, 0.1));
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: -1;
    }
    
    .teacher-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .teacher-card:hover:before {
        opacity: 1;
    }
    
    .teacher-checkbox {
        margin-right: 18px;
        transform: scale(1.2);
    }
    
    .teacher-info {
        flex-grow: 1;
        padding-right: 15px;
        transition: all 0.3s ease;
    }
    
    .teacher-card:hover .teacher-info {
        transform: translateX(5px);
    }
    
    .teacher-name {
        font-weight: 700;
        font-size: 18px;
        color: #2c3e50;
        margin-bottom: 4px;
        position: relative;
        display: inline-block;
    }
    
    .teacher-name:after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #93c5fd);
        transition: width 0.3s ease;
    }
    
    .teacher-card:hover .teacher-name:after {
        width: 100%;
    }
    
    .teacher-id {
        color: #64748b;
        font-size: 14px;
        margin-top: 4px;
        display: flex;
        align-items: center;
    }
    
    .teacher-id:before {
        content: '🆔';
        margin-right: 5px;
        font-size: 12px;
        opacity: 0.7;
    }
    
    .teacher-status {
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 100px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .status-present {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
    }
    
    .status-present:hover {
        background: linear-gradient(135deg, #059669, #10b981);
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
    }
    
    .status-absent {
        background: linear-gradient(135deg, #ef4444, #f87171);
        color: white;
    }
    
    .status-absent:hover {
        background: linear-gradient(135deg, #dc2626, #ef4444);
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
    }
    
    .status-unmarked {
        background: linear-gradient(135deg, #9ca3af, #d1d5db);
        color: #1f2937;
    }
    
    .status-unmarked:hover {
        background: linear-gradient(135deg, #6b7280, #9ca3af);
        color: white;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(156, 163, 175, 0.3);
    }
    .section-header {
        background: linear-gradient(90deg, #ff6f61, #de425b);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        margin: 20px 0 15px 0;
        font-weight: 700;
        font-size:20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .select-all-btn {
        background: #66bb6a;
        color: white;
        border: none;
        padding: 7px 14px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        transition: background 0.3s ease-in-out;
    }
    .select-all-btn:hover {
        background: #43a047;

    }
    #  .scroll-container {
    #     max-height: 400px;
    #     overflow-y: auto;
    # }
    /* Calendar Styles */
        .calendar-container {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .calendar-title {
            font-size: 18px;
            font-weight: 600;
            color: #1a202c;
        }
        
        .calendar-nav {
            display: flex;
            gap: 10px;
        }
        
        .calendar-btn {
            background: #f3f4f6;
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        
        .calendar-btn:hover {
            background: #e5e7eb;
        }
        
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
        }
        
        .calendar-weekday {
            text-align: center;
            font-weight: 600;
            color: #6b7280;
            padding: 8px 0;
            font-size: 14px;
        }
        
        .calendar-day {
            text-align: center;
            padding: 10px 0;
            border-radius: 8px;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .calendar-day:hover {
            background: #f3f4f6;
        }
        
        .calendar-day.today {
            background: #e0e7ff;
            color: #4338ca;
            font-weight: 600;
        }
        
        .calendar-day.empty {
            visibility: hidden;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    current_date = get_calendar_dates()
    month_name = current_date.strftime("%B %Y")
    calendar_days = generate_calendar_days(current_date)

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="calendar-container">
                <div class="calendar-header">
                    <div class="calendar-title">{month_name}</div>
                    <div class="calendar-nav">
                        <button class="calendar-btn" onclick="prevMonth()">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
                            </svg>
                        </button>
                        <button class="calendar-btn" onclick="nextMonth()">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="calendar-grid">
                    {calendar_days}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Calendar navigation buttons JavaScript
    st.markdown(
        """
        <script>
            function prevMonth() {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: -1}, '*');
            }
            
            function nextMonth() {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: 1}, '*');
            }
        </script>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
    users_df = pd.read_csv("attached_assets/users.csv")
    today = datetime.now().date()
    attendance_df = st.session_state.data_manager.get_attendance_report(
        str(today), str(today)
    )
    # Merge to find who has already marked attendance
    if not attendance_df.empty:
        marked_teachers = attendance_df["teacher_id"].tolist()
    else:
        marked_teachers = []

    timing_df = pd.read_csv("configs/timing.csv")  # Ensure correct path
    auto_absent_hour = int(timing_df.iloc[0]["hour"])
    auto_absent_minute = int(timing_df.iloc[0]["minute"])
    auto_absent_enabled = bool(timing_df.iloc[0]["enabled"])
    AUTO_ABSENT_TIME = datetime.strptime(
        f"{auto_absent_hour}:{auto_absent_minute}:00", "%H:%M:%S"
    ).time()

    if "attendance_data" not in st.session_state:
        st.session_state.attendance_data = {}

    # Initialize select all checkbox state
    if "mark_all_present" not in st.session_state:
        st.session_state.mark_all_present = False

    # Select all checkbox
    all_present = st.checkbox(
        " Mark all as present",
        value=st.session_state.mark_all_present,
        key="mark_all_present",
    )
    # Create a form for marking attendance
    with st.form("admin_attendance_form"):
        st.markdown(
            """<div class='section-header'> 
            <div class="stat-icoon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 16 16">
                    <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"/>
                </svg></div>
                <b>Teacher Attendance</B></div>""",
            unsafe_allow_html=True,
        )
        attendance_data = {}

        current_time = datetime.now().time()  # Current system time
        errors = []  # To store error messages
        # Display teachers with checkboxes
        for _, teacher in users_df.iterrows():
            teacher_id = teacher["teacher_id"]
            teacher_name = teacher["name"]

            # Check if teacher has already marked attendance
            status = "unmarked"
            if teacher_id in marked_teachers:
                teacher_status = attendance_df[
                    attendance_df["teacher_id"] == teacher_id
                ]["status"].iloc[0]
                status = teacher_status

            # Create checkbox key
            checkbox_key = f"teacher_{teacher_id}"

            # Determine initial checkbox state based on all_present or existing status
            initial_state = all_present or (status == "present")

            # Create teacher card
            st.markdown(
                f"""
            <div class='teacher-card'>
                <div class='teacher-info'>
                    <div class='teacher-name'>{teacher_name}</div>
                    <div class='teacher-id'>ID: {teacher_id}</div>
                </div>
                <div class='teacher-status status-{status}'>
                    {status.capitalize()}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Add checkbox below the card
            is_present = st.checkbox(f"Present", value=initial_state, key=checkbox_key)
            if auto_absent_enabled and current_time > AUTO_ABSENT_TIME:
                if status == "unmarked" and is_present:
                    errors.append(
                        f"❌ You can't mark {teacher_name} present after auto-absent time!"
                    )
                elif status == "present" and not is_present:
                    errors.append(
                        f"❌ You can't unmark {teacher_name} after auto-absent time!"
                    )
            else:
                attendance_data[teacher_id] = is_present
        # Submit button
        submitted = st.form_submit_button("Save Attendance", use_container_width=True)
        if submitted:
            success_count = 0
            already_marked_count = 0

            # Process attendance regardless of which checkboxes were changed
            for teacher_id, is_present in attendance_data.items():
                status = "present" if is_present else "unmarked"

                # Check if attendance already marked
                if teacher_id in marked_teachers:
                    # Get existing status
                    existing_status = attendance_df[
                        attendance_df["teacher_id"] == teacher_id
                    ]["status"].iloc[0]

                    # Only update if status is different
                    if existing_status != status:
                        # Remove old record
                        attendance_df = attendance_df[
                            attendance_df["teacher_id"] != teacher_id
                        ]

                        # Add new record
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        new_attendance = pd.DataFrame(
                            {
                                "date": [str(today)],
                                "teacher_id": [teacher_id],
                                "status": [status],
                                "timestamp": [timestamp],
                            }
                        )

                        updated_attendance_df = pd.concat(
                            [attendance_df, new_attendance], ignore_index=True
                        )
                        updated_attendance_df.to_csv("attendance.csv", index=False)
                        success_count += 1
                    else:
                        already_marked_count += 1
                else:
                    # Mark new attendance
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if data_manager.mark_attendance(teacher_id, status, timestamp):
                        success_count += 1

            # Show success and info messages after processing
            if success_count > 0:
                st.success(
                    f"✅ Attendance marked successfully for {success_count} teachers"
                )
                # Auto rerun to update the attendance display
                st.rerun()

            if already_marked_count > 0:
                st.info(
                    f"ℹ️ {already_marked_count} teachers already had the same status"
                )

        # Display detailed table with enhanced styling
        st.markdown(
            """
        <div style=" 
             padding: 10px 20px; border-radius: 10px; margin: 25px 0 15px 0; 
             color: white; font-weight: 600; font-size: 20px; 
             box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" style="margin-right: 10px;" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                    <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
                </svg>
                Detailed Attendance
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Get teacher names
        merged_df = pd.merge(
            attendance_df, users_df[["teacher_id", "name"]], on="teacher_id", how="left"
        )

        # Filter out unmarked teachers - only show present or absent
        filtered_df = merged_df[merged_df["status"].isin(["present", "absent"])]

        if not filtered_df.empty:
            # Select and rename columns for display
            display_df = filtered_df[
                ["date", "name", "teacher_id", "status", "timestamp"]
            ]
            display_df.columns = [
                "Date",
                "Name",
                "Teacher ID",
                "Status",
                "Timestamp",
            ]

            # Display the dataframe
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No attendance data available to display")
