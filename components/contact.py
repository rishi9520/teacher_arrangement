import streamlit as st
import datetime
import json
import random
from streamlit.components.v1 import html


def render_contact_page():
    """Render ultra-premium contact page with advanced animations and interactive elements"""


# Ultra-premium CSS with advanced animations and effects
st.markdown(
    """
<style>
    /* Base Styles and Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #4F46E5, #7C3AED);
        --secondary-gradient: linear-gradient(135deg, #3B82F6, #2563EB);
        --accent-gradient: linear-gradient(135deg, #F59E0B, #D97706);
        --success-gradient: linear-gradient(135deg, #10B981, #059669);
        --error-gradient: linear-gradient(135deg, #EF4444, #DC2626);
        --primary-color: #4F46E5;
        --text-primary: #1E293B;
        --text-secondary: #475569;
        --text-light: #94A3B8;
        --card-bg: #FFFFFF;
        --card-border: #E2E8F0;
        --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        --card-hover-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    
    .ultra-contact-container {
        font-family: 'Montserrat', sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Advanced Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes zoomIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); }
        50% { transform: scale(1.05); box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3); }
        100% { transform: scale(1); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); }
    }
    
    @keyframes glowing {
        0% { box-shadow: 0 0 5px rgba(79, 70, 229, 0.5); }
        50% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.8); }
        100% { box-shadow: 0 0 5px rgba(79, 70, 229, 0.5); }
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Ultra-premium Hero Section */
    .contact-hero {
        position: relative;
        padding: 120px 0 140px;
        text-align: center;
        overflow: hidden;
        border-radius: 0 0 30px 30px;
        background: var(--primary-gradient);
        margin-bottom: 80px;
    }
    
    .contact-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url('https://cdn.pixabay.com/photo/2018/03/24/08/56/background-3257024_1280.jpg');
        background-size: cover;
        background-position: center;
        mix-blend-mode: overlay;
        opacity: 0.1;
    }
    
    .hero-shapes {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 0;
    }
    
    .hero-shape {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }
    
    .hero-shape-1 {
        width: 150px;
        height: 150px;
        top: 20%;
        left: 10%;
        animation: float 8s ease-in-out infinite;
    }
    
    .hero-shape-2 {
        width: 80px;
        height: 80px;
        bottom: 20%;
        right: 10%;
        animation: float 6s ease-in-out infinite;
        animation-delay: 1s;
    }
    
    .hero-shape-3 {
        width: 120px;
        height: 120px;
        top: 60%;
        left: 20%;
        animation: float 7s ease-in-out infinite;
        animation-delay: 2s;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        letter-spacing: -0.5px;
        animation: zoomIn 1s ease-out forwards;
    }
    
    .hero-title span {
        background: linear-gradient(to right, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        display: inline-block;
    }
    
    .hero-title span::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 5px;
        width: 100%;
        height: 4px;
        background: linear-gradient(to right, #FFD700, #FFA500);
        border-radius: 2px;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 40px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
        animation: fadeIn 1s ease-out forwards;
        animation-delay: 0.3s;
        opacity: 0;
    }
    
    .hero-buttons {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 40px;
        animation: fadeIn 1s ease-out forwards;
        animation-delay: 0.6s;
        opacity: 0;
    }
    
    .hero-button {
        padding: 16px 32px;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        text-decoration: none;
    }
    
    .hero-button-primary {
        background: white;
        color: var(--primary-color);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .hero-button-primary:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    .hero-button-secondary {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .hero-button-secondary:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-5px);
    }
    
    .hero-wave {
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 80px;
    }
    
    /* Contact Cards Grid */
    .contact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 30px;
        margin-bottom: 80px;
    }
    
    /* Ultra Card styles */
    .ultra-card {
        background: var(--card-bg);
        border-radius: 20px;
        box-shadow: var(--card-shadow);
        padding: 40px;
        position: relative;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
        transform: translateY(50px);
        opacity: 0;
        animation: fadeIn 0.7s cubic-bezier(0.215, 0.61, 0.355, 1) forwards;
    }
    
    .ultra-card:hover {
        transform: translateY(-10px) !important;
        box-shadow: var(--card-hover-shadow);
    }
    
    .ultra-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: var(--primary-gradient);
    }
    
    .ultra-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(79, 70, 229, 0));
        border-radius: 100% 0 0 0;
        z-index: 0;
    }
    
    .ultra-card-header {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }
    
    .ultra-card-icon {
        width: 60px;
        height: 60px;
        border-radius: 16px;
        background: var(--primary-gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20px;
        box-shadow: 0 8px 16px rgba(79, 70, 229, 0.2);
        flex-shrink: 0;
        position: relative;
        overflow: hidden;
    }
    
    .ultra-card-icon::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
        animation: spin 10s linear infinite;
    }
    
    .ultra-card-icon img {
        width: 30px;
        height: 30px;
        filter: brightness(0) invert(1);
    }
    
    .ultra-card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    
    .ultra-card-content {
        position: relative;
        z-index: 1;
    }
    
    .ultra-card-description {
        color: var(--text-secondary);
        margin-bottom: 30px;
        line-height: 1.7;
    }
    
    /* Contact Info Grid */
    .contact-info-group {
        margin-bottom: 30px;
    }
    
    .contact-info-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .contact-info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }
    
    .contact-info-grid.full-width {
        grid-template-columns: 1fr;
    }
    
    .contact-info-item {
        display: flex;
        padding: 15px;
        background: #F8FAFC;
        border-radius: 12px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        border: 1px solid #F1F5F9;
    }
    
    .contact-info-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        border-color: #E2E8F0;
    }
    
    .contact-info-item:hover .contact-info-icon {
        transform: scale(1.1);
    }
    
    .contact-info-icon {
        width: 45px;
        height: 45px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        flex-shrink: 0;
        transition: all 0.3s ease;
    }
    
    .contact-info-icon img {
        width: 24px;
        height: 24px;
    }
    
    .contact-info-details {
        flex: 1;
    }
    
    .contact-info-meta {
        font-size: 0.85rem;
        color: var(--text-light);
        margin-bottom: 5px;
    }
    
    .contact-info-value {
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        font-size: 1rem;
    }
    
    .contact-info-item.clickable {
        cursor: pointer;
    }
    
    .contact-info-item.clickable:hover::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: var(--primary-gradient);
    }
    
    /* Business Hours Card */
    .hours-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 15px;
    }
    
    .hours-item {
        background: #F8FAFC;
        padding: 20px;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        border: 1px solid #F1F5F9;
        transition: all 0.3s ease;
    }
    
    .hours-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        border-color: #E2E8F0;
    }
    
    .hours-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: var(--primary-gradient);
        opacity: 0.7;
        border-radius: 2px;
    }
    
    .hours-day {
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 10px;
        font-size: 1.1rem;
    }
    
    .hours-time {
        color: var(--text-secondary);
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .hours-time-icon {
        color: var(--primary-color);
        font-size: 0.9rem;
    }
    
    .hours-status {
        position: absolute;
        top: 15px;
        right: 15px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    
    .hours-status.open {
        background: #10B981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    }
    
    .hours-status.closed {
        background: #EF4444;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
    }
    
    /* Ultra-premium Contact Form */
    .ultra-form-card {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        background: white;
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    .ultra-form-header {
        background: var(--primary-gradient);
        padding: 40px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .ultra-form-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
        animation: spin 20s linear infinite;
    }
    
    .ultra-form-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        position: relative;
    }
    
    .ultra-form-subtitle {
        opacity: 0.9;
        font-size: 1.1rem;
        max-width: 600px;
        line-height: 1.6;
    }
    
    .ultra-form-content {
        padding: 40px;
    }
    
    .ultra-form-group {
        margin-bottom: 25px;
        position: relative;
    }
    
    .ultra-form-label {
        display: block;
        margin-bottom: 10px;
        font-weight: 600;
        color: var(--text-primary);
        position: relative;
        font-size: 0.95rem;
    }
    
    .ultra-form-label::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: -5px;
        width: 20px;
        height: 2px;
        background: var(--primary-gradient);
        border-radius: 1px;
    }
    
    .ultra-form-input {
        width: 100%;
        padding: 16px 20px;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #F8FAFC;
        font-family: 'Montserrat', sans-serif;
    }
    
    .ultra-form-input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        outline: none;
        background: white;
    }
    
    .ultra-form-input::placeholder {
        color: #94A3B8;
    }
    
    .ultra-form-select {
        width: 100%;
        padding: 16px 20px;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        font-size: 1rem;
        appearance: none;
        background-color: #F8FAFC;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' fill='%234F46E5' viewBox='0 0 20 20'%3E%3Cpath d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 15px center;
        background-size: 20px;
        transition: all 0.3s ease;
        font-family: 'Montserrat', sans-serif;
    }
    
    .ultra-form-select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        outline: none;
        background-color: white;
    }
    
    .ultra-form-textarea {
        width: 100%;
        padding: 16px 20px;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        font-size: 1rem;
        min-height: 150px;
        resize: vertical;
        transition: all 0.3s ease;
        background: #F8FAFC;
        font-family: 'Montserrat', sans-serif;
    }
    
    .ultra-form-textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        outline: none;
        background: white;
    }
    
    .ultra-form-button {
        display: inline-block;
        padding: 18px 30px;
        background: var(--primary-gradient);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        text-align: center;
        width: 100%;
        box-shadow: 0 8px 15px rgba(79, 70, 229, 0.3);
        position: relative;
        overflow: hidden;
        font-family: 'Montserrat', sans-serif;
    }
    
    .ultra-form-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(79, 70, 229, 0.4);
    }
    
    .ultra-form-button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 80%);
        transition: all 0.8s ease;
    }
    
    .ultra-form-button:hover::before {
        transform: rotate(180deg);
    }
    
    /* Pulsing animation for button */
    .ultra-form-button.pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Ultra-premium Social Section */
    .ultra-social-section {
        margin: 100px 0;
        padding: 80px 0;
        position: relative;
        overflow: hidden;
    }
    
    .ultra-social-bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #F3F4F6, #E5E7EB);
        z-index: -1;
        border-radius: 30px;
    }
    
    .ultra-social-content {
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .ultra-social-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 20px;
        position: relative;
        display: inline-block;
        z-index: 1;
    }
    
    .ultra-social-title::after {
        content: '';
        position: absolute;
        left: 50%;
        bottom: -10px;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: 2px;
    }
    
    .ultra-social-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin-bottom: 50px;
        line-height: 1.7;
    }
    
    .ultra-social-icons {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 30px;
        margin-bottom: 20px;
    }
    
    .ultra-social-icon {
        width: 140px;
        text-align: center;
        background: white;
        padding: 30px 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        transition: all 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
        text-decoration: none;
        position: relative;
        overflow: hidden;
        transform: translateY(30px);
        opacity: 0;
        animation: fadeIn 0.5s cubic-bezier(0.215, 0.61, 0.355, 1) forwards;
    }
    
    .ultra-social-icon:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .ultra-social-icon::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
    }
    
    .ultra-social-icon:hover::before {
        transform: scaleX(1);
    }
    
    .ultra-social-icon-circle {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        transition: all 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
        position: relative;
    }
    
    .ultra-social-icon:hover .ultra-social-icon-circle {
        transform: rotateY(180deg);
    }
    
    .ultra-social-icon-image {
        width: 35px;
        height: 35px;
        object-fit: contain;
        transition: all 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
    }
    
    .ultra-social-icon:hover .ultra-social-icon-image {
        transform: scale(1.2);
    }
    
    .ultra-social-icon-name {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    
    .ultra-social-icon-username {
        font-size: 0.85rem;
        color: var(--text-light);
    }
    
    /* Ultra-premium Location Section */
    .ultra-location-section {
        margin-bottom: 100px;
    }
    
    .ultra-location-card {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: var(--card-shadow);
        background: white;
        position: relative;
    }
    
    .ultra-map-container {
        position: relative;
        height: 500px;
        z-index: 1;
    }
    
    .ultra-map-container iframe {
        width: 100%;
        height: 100%;
        border: 0;
    }
    
    .ultra-map-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.8) 50%, rgba(255,255,255,0) 100%);
        padding: 100px 40px 40px;
        z-index: 2;
    }
    
    .ultra-location-content {
        display: flex;
        align-items: center;
        gap: 20px;
        max-width: 600px;
        margin: 0 auto;
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        position: relative;
        z-index: 3;
    }
    
    .ultra-location-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        background: var(--primary-gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .ultra-location-icon img {
        width: 30px;
        height: 30px;
        filter: brightness(0) invert(1);
    }
    
    .ultra-location-details {
        flex: 1;
    }
    
    .ultra-location-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 8px 0;
    }
    
    .ultra-location-address {
        color: var(--text-secondary);
        margin: 0;
        line-height: 1.6;
    }
    
    .ultra-location-directions {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: var(--primary-color);
        font-weight: 600;
        margin-top: 15px;
        text-decoration: none;
        position: relative;
        padding-bottom: 2px;
    }
    
    .ultra-location-directions::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    
    .ultra-location-directions:hover::after {
        transform: scaleX(1);
    }
    
    /* Ultra-premium FAQ Section */
    .ultra-faq-section {
        margin-bottom: 100px;
    }
    
    .ultra-faq-header {
        text-align: center;
        margin-bottom: 60px;
    }
    
    .ultra-faq-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 20px;
        position: relative;
        display: inline-block;
    }
    
    .ultra-faq-title::after {
        content: '';
        position: absolute;
        left: 50%;
        bottom: -10px;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: 2px;
    }
    
    .ultra-faq-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.7;
    }
    
    .ultra-faq-container {
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Ultra-premium Footer */
    .ultra-footer {
        background: var(--primary-gradient);
        padding: 80px 40px 40px;
        border-radius: 30px 30px 0 0;
        position: relative;
        overflow: hidden;
        color: white;
        margin-top: 100px;
    }
    
    .ultra-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('https://cdn.pixabay.com/photo/2018/03/24/08/56/background-3257024_1280.jpg');
        background-size: cover;
        background-position: center;
        mix-blend-mode: overlay;
        opacity: 0.1;
    }
    
    .ultra-footer-content {
        position: relative;
        z-index: 1;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 50px;
        margin-bottom: 50px;
    }
    
    .ultra-footer-logo {
        max-width: 100px;
        margin-bottom: 25px;
    }
    
    .ultra-footer-about {
        max-width: 300px;
    }
    
    .ultra-footer-about-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95rem;
        line-height: 1.7;
        margin-bottom: 25px;
    }
    
    .ultra-footer-heading {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 25px;
        position: relative;
        padding-bottom: 10px;
    }
    
    .ultra-footer-heading::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 0;
        width: 50px;
        height: 3px;
        background: white;
        border-radius: 1.5px;
    }
    
    .ultra-footer-links {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .ultra-footer-link {
        margin-bottom: 15px;
    }
    
    .ultra-footer-link a {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .ultra-footer-link a:hover {
        color: white;
        transform: translateX(5px);
    }
    
    .ultra-footer-link-icon {
        font-size: 0.8rem;
    }
    
    .ultra-footer-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.2);
        margin: 30px 0;
    }
    
    .ultra-footer-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        position: relative;
        z-index: 1;
    }
    
    .ultra-footer-copyright {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .ultra-footer-social {
        display: flex;
        gap: 15px;
    }
    
    .ultra-footer-social-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .ultra-footer-social-icon:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .ultra-footer-social-img {
        width: 20px;
        height: 20px;
        filter: brightness(0) invert(1);
    }
    
    /* Animation delays for staggered effect */
    .delay-1 {
        animation-delay: 0.2s !important;
    }
    
    .delay-2 {
        animation-delay: 0.4s !important;
    }
    
    .delay-3 {
        animation-delay: 0.6s !important;
    }
    
    .delay-4 {
        animation-delay: 0.8s !important;
    }
    
    .delay-5 {
        animation-delay: 1s !important;
    }
    
    /* LinkedIn Specific */
    .linkedin-bg {
        background: #E7F0FF;
    }
    
    .linkedin-color {
        color: #0A66C2;
    }
    
    /* Instagram Specific */
    .instagram-bg {
        background: linear-gradient(45deg, #FFDC80, #FCAF45, #F77737, #F56040, #FD1D1D, #E1306C, #C13584, #833AB4, #5851DB, #405DE6);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
    }
    
    .instagram-color {
        color: #E1306C;
    }
    
    /* Telegram Specific */
    .telegram-bg {
        background: #E3F2FD;
    }
    
    .telegram-color {
        color: #0088CC;
    }
    
    /* YouTube Specific */
    .youtube-bg {
        background: #FFEBEE;
    }
    
    .youtube-color {
        color: #FF0000;
    }
    
    /* WhatsApp Specific */
    .whatsapp-bg {
        background: #E8F5E9;
    }
    
    .whatsapp-color {
        color: #25D366;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 1024px) {
        .hero-title {
            font-size: 3rem;
        }
        
        .ultra-form-title {
            font-size: 1.8rem;
        }
        
        .ultra-social-title, .ultra-faq-title {
            font-size: 2.2rem;
        }
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .contact-hero {
            padding: 80px 0 100px;
        }
        
        .contact-info-grid {
            grid-template-columns: 1fr;
        }
        
        .ultra-social-icons {
            gap: 20px;
        }
        
        .ultra-social-icon {
            width: 120px;
            padding: 20px 15px;
        }
        
        .ultra-footer-content {
            grid-template-columns: 1fr;
        }
        
        .ultra-footer-bottom {
            flex-direction: column;
            text-align: center;
        }
        
        .ultra-footer-copyright {
            justify-content: center;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Ultra-premium Hero Section
st.markdown(
    """
<div class="ultra-contact-container">
    <div class="contact-hero">
        <div class="hero-shapes">
            <div class="hero-shape hero-shape-1"></div>
            <div class="hero-shape hero-shape-2"></div>
            <div class="hero-shape hero-shape-3"></div>
        </div>
        <div class="hero-content">
            <h1 class="hero-title">Get in Touch <span>With Us</span></h1>
            <p style="margin-left:110px;"class="hero-subtitle">
                We're here to help! Reach out for support, inquiries, or to explore how our 
                Teacher Attendance System can transform your school's operations.
            </p>
            <div class="hero-buttons">
                <a href="#contact-form" class="hero-button hero-button-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                    </svg>
                    Send Message
                </a>
                <a href="#social-connect" class="hero-button hero-button-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l6.614 1.764a1.5 1.5 0 0 0 .772 0zM1.5 4h13a.5.5 0 0 1 .5.5v1.616L8.129 7.948a.5.5 0 0 1-.258 0L1 6.116V4.5a.5.5 0 0 1 .5-.5z"/>
                    </svg>
                    Connect with Us
                </a>
            </div>
        </div>
        <div class="hero-wave">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 100" fill="#ffffff">
                <path d="M0,96L48,85.3C96,75,192,53,288,42.7C384,32,480,32,576,42.7C672,53,768,75,864,74.7C960,75,1056,53,1152,48C1248,43,1344,53,1392,58.7L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
            </svg>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Contact Info and Form in Grid Layout
st.markdown(
    """
    <div class="contact-grid">
        <!-- Contact Information Card -->
        <div class="ultra-card delay-1">
            <div class="ultra-card-header">
                <div class="ultra-card-icon">
                    <img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png" alt="Contact">
                </div>
                <h2 class="ultra-card-title">Contact Details</h2>
            </div>
            <div class="ultra-card-content">
                <p class="ultra-card-description">
                    Reach out to us through any of our communication channels below. We're dedicated to providing prompt responses and excellent service to all inquiries.
                </p>
                
                <div class="contact-info-group">
    <h3 class="contact-info-label">Personal Information</h3>
    <div class="contact-info-grid">
        <!-- Phone Link (Using <a> tag for better accessibility) -->
        <a href="tel:+919520496351" class="contact-info-item clickable">
            <div class="contact-info-icon" style="background: #EEF2FF;">
                <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" alt="Phone">
            </div>
            <div class="contact-info-details">
                <div class="contact-info-meta">Phone Number</div>
                <div class="contact-info-value">+91 9520496351</div>
            </div>
        </a>

        <!-- WhatsApp Link (Using <a> tag) -->
        <a href="https://wa.me/8954730444" target="_blank" rel="noopener noreferrer" class="contact-info-item clickable">
            <div class="contact-info-icon" style="background: #ECFDF5;">
                <img src="https://cdn-icons-png.flaticon.com/512/220/220236.png" alt="WhatsApp">
            </div>
            <div class="contact-info-details">
                <div class="contact-info-meta">WhatsApp</div>
                <div class="contact-info-value">+91 8954730444</div>
            </div>
        </a>

        <!-- Email Link (Using <a> tag) -->
        <a href="mailto:rishiagrawal45202@gmail.com" class="contact-info-item clickable">
            <div class="contact-info-icon" style="background: #F0F9FF;">
                <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email">
            </div>
            <div class="contact-info-details">
                <div class="contact-info-meta">Email Address</div>
                <div class="contact-info-value">rishiagrawal45202@gmail.com</div>
            </div>
        </a>

        <!-- Full Name (Not clickable) -->
        <div class="contact-info-item">
            <div class="contact-info-icon" style="background: #EFF6FF;">
                <img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png" alt="Person">
            </div>
            <div class="contact-info-details">
                <div class="contact-info-meta">Full Name</div>
                <div class="contact-info-value">Rishi Agrawal</div>
            </div>
        </div>
    </div> <!-- Closing contact-info-grid -->
</div> <!-- Closing contact-info-group -->

<!-- Location Section -->
<div class="contact-info-group">
    <h3 class="contact-info-label">Our Location</h3>
    <div class="contact-info-grid full-width">
        <!-- Address Link (Using <a> tag) -->
        <a href="https://maps.app.goo.gl/JK2xpB5ym2pffSzZ8" target="_blank" rel="noopener noreferrer" class="contact-info-item clickable">
            <div class="contact-info-icon" style="background: #FFF7ED;">
                <img src="https://cdn-icons-png.flaticon.com/512/927/927667.png" alt="Address">
            </div>
            <div class="contact-info-details">
                <div class="contact-info-meta">Office Address</div>
                <div class="contact-info-value">Jawahar Bajar, Sadabad (Hathras), Uttar Pradesh, India - 281306</div>
            </div>
        </a>
    </div> <!-- Closing contact-info-grid -->
</div> <!-- Closing contact-info-group -->

<!-- Business Hours Section -->
<div class="contact-info-group">
    <h3 class="contact-info-label">Business Hours</h3>
    <div class="hours-grid">
        <div class="hours-item">
            <div class="hours-status open"></div>
            <div class="hours-day">Weekdays</div>
            <div class="hours-time">
                <span class="hours-time-icon">⏰</span>
                9:00 AM - 6:00 PM
            </div>
        </div>

        <div class="hours-item">
            <div class="hours-status open"></div>
            <div class="hours-day">Saturday</div>
            <div class="hours-time">
                <span class="hours-time-icon">⏰</span>
                10:00 AM - 4:00 PM
            </div>
        </div>

        <div class="hours-item">
            <div class="hours-status closed"></div>
            <div class="hours-day">Sunday</div>
            <div class="hours-time">
                <span class="hours-time-icon">⏱️</span>
                Closed
            </div>
        </div>
    </div> <!-- Closing hours-grid -->
</div> <!-- Closing contact-info-group -->

<!-- Contact Form Card -->
<div id="contact-form" class="ultra-card delay-2">
    <!-- Form tag added with placeholder action and POST method -->
    <!-- Aapko "action" attribute ko apne server-side script ke URL se update karna hoga -->
    <form class="ultra-form-card" action="/path/to/your/form-handler.php" method="POST">
        <div class="ultra-form-header">
            <h2 class="ultra-form-title">Send Us a Message</h2>
            <p class="ultra-form-subtitle">
                Have questions about our Teacher Attendance System? Fill out the form below, and we'll get back to you promptly with all the information you need.
            </p>
        </div>
        <div class="ultra-form-content">
            <div class="ultra-form-group">
                <label class="ultra-form-label" for="name">Your Name</label>
                <!-- Added name attribute for form submission -->
                <input type="text" id="name" name="name" class="ultra-form-input" placeholder="Enter your full name" required>
            </div>

            <div class="ultra-form-group">
                <label class="ultra-form-label" for="email">Email Address</label>
                <!-- Added name attribute for form submission -->
                <input type="email" id="email" name="email" class="ultra-form-input" placeholder="Enter your email address" required>
            </div>

            <div class="ultra-form-group">
                <label class="ultra-form-label" for="phone">Phone Number</label>
                <!-- Added name attribute for form submission -->
                <input type="tel" id="phone" name="phone" class="ultra-form-input" placeholder="Enter your phone number">
            </div>

            <div class="ultra-form-group">
                <label class="ultra-form-label" for="subject">Subject</label>
                <!-- Added name attribute for form submission -->
                <select id="subject" name="subject" class="ultra-form-select" required>
                    <option value="" disabled selected>Select a subject</option>
                    <option value="general">General Inquiry</option>
                    <option value="support">Technical Support</option>
                    <option value="demo">Request a Demo</option>
                    <option value="sales">Pricing & Plans</option>
                    <option value="feature">Feature Request</option>
                    <option value="partner">Partnership Opportunity</option>
                    <option value="feedback">Feedback</option>
                </select>
            </div>

            <div class="ultra-form-group">
                <label class="ultra-form-label" for="message">Your Message</label>
                <!-- Added name attribute for form submission -->
                <textarea id="message" name="message" class="ultra-form-textarea" placeholder="Type your message here..." required></textarea>
            </div>

            <button type="submit" class="ultra-form-button pulse">
                Send Message
            </button>
        </div> <!-- Closing ultra-form-content -->
    </form> <!-- Closing form tag -->
</div> <!-- Closing ultra-card -->
""",
    unsafe_allow_html=True,
)
# Social Media Section with Ultra-premium Design
st.markdown(
    """
    <div id="social-connect" class="ultra-social-section">
        <div class="ultra-social-bg"></div>
        <div class="ultra-social-content">
            <h2 class="ultra-social-title">Connect With Us</h2>
            <p class="ultra-social-subtitle">
                Follow us on social media to stay updated with our latest announcements, educational insights, and product updates. Join our growing community of educational professionals.
            </p>
            
            <div class="ultra-social-icons">
                <a href="https://www.linkedin.com/in/rishi-agrawal-994a42253" target="_blank" class="ultra-social-icon delay-1">
                    <div class="ultra-social-icon-circle linkedin-bg">
                        <img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" alt="LinkedIn" class="ultra-social-icon-image">
                    </div>
                    <div class="ultra-social-icon-name linkedin-color">LinkedIn</div>
                    <div class="ultra-social-icon-username">@RishiAgrawal</div>
                </a>
                
                <a href="https://www.instagram.com/rishiagrawal45202/" target="_blank" class="ultra-social-icon delay-2">
                    <div class="ultra-social-icon-circle instagram-bg">
                        <img src="https://cdn-icons-png.flaticon.com/512/3955/3955024.png" alt="Instagram" class="ultra-social-icon-image">
                    </div>
                    <div class="ultra-social-icon-name instagram-color">Instagram</div>
                    <div class="ultra-social-icon-username">@rishiagrawal45202</div>
                </a>
                
                <a href="https://t.me/Rishi_agrawal" target="_blank" class="ultra-social-icon delay-3">
                    <div class="ultra-social-icon-circle telegram-bg">
                        <img src="https://cdn-icons-png.flaticon.com/512/5968/5968804.png" alt="Telegram" class="ultra-social-icon-image">
                    </div>
                    <div class="ultra-social-icon-name telegram-color">Telegram</div>
                    <div class="ultra-social-icon-username">@Rishi_agrawal</div>
                </a>
                
                <a href="https://youtube.com/@softcode21?si=jll8Hxsu-dvkN74T" target="_blank" class="ultra-social-icon delay-4">
                    <div class="ultra-social-icon-circle youtube-bg">
                        <img src="https://cdn-icons-png.flaticon.com/512/3670/3670147.png" alt="YouTube" class="ultra-social-icon-image">
                    </div>
                    <div class="ultra-social-icon-name youtube-color">YouTube</div>
                    <div class="ultra-social-icon-username">@softcode21</div>
                </a>
                
                <a href="https://wa.me/8954730444" target="_blank" class="ultra-social-icon delay-5">
                    <div class="ultra-social-icon-circle whatsapp-bg">
                        <img src="https://cdn-icons-png.flaticon.com/512/3670/3670051.png" alt="WhatsApp" class="ultra-social-icon-image">
                    </div>
                    <div class="ultra-social-icon-name whatsapp-color">WhatsApp</div>
                    <div class="ultra-social-icon-username">+91 8954730444</div>
                </a>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Our Location Section with Ultra-premium Design
st.markdown(
    """
    <div class="ultra-location-section">
        <div class="ultra-location-card">
            <div class="ultra-map-container">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14057.058795243926!2d78.3839!3d27.39!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x397474e94fffffa1%3A0xd2855f8ebb006bf5!2sSadabad%2C%20Uttar%20Pradesh!5e0!3m2!1sen!2sin!4v1743499257162!5m2!1sen!2sin"></iframe>
                
                <div class="ultra-map-overlay">
                    <div class="ultra-location-content">
                        <div class="ultra-location-icon">
                            <img src="https://cdn-icons-png.flaticon.com/512/927/927667.png" alt="Address">
                        </div>
                        <div class="ultra-location-details">
                            <h3 class="ultra-location-title">Visit Our Office</h3>
                            <p class="ultra-location-address">
                                Jawahar Bajar, Sadabad (Hathras), Uttar Pradesh, India - 281306
                            </p>
                            <a href="https://maps.app.goo.gl/JK2xpB5ym2pffSzZ8" target="_blank" class="ultra-location-directions">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M9.646 6.764a.5.5 0 0 1 .708 0l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 11H2.5A2.5 2.5 0 0 1 0 8.5v-6a.5.5 0 0 1 1 0v6A1.5 1.5 0 0 0 2.5 10h10.793l-3.647-3.646a.5.5 0 0 1 0-.708z"/>
                                </svg>
                                Get Directions
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# FAQ Section with Ultra-premium Design
st.markdown(
    """
    <div class="ultra-faq-section">
        <div class="ultra-faq-header">
            <h2 class="ultra-faq-title">Frequently Asked Questions</h2>
            <p class="ultra-faq-subtitle">
                Find quick answers to common questions about our services, support options, and the Teacher Attendance System. If you can't find what you're looking for, feel free to contact us.
            </p>
        </div>
        
        <div class="ultra-faq-container">
""",
    unsafe_allow_html=True,
)

# Using Streamlit's built-in expanders for FAQs with custom styling
with st.expander("How can I get technical support for the Teacher Attendance System?"):
    st.markdown(
        """
    <div style="color: #475569; padding: 15px 0; line-height: 1.7;">
        <p>Our dedicated technical support team is available through multiple channels to assist you:</p>
        <ul style="margin-top: 10px; margin-bottom: 15px;">
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Email Support:</strong> Contact us at <a href="mailto:rishiagrawal45202@gmail.com" style="color: #4F46E5; text-decoration: none;">rishiagrawal45202@gmail.com</a> for detailed assistance.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Phone Support:</strong> Call our support line at <a href="tel:+919520496351" style="color: #4F46E5; text-decoration: none;">+91 9520496351</a> for immediate help.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">WhatsApp Support:</strong> Connect with us on WhatsApp at <a href="https://wa.me/8954730444" style="color: #4F46E5; text-decoration: none;">+91 8954730444</a> for quick responses.</li>
        </ul>
        <p>We aim to respond to all support inquiries within 24 hours during business days. For urgent matters, we recommend using our phone support for the fastest resolution.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with st.expander(
    "What customization options are available for the Teacher Attendance System?"
):
    st.markdown(
        """
    <div style="color: #475569; padding: 15px 0; line-height: 1.7;">
        <p>Our Teacher Attendance System offers extensive customization options to meet your institution's specific requirements:</p>
        <ul style="margin-top: 10px; margin-bottom: 15px;">
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Interface Branding:</strong> Customize the user interface with your school's colors, logo, and branding elements.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Workflow Adaptations:</strong> Modify attendance workflows to match your institution's specific processes and policies.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Custom Reports:</strong> Create tailored reports and analytics dashboards that focus on the metrics most important to your administration.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Integration Capabilities:</strong> Connect with your existing school management systems, HR software, or other platforms for seamless data flow.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Role-Based Access:</strong> Define custom permission sets and user roles specific to your organizational structure.</li>
        </ul>
        <p>Our development team works closely with each client to understand their unique needs and implement customizations that enhance productivity and user experience. Contact us for a personalized consultation to discuss your specific requirements.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with st.expander(
    "What training and onboarding resources are provided with the system?"
):
    st.markdown(
        """
    <div style="color: #475569; padding: 15px 0; line-height: 1.7;">
        <p>We provide comprehensive training and onboarding resources to ensure a smooth implementation of the Teacher Attendance System:</p>
        <ul style="margin-top: 10px; margin-bottom: 15px;">
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Admin Training Sessions:</strong> Live virtual or on-site training for administrative staff on system configuration and management.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">End-User Workshops:</strong> Interactive sessions for teachers and staff to learn the daily attendance marking process.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Video Tutorials:</strong> A library of instructional videos covering all system features and common workflows.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Comprehensive Documentation:</strong> Detailed user guides and technical documentation for reference.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Knowledge Base:</strong> Searchable online resource with FAQs, troubleshooting guides, and best practices.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Implementation Support:</strong> Dedicated support during the initial setup and data migration phases.</li>
        </ul>
        <p>Our goal is to make the transition to our system as smooth as possible. We also offer custom training programs tailored to your institution's specific needs and skill levels.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with st.expander("How secure is the data in the Teacher Attendance System?"):
    st.markdown(
        """
    <div style="color: #475569; padding: 15px 0; line-height: 1.7;">
        <p>Data security is our top priority. The Teacher Attendance System implements multiple layers of protection:</p>
        <ul style="margin-top: 10px; margin-bottom: 15px;">
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">End-to-End Encryption:</strong> All data is encrypted during transmission and storage using industry-standard encryption protocols.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Access Controls:</strong> Granular, role-based access controls ensure users can only access information relevant to their role.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Regular Security Audits:</strong> We conduct periodic security assessments and vulnerability testing.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Data Backups:</strong> Automated daily backups with secure off-site storage to prevent data loss.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Compliance:</strong> Our system adheres to relevant data protection regulations and educational privacy standards.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Audit Logging:</strong> Comprehensive logging of all system activities for security monitoring and compliance.</li>
        </ul>
        <p>We continually update our security measures to address emerging threats and ensure your institution's data remains protected. Our commitment to data security gives you peace of mind that your sensitive information is always safeguarded.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with st.expander(
    "What are the hardware and system requirements for the Teacher Attendance System?"
):
    st.markdown(
        """
    <div style="color: #475569; padding: 15px 0; line-height: 1.7;">
        <p>Our Teacher Attendance System is designed to be lightweight and accessible across various devices:</p>
        <ul style="margin-top: 10px; margin-bottom: 15px;">
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Supported Browsers:</strong> Works with all modern browsers including Chrome, Firefox, Safari, and Edge (latest two major versions).</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Device Compatibility:</strong> Accessible on desktops, laptops, tablets, and smartphones with responsive design.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Internet Connection:</strong> Requires stable internet connection (minimum 1 Mbps).</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Server Requirements:</strong> For on-premises deployment (optional), server specifications will be provided based on your institution's size.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Storage Space:</strong> Minimal local storage requirements as data is primarily cloud-based.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Optional Hardware:</strong> Compatible with biometric devices and card readers for enhanced attendance verification (separate integration required).</li>
        </ul>
        <p>The system is cloud-based by default, eliminating the need for specialized on-site hardware or dedicated servers. This ensures easy accessibility, regular updates, and minimal IT overhead for your institution.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with st.expander(
    "Can the system handle substitute teacher management and arrangements?"
):
    st.markdown(
        """
    <div style="color: #475569; padding: 15px 0; line-height: 1.7;">
        <p>Yes, our Teacher Attendance System includes comprehensive substitute teacher management functionality:</p>
        <ul style="margin-top: 10px; margin-bottom: 15px;">
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Automatic Assignments:</strong> The system can automatically identify suitable substitutes based on qualifications, schedule availability, and subject expertise.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Manual Override:</strong> Administrators can manually assign specific substitutes to classes as needed.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Substitute Pool Management:</strong> Maintain a database of available substitute teachers with their qualifications, contact information, and availability.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Notification System:</strong> Automatically notify substitute teachers of assignments via email, SMS, or in-app notifications.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Coverage Tracking:</strong> Monitor which classes have been covered and identify any gaps in coverage that need attention.</li>
            <li style="margin-bottom: 8px;"><strong style="color: #1E3A8A;">Reporting:</strong> Generate detailed reports on substitute utilization, frequent absences, and coverage statistics.</li>
        </ul>
        <p>This comprehensive approach ensures that when teachers are absent, their classes are promptly and appropriately covered, minimizing disruption to student learning and maintaining educational continuity.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# Ultra-premium Footer
current_year = datetime.datetime.now().year

st.markdown(
    f"""
    <div class="ultra-footer">
        <div class="ultra-footer-content">
            <div class="ultra-footer-about">
                <img src="https://cdn-icons-png.flaticon.com/512/2521/2521826.png" alt="Logo" class="ultra-footer-logo">
                <p class="ultra-footer-about-text">
                    The Teacher Attendance System by RK Coders revolutionizes educational administration by streamlining attendance tracking and substitute management, allowing schools to focus on what matters most—quality education.
                </p>
            </div>
            
            <div class="ultra-footer-links-container">
                <h3 class="ultra-footer-heading">Quick Links</h3>
                <ul class="ultra-footer-links">
                    <li class="ultra-footer-link">
                        <a href="#">
                            <span class="ultra-footer-link-icon">→</span> Home
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="#">
                            <span class="ultra-footer-link-icon">→</span> Features
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="#">
                            <span class="ultra-footer-link-icon">→</span> Pricing
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="#">
                            <span class="ultra-footer-link-icon">→</span> About Us
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="#">
                            <span class="ultra-footer-link-icon">→</span> Terms & Conditions
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="#">
                            <span class="ultra-footer-link-icon">→</span> Privacy Policy
                        </a>
                    </li>
                </ul>
            </div>
            
            <div class="ultra-footer-contact-container">
                <h3 class="ultra-footer-heading">Contact Us</h3>
                <ul class="ultra-footer-links">
                    <li class="ultra-footer-link">
                        <a href="tel:+919520496351">
                            <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" width="16" style="margin-right: 10px; filter: brightness(0) invert(1);"> +91 9520496351
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="mailto:rishiagrawal45202@gmail.com">
                            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="16" style="margin-right: 10px; filter: brightness(0) invert(1);"> rishiagrawal45202@gmail.com
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="https://wa.me/8954730444">
                            <img src="https://cdn-icons-png.flaticon.com/512/220/220236.png" width="16" style="margin-right: 10px; filter: brightness(0) invert(1);"> +91 8954730444
                        </a>
                    </li>
                    <li class="ultra-footer-link">
                        <a href="#">
                            <img src="https://cdn-icons-png.flaticon.com/512/927/927667.png" width="16" style="margin-right: 10px; filter: brightness(0) invert(1);"> Jawahar Bajar, Sadabad (Hathras), UP, India - 281306
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="ultra-footer-divider"></div>
        
        <div class="ultra-footer-bottom">
            <div class="ultra-footer-copyright">
                <img src="https://cdn-icons-png.flaticon.com/512/74/74745.png" width="18" style="filter: brightness(0) invert(1);"> 
                <span>© {current_year} RK Coders. All Rights Reserved. Teacher Attendance System by Rishi Agrawal, son of Late Devendra Agrawal.</span>
            </div>
            
            <div class="ultra-footer-social">
                <a href="https://www.linkedin.com/in/rishi-agrawal-994a42253" target="_blank" class="ultra-footer-social-icon">
                    <img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" class="ultra-footer-social-img" alt="LinkedIn">
                </a>
                <a href="https://www.instagram.com/rishiagrawal45202/" target="_blank" class="ultra-footer-social-icon">
                    <img src="https://cdn-icons-png.flaticon.com/512/3955/3955024.png" class="ultra-footer-social-img" alt="Instagram">
                </a>
                <a href="https://t.me/Rishi_agrawal" target="_blank" class="ultra-footer-social-icon">
                    <img src="https://cdn-icons-png.flaticon.com/512/5968/5968804.png" class="ultra-footer-social-img" alt="Telegram">
                </a>
                <a href="https://youtube.com/@softcode21?si=jll8Hxsu-dvkN74T" target="_blank" class="ultra-footer-social-icon">
                    <img src="https://cdn-icons-png.flaticon.com/512/3670/3670147.png" class="ultra-footer-social-img" alt="YouTube">
                </a>
                <a href="https://wa.me/8954730444" target="_blank" class="ultra-footer-social-icon">
                    <img src="https://cdn-icons-png.flaticon.com/512/3670/3670051.png" class="ultra-footer-social-img" alt="WhatsApp">
                </a>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# JavaScript for animations and interactions
js_code = """
<script>
    // Function to check if element is in viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
    
    // Function to handle scroll animations
    function handleScrollAnimation() {
        // Animate cards on scroll
        document.querySelectorAll('.ultra-card').forEach(card => {
            if (isInViewport(card) && card.style.opacity !== '1') {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }
        });
        
        // Animate social icons on scroll
        document.querySelectorAll('.ultra-social-icon').forEach(icon => {
            if (isInViewport(icon) && icon.style.opacity !== '1') {
                icon.style.opacity = '1';
                icon.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Add hover effect to contact info items
    document.addEventListener('DOMContentLoaded', function() {
        // Set initial state for cards with delay
        document.querySelectorAll('.ultra-card').forEach((card, index) => {
            card.style.transitionDelay = (0.1 * index) + 's';
        });
        
        // Set initial state for social icons with delay
        document.querySelectorAll('.ultra-social-icon').forEach((icon, index) => {
            icon.style.transitionDelay = (0.1 * index) + 's';
        });
        
        // Run initial animation check
        handleScrollAnimation();
        
        // Add scroll listener
        window.addEventListener('scroll', handleScrollAnimation);
        
        // Add form input animations
        const formInputs = document.querySelectorAll('.ultra-form-input, .ultra-form-select, .ultra-form-textarea');
        formInputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-5px)';
                this.parentElement.style.transition = 'transform 0.3s ease';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'translateY(0)';
            });
        });
        
        // Form button hover effects
        const formButton = document.querySelector('.ultra-form-button');
        if (formButton) {
            formButton.addEventListener('mouseenter', function() {
                this.classList.add('pulse');
            });
            
            formButton.addEventListener('mouseleave', function() {
                this.classList.remove('pulse');
            });
        }
        
        // Add smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 100,
                        behavior: 'smooth'
                    });
                }
            });
        });
    });
</script>
"""

st.markdown(js_code, unsafe_allow_html=True)
