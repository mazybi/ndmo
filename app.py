import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
from data_models import (
    get_all_controls,
    get_phases,
    get_documents_by_control,
    get_evidence_requirements,
    calculate_compliance_score,
    get_all_specifications,
    get_specifications_by_priority,
    get_control_by_id,
    get_specification_by_id,
    get_statistics,
    DOMAINS
)
from sans_data_loader import (
    load_sans_system,
    get_all_specifications as get_sans_specs,
    get_evidence_by_spec,
    get_calculations,
    get_maturity_questions,
    get_statistics as get_sans_stats
)

# Page configuration
st.set_page_config(
    page_title="NDMO/NDI Data Governance Compliance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with professional design
st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main header */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 1rem;
    }
    
    /* Welcome page styles */
    .welcome-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .welcome-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease;
    }
    
    .welcome-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        animation: fadeInUp 1.2s ease;
    }
    
    .welcome-description {
        font-size: 1.2rem;
        line-height: 1.8;
        max-width: 800px;
        margin: 0 auto;
        animation: fadeIn 1.5s ease;
    }
    
    .logo-container {
        text-align: center;
        margin: 2rem 0;
        animation: logoSlideIn 1.5s ease-out;
    }
    
    .logo-img {
        max-width: 300px;
        height: auto;
        border-radius: 1rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        animation: logoFadeInScale 2s ease-out;
    }
    
    @keyframes logoSlideIn {
        0% {
            opacity: 0;
            transform: translateY(-50px) scale(0.8);
        }
        50% {
            opacity: 0.5;
            transform: translateY(-10px) scale(0.9);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes logoFadeInScale {
        0% {
            opacity: 0;
            transform: scale(0.5);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Loading spinner */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #1f77b4;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Modern Landing Page Styles */
    .landing-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .landing-header {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeInDown 0.8s ease;
    }
    
    .landing-logo {
        max-width: 200px;
        height: auto;
        margin: 0 auto 1.5rem;
        display: block;
        border-radius: 1rem;
        box-shadow: 0 8px 25px rgba(31, 119, 180, 0.2);
        animation: logoFadeInScale 1s ease-out;
    }
    
    .landing-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .landing-subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 3rem;
    }
    
    /* Modern Tool Cards */
    .tool-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }
    
    .tool-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e9ecef;
        border-radius: 1.25rem;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease backwards;
    }
    
    .tool-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(31, 119, 180, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .tool-card:hover::before {
        left: 100%;
    }
    
    .tool-card:nth-child(1) { animation-delay: 0.1s; }
    .tool-card:nth-child(2) { animation-delay: 0.2s; }
    .tool-card:nth-child(3) { animation-delay: 0.3s; }
    .tool-card:nth-child(4) { animation-delay: 0.4s; }
    .tool-card:nth-child(5) { animation-delay: 0.5s; }
    .tool-card:nth-child(6) { animation-delay: 0.6s; }
    
    .tool-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 40px rgba(31, 119, 180, 0.2);
        border-color: #1f77b4;
    }
    
    .tool-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
        transition: transform 0.3s ease;
    }
    
    .tool-card:hover .tool-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    .tool-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .tool-description {
        font-size: 0.95rem;
        color: #6c757d;
        line-height: 1.6;
        margin: 0;
    }
    
    .enter-button-container {
        text-align: center;
        margin-top: 3rem;
        animation: fadeInUp 1s ease;
    }
    
    .enter-button {
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        color: white;
        border: none;
        padding: 1.25rem 3rem;
        border-radius: 1rem;
        font-size: 1.2rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(31, 119, 180, 0.3);
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        text-decoration: none;
    }
    
    .enter-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(31, 119, 180, 0.4);
    }
    
    .enter-button-icon {
        font-size: 1.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Feature cards (kept for backward compatibility) */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Login page - Professional Design */
    .login-container {
        max-width: 480px;
        margin: 3rem auto;
        padding: 3.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 1.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        border: 1px solid rgba(31, 119, 180, 0.1);
        animation: slideInUp 0.6s ease-out;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .login-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease;
    }
    
    .login-subtitle {
        font-size: 1rem;
        color: #6c757d;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease;
    }
    
    .login-logo {
        width: 120px;
        height: 120px;
        margin: 0 auto 2rem;
        border-radius: 50%;
        box-shadow: 0 8px 25px rgba(31, 119, 180, 0.2);
        animation: logoPulse 2s ease-in-out infinite;
    }
    
    @keyframes logoPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 8px 25px rgba(31, 119, 180, 0.2); }
        50% { transform: scale(1.05); box-shadow: 0 12px 35px rgba(31, 119, 180, 0.3); }
    }
    
    .login-form-group {
        margin-bottom: 1.5rem;
    }
    
    .login-input-wrapper {
        position: relative;
        margin-bottom: 1.5rem;
    }
    
    .login-input-icon {
        position: absolute;
        left: 15px;
        top: 50%;
        transform: translateY(-50%);
        color: #6c757d;
        font-size: 1.2rem;
        z-index: 1;
    }
    
    .login-button-primary {
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 0.75rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(31, 119, 180, 0.3);
        margin-top: 1rem;
    }
    
    .login-button-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(31, 119, 180, 0.4);
    }
    
    .login-button-secondary {
        background: white;
        color: #1f77b4;
        border: 2px solid #1f77b4;
        padding: 0.875rem 2rem;
        border-radius: 0.75rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 0.75rem;
    }
    
    .login-button-secondary:hover {
        background: #f8f9fa;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(31, 119, 180, 0.2);
    }
    
    .login-divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 2rem 0;
        color: #6c757d;
    }
    
    .login-divider::before,
    .login-divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #dee2e6;
    }
    
    .login-divider span {
        padding: 0 1rem;
        font-size: 0.875rem;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Global Loading Overlay */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease;
    }
    
    .loading-spinner-large {
        width: 60px;
        height: 60px;
        border: 5px solid #f3f3f3;
        border-top: 5px solid #1f77b4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1.5rem;
    }
    
    .loading-text {
        font-size: 1.1rem;
        color: #1f77b4;
        font-weight: 600;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    
    /* Control card */
    .control-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        transition: all 0.3s ease;
    }
    
    .control-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    
    /* Metric card */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-compliant {
        background: #28a745;
        color: white;
    }
    
    .status-progress {
        background: #ffc107;
        color: #000;
    }
    
    .status-non-compliant {
        background: #dc3545;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'compliance_data' not in st.session_state:
    st.session_state.compliance_data = {}
if 'evidence_data' not in st.session_state:
    st.session_state.evidence_data = {}
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

def show_welcome_page():
    """Show modern, elegant landing page with tools only"""
    import time
    
    # Show loading initially
    with st.spinner("Loading system..."):
        time.sleep(0.3)
    
    # Header with Logo and Title - Professional Layout
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    """, unsafe_allow_html=True)
    
    # Logo and Title in a row
    col_logo, col_title = st.columns([1, 3])
    
    with col_logo:
        # Logo - smaller and centered
        try:
            st.image("logo@3x.png", width=120, use_container_width=False)
        except:
            st.markdown("<div style='font-size: 3rem; color: #1f77b4;'>📊</div>", unsafe_allow_html=True)
    
    with col_title:
        st.markdown("<h1 style='text-align: left; font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; padding-top: 1rem;'>NDMO/NDI Compliance System</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: left; font-size: 0.95rem; color: #6c757d; margin: 0.5rem 0 0 0;'>Professional Data Governance Management Platform</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tools Grid - Using Streamlit columns
    st.markdown("""
    <style>
    .tool-card-st {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e9ecef;
        border-radius: 1.25rem;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s ease;
        height: 100%;
        margin-bottom: 1.5rem;
    }
    .tool-card-st:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(31, 119, 180, 0.2);
        border-color: #1f77b4;
    }
    .tool-icon-st {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }
    .tool-title-st {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .tool-description-st {
        font-size: 0.95rem;
        color: #6c757d;
        line-height: 1.6;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tools in 3 columns - 7 tools (3 rows)
    tools = [
        {
            'icon': '🎯',
            'title': 'Control Management',
            'description': 'Comprehensive management of controls and specifications with priority-based classification'
        },
        {
            'icon': '📊',
            'title': 'Interactive Dashboard',
            'description': 'Real-time statistics and interactive charts for compliance measurement and progress tracking'
        },
        {
            'icon': '📋',
            'title': 'Professional Templates',
            'description': 'Fillable professional forms with unified design, logo, and classification for all compliance documents'
        },
        {
            'icon': '📈',
            'title': 'Compliance Scoring',
            'description': 'Automated calculation of compliance scores with real-time progress tracking and reporting'
        },
        {
            'icon': '🔍',
            'title': 'Evidence Management',
            'description': 'Upload and track required evidence for each specification with automated validation'
        },
        {
            'icon': '📥',
            'title': 'Data Import',
            'description': 'Seamless data import from Excel files with automatic mapping and validation'
        },
        {
            'icon': '🛡️',
            'title': 'Data Quality',
            'description': 'Schema analysis, data processing, and NDMO compliance assessment with professional reporting'
        }
    ]
    
    # Display tools in 3 columns
    col1, col2, col3 = st.columns(3)
    
    # Distribute tools across columns
    for idx, tool in enumerate(tools):
        if idx % 3 == 0:
            with col1:
                st.markdown(f"""
                <div class="tool-card-st">
                    <span class="tool-icon-st">{tool['icon']}</span>
                    <h3 class="tool-title-st">{tool['title']}</h3>
                    <p class="tool-description-st">{tool['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        elif idx % 3 == 1:
            with col2:
                st.markdown(f"""
                <div class="tool-card-st">
                    <span class="tool-icon-st">{tool['icon']}</span>
                    <h3 class="tool-title-st">{tool['title']}</h3>
                    <p class="tool-description-st">{tool['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            with col3:
                st.markdown(f"""
                <div class="tool-card-st">
                    <span class="tool-icon-st">{tool['icon']}</span>
                    <h3 class="tool-title-st">{tool['title']}</h3>
                    <p class="tool-description-st">{tool['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Enter System Button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 Enter System", use_container_width=True, type="primary", key="enter_system_btn"):
            # Show loading
            with st.spinner("Loading Dashboard..."):
                time.sleep(0.5)
            
            st.session_state.authenticated = True
            st.rerun()

def show_login_page():
    """Show professional login page with modern design"""
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo
        logo_html = """
        <div class="login-header">
            <div class="login-logo-container" style="text-align: center; margin-bottom: 2rem;">
        """
        try:
            import base64
            with open("logo@3x.png", "rb") as f:
                logo_data = base64.b64encode(f.read()).decode()
                logo_html += f'<img src="data:image/png;base64,{logo_data}" class="login-logo" alt="NDMO/NDI Logo">'
        except:
            logo_html += '<div class="login-logo" style="background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem; font-weight: bold;">📊</div>'
        
        logo_html += """
            </div>
            <h1 class="login-title">Welcome Back</h1>
            <p class="login-subtitle">Sign in to access the NDMO/NDI Compliance System</p>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
        
        # Login Form
        with st.form("login_form", clear_on_submit=False):
            st.markdown("""
            <div class="login-form-group">
            </div>
            """, unsafe_allow_html=True)
            
            # Username with icon
            username = st.text_input(
                "👤 Username",
                placeholder="Enter your username",
                key="login_username",
                help="Enter your registered username"
            )
            
            # Password with icon
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
                help="Enter your password"
            )
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me", key="remember_me")
            
            # Login button
            login_button = st.form_submit_button(
                "🚀 Sign In",
                use_container_width=True,
                type="primary"
            )
            
            # Divider
            st.markdown("""
            <div class="login-divider">
                <span>OR</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Guest button
            guest_button = st.form_submit_button(
                "👤 Continue as Guest",
                use_container_width=True
            )
            
            # Handle form submission
            if login_button:
                if username and password:
                    # Show loading overlay
                    loading_html = """
                    <div class="loading-overlay">
                        <div class="loading-spinner-large"></div>
                        <div class="loading-text">Authenticating...</div>
                    </div>
                    """
                    st.markdown(loading_html, unsafe_allow_html=True)
                    
                    import time
                    time.sleep(0.5)  # Simulate authentication
                    
                    st.session_state.authenticated = True
                    st.session_state.user_name = username
                    st.session_state.remember_me = remember_me
                    st.success(f"✅ Welcome {username}!")
                    st.rerun()
                else:
                    st.error("⚠️ Please enter both username and password")
            
            if guest_button:
                # Show loading overlay
                loading_html = """
                <div class="loading-overlay">
                    <div class="loading-spinner-large"></div>
                    <div class="loading-text">Loading...</div>
                </div>
                """
                st.markdown(loading_html, unsafe_allow_html=True)
                
                import time
                time.sleep(0.3)
                
                st.session_state.authenticated = True
                st.session_state.user_name = "Guest"
                st.rerun()
        
        # Footer links
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #dee2e6;">
            <p style="color: #6c757d; font-size: 0.875rem;">
                Need help? <a href="#" style="color: #1f77b4; text-decoration: none;">Contact Support</a> | 
                <a href="#" style="color: #1f77b4; text-decoration: none;">Forgot Password?</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Check authentication
    if not st.session_state.authenticated:
        show_welcome_page()
        return
    
    # Main header with user name
    user_name = st.session_state.user_name
    header_html = f"""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <h1 class="main-header">📊 NDMO/NDI Compliance System</h1>
        <p style="font-size: 1.2rem; color: #666;">Welcome {user_name} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Logout button
    col1, col2, col3 = st.columns([5, 1, 1])
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_name = ""
            st.rerun()
    
    st.markdown("---")
    
    # Navigation with tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🏠 Dashboard",
        "🎯 Controls",
        "📊 Specifications",
        "📋 Templates",
        "📈 Measurement",
        "📥 Import",
        "📚 Documents",
        "🛡️ Data Quality",
        "⚙️ Settings"
    ])
    
    with tab1:
        show_dashboard_overview()
    
    with tab2:
        show_controls_specifications()
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            show_specifications_by_priority(key_suffix="_tab2")
        with col2:
            st.subheader("NDI Controls")
            st.info("NDI Controls information will be displayed here")
    
    with tab3:
        show_specifications_by_priority(key_suffix="_tab3")
        st.markdown("---")
        show_calculations_scoring()
        st.markdown("---")
        show_maturity_assessment()
    
    with tab4:
        show_templates_forms()
    
    with tab5:
        show_compliance_measurement()
        st.markdown("---")
        show_compliance_phases()
    
    with tab6:
        show_import_data()
    
    with tab7:
        show_documents_evidence()
    
    with tab8:
        show_data_quality_dashboard()
    
    with tab9:
        st.header("⚙️ Settings")
        st.subheader("System Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**System Version:** 1.0.0")
            st.info("**Last Updated:** 2025-11-23")
        with col2:
            st.info("**Total Controls:** " + str(len(get_all_controls())))
            st.info("**Total Specifications:** " + str(len(get_all_specifications())))
        
        st.markdown("---")
        st.subheader("Data Management")
        
        if st.button("🗑️ Clear Session Data"):
            st.session_state.compliance_data = {}
            st.session_state.evidence_data = {}
            st.success("Session data cleared successfully")
        
        if st.button("💾 Export Compliance Data"):
            import json
            export_data = {
                'compliance_data': st.session_state.compliance_data,
                'evidence_data': st.session_state.evidence_data,
                'export_date': datetime.now().isoformat()
            }
            st.download_button(
                "📥 Download JSON",
                json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=f"compliance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def show_dashboard_overview():
    st.header("📈 Compliance Overview")
    
    # Get all controls
    all_controls = get_all_controls()
    
    # Calculate overall metrics
    total_controls = len(all_controls)
    completed_controls = sum(1 for ctrl_id, data in st.session_state.compliance_data.items() 
                            if data.get('status') == 'Compliant')
    in_progress = sum(1 for ctrl_id, data in st.session_state.compliance_data.items() 
                     if data.get('status') == 'In Progress')
    not_started = total_controls - completed_controls - in_progress
    
    # Calculate overall score
    overall_score = calculate_compliance_score(st.session_state.compliance_data, all_controls)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Compliance Score", f"{overall_score:.1f}%", delta=None)
    
    with col2:
        st.metric("Total Controls", total_controls)
    
    with col3:
        st.metric("Compliant Controls", completed_controls, delta=f"{completed_controls}/{total_controls}")
    
    with col4:
        st.metric("In Progress", in_progress)
    
    st.markdown("---")
    
    # Compliance by category
    st.subheader("Compliance by Category")
    category_data = {}
    for control in all_controls:
        category = control.get('category') or control.get('domain', 'Unknown')
        if category not in category_data:
            category_data[category] = {'total': 0, 'compliant': 0}
        category_data[category]['total'] += 1
        ctrl_id = control.get('id') or control.get('control_id', '')
        if ctrl_id and ctrl_id in st.session_state.compliance_data:
            if st.session_state.compliance_data[ctrl_id].get('status') == 'Compliant':
                category_data[category]['compliant'] += 1
    
    # Create bar chart
    categories = list(category_data.keys())
    compliant_counts = [category_data[cat]['compliant'] for cat in categories]
    total_counts = [category_data[cat]['total'] for cat in categories]
    compliance_rates = [(compliant_counts[i] / total_counts[i] * 100) if total_counts[i] > 0 else 0 
                       for i in range(len(categories))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=compliance_rates,
        name='Compliance Rate (%)',
        marker_color='#1f77b4'
    ))
    fig.update_layout(
        title="Compliance Rate by Category",
        xaxis_title="Category",
        yaxis_title="Compliance Rate (%)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Status distribution pie chart
    st.subheader("Status Distribution")
    status_counts = {
        'Compliant': completed_controls,
        'In Progress': in_progress,
        'Not Started': not_started
    }
    
    fig_pie = px.pie(
        values=list(status_counts.values()),
        names=list(status_counts.keys()),
        title="Controls Status Distribution",
        color_discrete_map={
            'Compliant': '#2ecc71',
            'In Progress': '#f39c12',
            'Not Started': '#e74c3c'
        }
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent activity
    st.subheader("Recent Activity")
    if st.session_state.compliance_data:
        activity_df = pd.DataFrame([
            {
                'Control ID': ctrl_id,
                'Status': data.get('status', 'Not Started'),
                'Last Updated': data.get('last_updated', 'N/A')
            }
            for ctrl_id, data in list(st.session_state.compliance_data.items())[-10:]
        ])
        st.dataframe(activity_df, use_container_width=True)
    else:
        st.info("No compliance data recorded yet. Start by updating control statuses in the Compliance Measurement page.")

def show_controls_specifications():
    st.header("🎯 Controls & Specifications")
    
    all_controls = get_all_controls()
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        categories = list(set(ctrl.get('category', ctrl.get('domain', 'Unknown')) for ctrl in all_controls if ctrl.get('category') or ctrl.get('domain')))
        selected_category = st.selectbox(
            "Filter by Category",
            ["All"] + categories,
            key="filter_category_controls"
        )
    with col2:
        search_term = st.text_input("Search Controls", "")
    
    # Filter controls
    filtered_controls = all_controls
    if selected_category != "All":
        filtered_controls = [c for c in filtered_controls 
                           if c.get('category') == selected_category or c.get('domain') == selected_category]
    if search_term:
        filtered_controls = [c for c in filtered_controls 
                           if search_term.lower() in c.get('title', c.get('control_name', '')).lower() or 
                           search_term.lower() in str(c.get('description', c.get('control_description', ''))).lower()]
    
    st.info(f"Displaying {len(filtered_controls)} control(s)")
    
    # Display controls
    for control in filtered_controls:
        control_id = control.get('id') or control.get('control_id', 'N/A')
        control_title = control.get('title') or control.get('control_name', 'N/A')
        
        with st.expander(f"**{control_id} - {control_title}**", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Category:** {control.get('category', control.get('domain', 'N/A'))}")
                st.markdown(f"**Phase:** {control.get('phase', 'N/A')}")
                st.markdown(f"**Priority:** {control.get('priority', 'N/A')}")
                
                st.markdown("### Description")
                description = control.get('description') or control.get('control_description') or 'N/A'
                st.write(description)
                
                st.markdown("### Specifications")
                specs = get_all_specifications()
                control_specs = [s for s in specs if s.get('control_id') == control_id]
                if control_specs:
                    for spec in control_specs[:5]:  # Show first 5 specs
                        spec_text = spec.get('specification_text') or spec.get('text', 'N/A')
                        st.write(f"• **{spec.get('spec_id', 'N/A')}**: {spec_text[:100]}{'...' if len(spec_text) > 100 else ''}")
                    if len(control_specs) > 5:
                        st.info(f"Showing 5 of {len(control_specs)} specifications. Use Specifications tab to view all.")
                else:
                    st.info("No specifications available for this control")
                
                st.markdown("### Requirements")
                requirements = control.get('requirements', control.get('evidence_requirements', []))
                if requirements:
                    if isinstance(requirements, list):
                        for req in requirements[:5]:  # Show first 5 requirements
                            st.write(f"• {req}")
                        if len(requirements) > 5:
                            st.info(f"Showing 5 of {len(requirements)} requirements")
                    else:
                        st.write(f"• {requirements}")
                else:
                    st.info("No requirements listed")
            
            with col2:
                # Current status
                ctrl_id = control_id
                current_status = st.session_state.compliance_data.get(ctrl_id, {}).get('status', 'Not Started')
                status_options = ["Not Started", "In Progress", "Compliant", "Non-Compliant"]
                current_index = status_options.index(current_status) if current_status in status_options else 0
                new_status = st.selectbox(
                    "Status",
                    status_options,
                    index=current_index,
                    key=f"status_select_{ctrl_id}"
                )
                if new_status != current_status:
                    update_control_status(ctrl_id, new_status)
                
                # Compliance score for this control
                if ctrl_id in st.session_state.compliance_data:
                    score = st.session_state.compliance_data[ctrl_id].get('score', 0)
                    st.metric("Compliance Score", f"{score}%")

def update_control_status(ctrl_id, new_status=None):
    # If new_status is not provided, try to get it from session state
    if new_status is None:
        status_key = f"status_{ctrl_id}"
        if status_key in st.session_state:
            new_status = st.session_state[status_key]
        else:
            # Try to get from selectbox key
            selectbox_key = f"status_select_{ctrl_id}"
            if selectbox_key in st.session_state:
                new_status = st.session_state[selectbox_key]
            else:
                return  # No status to update
    
    if ctrl_id not in st.session_state.compliance_data:
        st.session_state.compliance_data[ctrl_id] = {}
    st.session_state.compliance_data[ctrl_id]['status'] = new_status
    st.session_state.compliance_data[ctrl_id]['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Auto-calculate score based on status
    if new_status == 'Compliant':
        st.session_state.compliance_data[ctrl_id]['score'] = 100
    elif new_status == 'In Progress':
        st.session_state.compliance_data[ctrl_id]['score'] = 50
    elif new_status == 'Non-Compliant':
        st.session_state.compliance_data[ctrl_id]['score'] = 0
    else:
        st.session_state.compliance_data[ctrl_id]['score'] = 0

def show_specifications_by_priority(key_suffix=""):
    st.header("📋 Specifications by Priority")
    
    try:
        # Try to get SANS statistics first
        stats = get_sans_stats()
        if not stats:
            stats = get_statistics()
        
        total_specs = stats.get('total_specifications', 191)
        st.subheader(f"Total: {total_specs} Specifications")
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Specifications", stats.get('total_specifications', 191))
        with col2:
            st.metric("P1 Specifications", stats.get('p1_specifications', 0), delta="Year 1")
        with col3:
            st.metric("P2 Specifications", stats.get('p2_specifications', 0), delta="Year 2")
        with col4:
            st.metric("P3 Specifications", stats.get('p3_specifications', 0), delta="Year 3")
        
        st.markdown("---")
        
        # Priority filter
        selected_priority = st.selectbox(
            "Filter by Priority",
            ["All", "P1", "P2", "P3"],
            key=f"filter_priority_specs{key_suffix}"
        )
        
        # Domain filter
        domain_options = ["All"] + [f"{d['code']} - {d['name']}" for d in DOMAINS] if DOMAINS else ["All"]
        selected_domain = st.selectbox(
            "Filter by Domain",
            domain_options,
            key=f"filter_domain_specs{key_suffix}"
        )
        
        # Get specifications (prefer SANS data)
        try:
            all_specs = get_sans_specs()
            if not all_specs:
                if selected_priority == "All":
                    all_specs = get_all_specifications()
                else:
                    all_specs = get_specifications_by_priority(selected_priority)
            else:
                # Filter by priority if needed
                if selected_priority != "All":
                    all_specs = [s for s in all_specs if s.get('priority') == selected_priority]
        except:
            if selected_priority == "All":
                all_specs = get_all_specifications()
            else:
                all_specs = get_specifications_by_priority(selected_priority)
        
        # Filter by domain
        if selected_domain != "All":
            domain_code = selected_domain.split(" - ")[0]
            all_specs = [s for s in all_specs if s.get('domain_code') == domain_code]
        
        st.info(f"Displaying {len(all_specs)} specification(s)")
        
        # Group by control
        controls_dict = {}
        for spec in all_specs:
            control_id = spec.get('control_id', 'Unknown')
            if control_id not in controls_dict:
                # Try to get control name from controls list
                all_controls = get_all_controls()
                control = next((c for c in all_controls if c.get('id') == control_id), None)
                control_name = control.get('title', f'Control {control_id}') if control else f'Control {control_id}'
                
                controls_dict[control_id] = {
                    'control_name': control_name,
                    'domain': spec.get('domain', 'Unknown'),
                    'specifications': []
                }
            controls_dict[control_id]['specifications'].append(spec)
        
        # Display by control
        for control_id, control_info in sorted(controls_dict.items()):
            with st.expander(f"**{control_id} - {control_info['control_name']}** ({len(control_info['specifications'])} specs)", expanded=False):
                st.markdown(f"**Domain:** {control_info['domain']}")
                
                for spec in sorted(control_info['specifications'], key=lambda x: x.get('spec_id', '')):
                    priority_color = {
                        'P1': '🔴',
                        'P2': '🟡',
                        'P3': '🟢'
                    }
                    priority_emoji = priority_color.get(spec.get('priority', ''), '⚪')
                    
                    st.markdown(f"**{priority_emoji} {spec.get('spec_id', 'N/A')}** [{spec.get('priority', 'Unknown')}]")
                    spec_text = spec.get('specification_text', spec.get('text', 'No description available'))
                    st.write(spec_text)
                    
                    # Show evidence if available
                    try:
                        evidence = get_evidence_by_spec(spec.get('spec_id', ''))
                        if evidence:
                            with st.expander(f"Evidence ({len(evidence)} items)"):
                                for ev in evidence:
                                    st.write(f"**{ev.get('type', 'Document')}:** {ev.get('description', '')}")
                                    if ev.get('acceptance_criteria'):
                                        st.write(f"*Acceptance Criteria:* {ev.get('acceptance_criteria')}")
                    except:
                        pass
                    
                    st.markdown("---")
        
        # Summary table
        st.subheader("Summary by Domain")
        if DOMAINS:
            domain_summary = []
            for domain in DOMAINS:
                domain_specs = [s for s in all_specs if s.get('domain_code') == domain['code']]
                p1_count = len([s for s in domain_specs if s.get('priority') == 'P1'])
                p2_count = len([s for s in domain_specs if s.get('priority') == 'P2'])
                p3_count = len([s for s in domain_specs if s.get('priority') == 'P3'])
                
                domain_summary.append({
                    'Domain': domain['name'],
                    'Code': domain['code'],
                    'Total Specs': len(domain_specs),
                    'P1': p1_count,
                    'P2': p2_count,
                    'P3': p3_count
                })
            
            df = pd.DataFrame(domain_summary)
            st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading specifications: {str(e)}")
        st.info("Note: The complete structure with 191 specifications needs to be populated from the PDF. The current structure is a template.")
        st.info("To view all 191 specifications, please ensure the PDF data has been extracted and imported into the system.")

def show_templates_forms():
    st.header("📋 Templates & Forms")
    st.markdown("Fill out NDMO/NDI templates directly in the tool and save them")
    
    # Main categories
    template_category = st.selectbox(
        "Select Template Category",
        ["📄 Evidence Forms", "📊 Compliance Reports", "✅ Audit Checklists", "🤝 Data Share Templates", "📈 Technical Reports", "📋 Use Case Brief"],
        key="template_category_select"
    )
    
    # ============================================
    # EVIDENCE FORMS SECTION
    # ============================================
    if template_category == "📄 Evidence Forms":
        st.subheader("📄 Evidence Forms")
        st.info("Fill out evidence collection forms directly or download professional templates")
        
        evidence_action = st.radio(
            "Choose Action",
            ["Fill Form Directly", "Download Professional Template"],
            horizontal=True,
            key="evidence_action"
        )
        
        if evidence_action == "Fill Form Directly":
            st.subheader("Fill Evidence Collection Form")
            st.info("Fill out the evidence collection form directly in the tool")
        
        all_controls = get_all_controls()
        
        selected_control = st.selectbox(
            "Select Control",
            [f"{c['id']} - {c['title']}" for c in all_controls],
            key="fill_evidence_control"
        )
        
        if selected_control:
            control_id = selected_control.split(" - ")[0]
            control = next((c for c in all_controls if c['id'] == control_id), None)
            
            if control:
                # Try to load saved form
                from fillable_forms import load_form_data
                saved_data = load_form_data("evidence", control_id, "")
                
                with st.form("evidence_form", clear_on_submit=False):
                    st.markdown(f"### {control_id} - {control['title']}")
                    
                    # Control Information (read-only)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input("Control ID", value=control_id, disabled=True)
                        st.text_input("Control Name", value=control['title'], disabled=True)
                    with col2:
                        spec_id = st.text_input("Specification ID *", value=saved_data['data'].get('spec_id', '') if saved_data and saved_data.get('data') else '')
                        priority_index = 0
                        if saved_data and saved_data.get('data') and saved_data['data'].get('priority') in ["P1", "P2", "P3"]:
                            priority_index = ["P1", "P2", "P3"].index(saved_data['data'].get('priority', 'P1'))
                        priority = st.selectbox("Priority *", ["P1", "P2", "P3"], index=priority_index, key="evidence_priority_select")
                    
                    st.markdown("---")
                    st.markdown("### Evidence Details")
                    
                    evidence_types = ["Policy Document", "Procedure Document", "Configuration", "Screenshot", "Report", "Log File", "Other"]
                    evidence_type_index = 0
                    if saved_data and saved_data.get('data') and saved_data['data'].get('evidence_type') in evidence_types:
                        evidence_type_index = evidence_types.index(saved_data['data'].get('evidence_type', 'Policy Document'))
                    evidence_type = st.selectbox("Evidence Type *", evidence_types, index=evidence_type_index, key="evidence_type_select")
                    
                    evidence_description = st.text_area(
                        "Evidence Description *",
                        value=saved_data['data'].get('evidence_description', '') if saved_data and saved_data.get('data') else '',
                        height=100
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        file_name = st.text_input("File Name", value=saved_data['data'].get('file_name', '') if saved_data and saved_data.get('data') else '')
                        file_location = st.text_input("File Location/Path", value=saved_data['data'].get('file_location', '') if saved_data and saved_data.get('data') else '')
                    with col2:
                        upload_date_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('upload_date'):
                            try:
                                upload_date_val = datetime.strptime(saved_data['data'].get('upload_date'), "%Y-%m-%d").date()
                            except:
                                upload_date_val = datetime.now().date()
                        upload_date = st.date_input("Upload Date", value=upload_date_val)
                        uploaded_by = st.text_input("Uploaded By *", value=saved_data['data'].get('uploaded_by', '') if saved_data and saved_data.get('data') else '')
                    
                    st.markdown("---")
                    st.markdown("### Compliance Status")
                    
                    status_options = ["Compliant", "Partially Compliant", "Non-Compliant"]
                    status_index = 0
                    if saved_data and saved_data.get('data') and saved_data['data'].get('compliance_status') in status_options:
                        status_index = status_options.index(saved_data['data'].get('compliance_status', 'Compliant'))
                    compliance_status = st.radio("Compliance Status *", status_options, index=status_index, key=f"compliance_status_{control_id}_{spec_id}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        compliance_score = st.slider("Compliance Score (%)", 0, 100, value=saved_data['data'].get('compliance_score', 100) if saved_data and saved_data.get('data') else 100)
                        impl_date_val = None
                        if saved_data and saved_data.get('data') and saved_data['data'].get('implementation_date'):
                            try:
                                impl_date_val = datetime.strptime(saved_data['data'].get('implementation_date'), "%Y-%m-%d").date()
                            except:
                                impl_date_val = None
                        implementation_date = st.date_input("Implementation Date", value=impl_date_val)
                    with col2:
                        notes = st.text_area("Notes/Comments", value=saved_data['data'].get('notes', '') if saved_data and saved_data.get('data') else '', height=100)
                    
                    st.markdown("---")
                    st.markdown("### Signatures")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        prepared_by = st.text_input("Prepared By", value=saved_data['data'].get('prepared_by', '') if saved_data and saved_data.get('data') else '')
                        prep_date_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('prepared_date'):
                            try:
                                prep_date_val = datetime.strptime(saved_data['data'].get('prepared_date'), "%Y-%m-%d").date()
                            except:
                                prep_date_val = datetime.now().date()
                        prepared_date = st.date_input("Prepared Date", value=prep_date_val)
                    with col2:
                        reviewed_by = st.text_input("Reviewed By", value=saved_data['data'].get('reviewed_by', '') if saved_data and saved_data.get('data') else '')
                        rev_date_val = None
                        if saved_data and saved_data.get('data') and saved_data['data'].get('reviewed_date'):
                            try:
                                rev_date_val = datetime.strptime(saved_data['data'].get('reviewed_date'), "%Y-%m-%d").date()
                            except:
                                rev_date_val = None
                        reviewed_date = st.date_input("Reviewed Date", value=rev_date_val)
                    
                    approved_by = st.text_input("Approved By", value=saved_data['data'].get('approved_by', '') if saved_data and saved_data.get('data') else '')
                    appr_date_val = None
                    if saved_data and saved_data.get('data') and saved_data['data'].get('approved_date'):
                        try:
                            appr_date_val = datetime.strptime(saved_data['data'].get('approved_date'), "%Y-%m-%d").date()
                        except:
                            appr_date_val = None
                    approved_date = st.date_input("Approved Date", value=appr_date_val)
                    
                    submitted = st.form_submit_button("💾 Save Form", use_container_width=True)
                    
                    if submitted:
                        if not spec_id or not evidence_description or not uploaded_by:
                            st.error("Please fill in all required fields (marked with *)")
                        else:
                            # Show loading with progress
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(20)
                                
                                from fillable_forms import save_form_data, generate_pdf_from_form
                                
                                form_data = {
                                'control_id': control_id,
                                'control_name': control['title'],
                                'spec_id': spec_id,
                                'priority': priority,
                                'date': datetime.now().strftime("%Y-%m-%d"),
                                'evidence_type': evidence_type,
                                'evidence_description': evidence_description,
                                'file_name': file_name,
                                'file_location': file_location,
                                'upload_date': upload_date.strftime("%Y-%m-%d") if upload_date else '',
                                'uploaded_by': uploaded_by,
                                'compliance_status': compliance_status,
                                'compliance_score': compliance_score,
                                'implementation_date': implementation_date.strftime("%Y-%m-%d") if implementation_date else '',
                                'notes': notes,
                                'prepared_by': prepared_by,
                                'prepared_date': prepared_date.strftime("%Y-%m-%d") if prepared_date else '',
                                'reviewed_by': reviewed_by,
                                'reviewed_date': reviewed_date.strftime("%Y-%m-%d") if reviewed_date else '',
                                'approved_by': approved_by,
                                'approved_date': approved_date.strftime("%Y-%m-%d") if approved_date else ''
                            }
                            
                                # Save form data
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(40)
                                json_file = save_form_data("evidence", control_id, spec_id, form_data)
                                
                                # Generate PDF
                                status_text.info("📄 Generating PDF...")
                                progress_bar.progress(70)
                                pdf_file = generate_pdf_from_form("evidence", form_data, control_id, control['title'], spec_id)
                                
                                progress_bar.progress(100)
                                status_text.success("✅ Form saved successfully! Scroll down to download.")
                                
                                st.session_state[f'evidence_json_{control_id}_{spec_id}'] = json_file
                                st.session_state[f'evidence_pdf_{control_id}_{spec_id}'] = pdf_file
                                
                                progress_bar.empty()
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                
                # Download buttons outside form
                if f'evidence_json_{control_id}_{spec_id}' in st.session_state:
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(st.session_state[f'evidence_json_{control_id}_{spec_id}'], 'rb') as f:
                            st.download_button(
                                "📥 Download JSON Data",
                                f.read(),
                                file_name=f"Evidence_{control_id}_{spec_id}_{datetime.now().strftime('%Y%m%d')}.json",
                                mime="application/json",
                                key=f"download_json_evidence_{control_id}_{spec_id}"
                            )
                    with col2:
                        with open(st.session_state[f'evidence_pdf_{control_id}_{spec_id}'], 'rb') as f:
                            st.download_button(
                                "📥 Download PDF",
                                f.read(),
                                file_name=f"Evidence_{control_id}_{spec_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                key=f"download_pdf_evidence_{control_id}_{spec_id}"
                            )
                            
                            # Update compliance data
                            if control_id not in st.session_state.compliance_data:
                                st.session_state.compliance_data[control_id] = {}
                            st.session_state.compliance_data[control_id]['status'] = compliance_status
                            st.session_state.compliance_data[control_id]['score'] = compliance_score
                            st.session_state.compliance_data[control_id]['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:  # Download Professional Template
            st.markdown("### Download Professional Evidence Template")
            st.info("Download a professional evidence template with logo and classification")
            
            all_controls = get_all_controls()
            
            selected_control = st.selectbox(
                "Select Control",
                [f"{c['id']} - {c['title']}" for c in all_controls],
                key="download_evidence_template_control"
            )
            
            if selected_control:
                control_id = selected_control.split(" - ")[0]
                control = next((c for c in all_controls if c['id'] == control_id), None)
                
                if control:
                    from sans_data_loader import get_all_specifications
                    all_specs = get_all_specifications()
                    specifications = [s for s in all_specs if s.get('control_id') == control_id]
                    
                    if specifications:
                        selected_spec = st.selectbox(
                            "Select Specification",
                            [f"{s.get('spec_id', '')} - {s.get('specification_text', '')[:60]}..." for s in specifications],
                            key="evidence_template_spec_select"
                        )
                        
                        if selected_spec:
                            spec_id = selected_spec.split(" - ")[0]
                            spec = next((s for s in specifications if s.get('spec_id') == spec_id), None)
                            
                            if spec:
                                if st.button("📥 Generate & Download Professional Evidence Template", use_container_width=True):
                                    progress_bar = st.progress(0)
                                    status_text = st.empty()
                                    
                                    try:
                                        status_text.info("🔄 Starting PDF generation...")
                                        progress_bar.progress(10)
                                        
                                        from professional_templates import create_professional_evidence_template
                                        from sans_data_loader import get_evidence_by_spec
                                        
                                        status_text.info("📄 Loading evidence requirements...")
                                        progress_bar.progress(30)
                                        
                                        evidence_reqs = get_evidence_by_spec(spec_id)
                                        
                                        status_text.info("📄 Creating template...")
                                        progress_bar.progress(60)
                                        
                                        filename = create_professional_evidence_template(
                                            control_id,
                                            control['title'],
                                            spec_id,
                                            spec.get('specification_text', ''),
                                            spec.get('description', ''),
                                            spec.get('priority', 'P1'),
                                            control.get('domain', control.get('category', 'Unknown')),
                                            evidence_reqs if evidence_reqs else None
                                        )
                                        
                                        progress_bar.progress(90)
                                        status_text.info("💾 Finalizing...")
                                        
                                        template_key = f'evidence_template_{control_id}_{spec_id}'
                                        st.session_state[template_key] = filename
                                        
                                        progress_bar.progress(100)
                                        status_text.success("✅ Professional template generated! Download button appears below.")
                                        progress_bar.empty()
                                        st.rerun()
                                    except Exception as e:
                                        progress_bar.empty()
                                        status_text.error(f"❌ Error: {str(e)}")
                                        import traceback
                                        with st.expander("Error Details"):
                                            st.code(traceback.format_exc())
                                
                                # Show download button if template exists
                                template_key = f'evidence_template_{control_id}_{spec_id}'
                                if template_key in st.session_state:
                                    try:
                                        with open(st.session_state[template_key], 'rb') as f:
                                            st.markdown("---")
                                            st.markdown("### 📥 Download Template")
                                            st.download_button(
                                                "📥 Download Evidence Template (PDF)",
                                                f.read(),
                                                file_name=f"Evidence_{spec_id.replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                                mime="application/pdf",
                                                use_container_width=True,
                                                key=f"download_evidence_template_{control_id}_{spec_id}"
                                            )
                                    except Exception as e:
                                        st.error(f"Error loading template: {str(e)}")
                    else:
                        st.warning("No specifications found for this control")
    
    # ============================================
    # COMPLIANCE REPORTS SECTION
    # ============================================
    elif template_category == "📊 Compliance Reports":
        st.subheader("📊 Compliance Reports")
        st.info("Fill out compliance reports directly or download professional templates")
        
        compliance_action = st.radio(
            "Choose Action",
            ["Fill Form Directly", "Download Professional Template"],
            horizontal=True,
            key="compliance_action"
        )
        
        if compliance_action == "Fill Form Directly":
            st.subheader("Fill Compliance Report")
            st.info("Fill out the compliance report directly in the tool")
            
            all_controls = get_all_controls()
            
            selected_control = st.selectbox(
                "Select Control",
                [f"{c['id']} - {c['title']}" for c in all_controls],
                key="fill_compliance_control"
            )
            
            if selected_control:
                control_id = selected_control.split(" - ")[0]
                control = next((c for c in all_controls if c['id'] == control_id), None)
                
                if control:
                    # Try to load saved form
                    from fillable_forms import load_form_data
                    saved_data = load_form_data("compliance_report", control_id, "")
                
                with st.form("compliance_report_form", clear_on_submit=False):
                    st.markdown(f"### {control_id} - {control['title']}")
                    
                    # Report Information
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input("Control ID", value=control_id, disabled=True)
                        st.text_input("Control Name", value=control['title'], disabled=True)
                        report_date = st.date_input("Report Date *", value=datetime.now().date())
                        entity_name = st.text_input("Entity Name *", value=saved_data['data'].get('entity_name', '') if saved_data and saved_data.get('data') else '')
                    with col2:
                        domain = st.text_input("Domain", value=control.get('domain', control.get('category', 'Unknown')), disabled=True)
                        report_period_from_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('report_period_from'):
                            try:
                                report_period_from_val = datetime.strptime(saved_data['data'].get('report_period_from'), "%Y-%m-%d").date()
                            except:
                                report_period_from_val = datetime.now().date()
                        report_period_from = st.date_input("Report Period From", value=report_period_from_val)
                        
                        report_period_to_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('report_period_to'):
                            try:
                                report_period_to_val = datetime.strptime(saved_data['data'].get('report_period_to'), "%Y-%m-%d").date()
                            except:
                                report_period_to_val = datetime.now().date()
                        report_period_to = st.date_input("Report Period To", value=report_period_to_val)
                        prepared_by = st.text_input("Prepared By *", value=saved_data['data'].get('prepared_by', '') if saved_data and saved_data.get('data') else '')
                    
                    st.markdown("---")
                    st.markdown("### Compliance Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        overall_status = st.selectbox("Overall Status *", ["Compliant", "Partially Compliant", "Non-Compliant"], 
                                                     index=0 if not saved_data or not saved_data.get('data') else 
                                                     ["Compliant", "Partially Compliant", "Non-Compliant"].index(saved_data['data'].get('overall_status', 'Compliant')) if saved_data['data'].get('overall_status') in ["Compliant", "Partially Compliant", "Non-Compliant"] else 0,
                                                     key="compliance_report_status_select")
                        overall_score = st.slider("Overall Score (%)", 0, 100, value=saved_data['data'].get('overall_score', 100) if saved_data and saved_data.get('data') else 100)
                    with col2:
                        compliant_count = st.number_input("Compliant Specs", min_value=0, value=saved_data['data'].get('compliant_count', 0) if saved_data and saved_data.get('data') else 0)
                        partially_compliant = st.number_input("Partially Compliant", min_value=0, value=saved_data['data'].get('partially_compliant', 0) if saved_data and saved_data.get('data') else 0)
                    with col3:
                        non_compliant = st.number_input("Non-Compliant", min_value=0, value=saved_data['data'].get('non_compliant', 0) if saved_data and saved_data.get('data') else 0)
                        not_applicable = st.number_input("Not Applicable", min_value=0, value=saved_data['data'].get('not_applicable', 0) if saved_data and saved_data.get('data') else 0)
                    with col4:
                        total_specs = st.number_input("Total Specifications", min_value=0, value=len(control.get('specifications', [])) if control.get('specifications') else saved_data['data'].get('total_specs', 0) if saved_data and saved_data.get('data') else 0)
                    
                    st.markdown("---")
                    st.markdown("### Findings and Recommendations")
                    
                    key_findings = st.text_area("Key Findings", value=saved_data['data'].get('key_findings', '') if saved_data and saved_data.get('data') else '', height=100)
                    recommendations = st.text_area("Recommendations", value=saved_data['data'].get('recommendations', '') if saved_data and saved_data.get('data') else '', height=100)
                    action_items = st.text_area("Action Items", value=saved_data['data'].get('action_items', '') if saved_data and saved_data.get('data') else '', height=100)
                    
                    st.markdown("---")
                    st.markdown("### Signatures")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        reviewed_by = st.text_input("Reviewed By", value=saved_data['data'].get('reviewed_by', '') if saved_data and saved_data.get('data') else '')
                        reviewed_date = st.date_input("Reviewed Date", value=datetime.strptime(saved_data['data'].get('reviewed_date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d").date() if saved_data and saved_data.get('data') and saved_data['data'].get('reviewed_date') else datetime.now().date())
                    with col2:
                        approved_by = st.text_input("Approved By", value=saved_data['data'].get('approved_by', '') if saved_data and saved_data.get('data') else '')
                        approved_date = st.date_input("Approved Date", value=datetime.strptime(saved_data['data'].get('approved_date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d").date() if saved_data and saved_data.get('data') and saved_data['data'].get('approved_date') else datetime.now().date())
                    
                    submitted = st.form_submit_button("💾 Save Compliance Report", use_container_width=True)
                    
                    if submitted:
                        if not entity_name or not prepared_by:
                            st.error("Please fill in all required fields (marked with *)")
                        else:
                            # Show loading with progress
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.info("💾 Saving compliance report...")
                                progress_bar.progress(20)
                                
                                from fillable_forms import save_form_data, generate_pdf_from_form
                                
                                form_data = {
                                'control_id': control_id,
                                'control_name': control['title'],
                                'domain': domain,
                                'report_date': report_date.strftime("%Y-%m-%d"),
                                'entity_name': entity_name,
                                'report_period_from': report_period_from.strftime("%Y-%m-%d"),
                                'report_period_to': report_period_to.strftime("%Y-%m-%d"),
                                'prepared_by': prepared_by,
                                'overall_status': overall_status,
                                'overall_score': overall_score,
                                'compliant_count': compliant_count,
                                'partially_compliant': partially_compliant,
                                'non_compliant': non_compliant,
                                'not_applicable': not_applicable,
                                'total_specs': total_specs,
                                'key_findings': key_findings,
                                'recommendations': recommendations,
                                'action_items': action_items,
                                'reviewed_by': reviewed_by,
                                'reviewed_date': reviewed_date.strftime("%Y-%m-%d"),
                                'approved_by': approved_by,
                                'approved_date': approved_date.strftime("%Y-%m-%d")
                            }
                                
                                # Save form data
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(40)
                                json_file = save_form_data("compliance_report", control_id, "", form_data)
                                
                                # Generate PDF
                                status_text.info("📄 Generating PDF...")
                                progress_bar.progress(70)
                                pdf_file = generate_pdf_from_form("compliance_report", form_data, control_id, control['title'], "")
                                
                                progress_bar.progress(100)
                                status_text.success("✅ Compliance report saved successfully! Scroll down to download.")
                                
                                st.session_state[f'compliance_report_json_{control_id}'] = json_file
                                st.session_state[f'compliance_report_pdf_{control_id}'] = pdf_file
                                
                                progress_bar.empty()
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                
                # Download buttons outside form
                if f'compliance_report_json_{control_id}' in st.session_state:
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(st.session_state[f'compliance_report_json_{control_id}'], 'rb') as f:
                            st.download_button(
                                "📥 Download JSON Data",
                                f.read(),
                                file_name=f"Compliance_Report_{control_id}_{datetime.now().strftime('%Y%m%d')}.json",
                                mime="application/json",
                                key=f"download_json_compliance_{control_id}"
                            )
                    with col2:
                        with open(st.session_state[f'compliance_report_pdf_{control_id}'], 'rb') as f:
                            st.download_button(
                                "📥 Download PDF",
                                f.read(),
                                file_name=f"Compliance_Report_{control_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                key=f"download_pdf_compliance_{control_id}"
                            )
        else:  # Download Professional Template
            st.markdown("### Download Professional Compliance Report")
            st.info("Download a professional compliance report with logo and classification")
            
            all_controls = get_all_controls()
            
            selected_control = st.selectbox(
                "Select Control",
                [f"{c['id']} - {c['title']}" for c in all_controls],
                key="download_compliance_template_control"
            )
            
            if selected_control:
                control_id = selected_control.split(" - ")[0]
                control = next((c for c in all_controls if c['id'] == control_id), None)
                
                if control:
                    if st.button("📥 Generate & Download Professional Compliance Report", use_container_width=True):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            status_text.info("🔄 Starting PDF generation...")
                            progress_bar.progress(10)
                            
                            from professional_templates import create_professional_compliance_report
                            
                            status_text.info("📄 Loading specifications...")
                            progress_bar.progress(30)
                            
                            from sans_data_loader import get_all_specifications
                            all_specs = get_all_specifications()
                            specifications = [s for s in all_specs if s.get('control_id') == control_id]
                            
                            status_text.info("📄 Creating template...")
                            progress_bar.progress(60)
                            
                            filename = create_professional_compliance_report(
                                control_id,
                                control['title'],
                                control.get('domain', control.get('category', 'Unknown')),
                                specifications
                            )
                            
                            progress_bar.progress(90)
                            status_text.info("💾 Finalizing...")
                            
                            template_key = f'compliance_report_template_{control_id}'
                            st.session_state[template_key] = filename
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Professional report generated! Download button appears below.")
                            progress_bar.empty()
                            st.rerun()
                        except Exception as e:
                            progress_bar.empty()
                            status_text.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
                    
                    # Show download button if template exists
                    template_key = f'compliance_report_template_{control_id}'
                    if template_key in st.session_state:
                        try:
                            with open(st.session_state[template_key], 'rb') as f:
                                st.markdown("---")
                                st.markdown("### 📥 Download Template")
                                st.download_button(
                                    "📥 Download Compliance Report (PDF)",
                                    f.read(),
                                    file_name=f"Compliance_Report_{control_id.replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True,
                                    key=f"download_compliance_template_{control_id}"
                                )
                        except Exception as e:
                            st.error(f"Error loading template: {str(e)}")
    
    # ============================================
    # AUDIT CHECKLISTS SECTION
    # ============================================
    elif template_category == "✅ Audit Checklists":
        st.subheader("✅ Audit Checklists")
        st.info("Fill out audit checklists directly or download professional templates")
        
        audit_action = st.radio(
            "Choose Action",
            ["Fill Form Directly", "Download Professional Template"],
            horizontal=True,
            key="audit_action"
        )
        
        if audit_action == "Fill Form Directly":
            st.subheader("Fill Audit Checklist")
            st.info("Fill out the audit checklist directly in the tool")
            
            all_controls = get_all_controls()
            
            selected_control = st.selectbox(
                "Select Control",
                [f"{c['id']} - {c['title']}" for c in all_controls],
                key="fill_audit_control"
            )
            
            if selected_control:
                control_id = selected_control.split(" - ")[0]
                control = next((c for c in all_controls if c['id'] == control_id), None)
                
                if control:
                    # Try to load saved form
                    from fillable_forms import load_form_data
                    saved_data = load_form_data("audit_checklist", control_id, "")
                
                with st.form("audit_checklist_form", clear_on_submit=False):
                    st.markdown(f"### {control_id} - {control['title']}")
                    
                    # Audit Information
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input("Control ID", value=control_id, disabled=True)
                        st.text_input("Control Name", value=control['title'], disabled=True)
                        audit_date = st.date_input("Audit Date *", value=datetime.strptime(saved_data['data'].get('audit_date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d").date() if saved_data and saved_data.get('data') and saved_data['data'].get('audit_date') else datetime.now().date())
                        auditor_name = st.text_input("Auditor Name *", value=saved_data['data'].get('auditor_name', '') if saved_data and saved_data.get('data') else '')
                    with col2:
                        st.text_input("Domain", value=control.get('domain', control.get('category', 'Unknown')), disabled=True)
                        entity_name = st.text_input("Entity Name *", value=saved_data['data'].get('entity_name', '') if saved_data and saved_data.get('data') else '')
                        audit_type = st.selectbox("Audit Type *", ["Internal", "External", "Regulatory"],
                                                 index=0 if not saved_data or not saved_data.get('data') else 
                                                 ["Internal", "External", "Regulatory"].index(saved_data['data'].get('audit_type', 'Internal')) if saved_data['data'].get('audit_type') in ["Internal", "External", "Regulatory"] else 0,
                                                 key="audit_type_select")
                        audit_scope = st.selectbox("Audit Scope *", ["Full", "Partial"],
                                                  index=0 if not saved_data or not saved_data.get('data') else 
                                                  ["Full", "Partial"].index(saved_data['data'].get('audit_scope', 'Full')) if saved_data['data'].get('audit_scope') in ["Full", "Partial"] else 0,
                                                  key="audit_scope_select")
                    
                    st.markdown("---")
                    st.markdown("### Audit Checklist Items")
                    
                    # Standard checklist items
                    checklist_items = [
                        "Policy documented and approved",
                        "Procedures implemented",
                        "Roles and responsibilities defined",
                        "Training conducted",
                        "Evidence available",
                        "Monitoring in place",
                        "Compliance verified",
                        "Documentation complete",
                        "Review conducted",
                        "Improvements identified"
                    ]
                    
                    checklist_results = {}
                    for i, item in enumerate(checklist_items):
                        result = st.radio(
                            f"{i+1}. {item}",
                            ["Yes", "No", "N/A"],
                            horizontal=True,
                            key=f"checklist_{control_id}_{i}",
                            index=0 if not saved_data or not saved_data.get('data') or f"checklist_{i}" not in saved_data['data'] else 
                            ["Yes", "No", "N/A"].index(saved_data['data'][f"checklist_{i}"]) if saved_data['data'][f"checklist_{i}"] in ["Yes", "No", "N/A"] else 0
                        )
                        checklist_results[f"checklist_{i}"] = result
                        notes_key = f"checklist_notes_{i}"
                        checklist_results[notes_key] = st.text_input(f"Notes for item {i+1}", value=saved_data['data'].get(notes_key, '') if saved_data and saved_data.get('data') else '', key=notes_key)
                    
                    st.markdown("---")
                    st.markdown("### Audit Findings")
                    
                    findings = st.text_area("Findings", value=saved_data['data'].get('findings', '') if saved_data and saved_data.get('data') else '', height=100)
                    recommendations = st.text_area("Recommendations", value=saved_data['data'].get('recommendations', '') if saved_data and saved_data.get('data') else '', height=100)
                    
                    st.markdown("---")
                    st.markdown("### Signatures")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        auditor_title = st.text_input("Auditor Title", value=saved_data['data'].get('auditor_title', '') if saved_data and saved_data.get('data') else '')
                    with col2:
                        reviewed_by = st.text_input("Reviewed By", value=saved_data['data'].get('reviewed_by', '') if saved_data and saved_data.get('data') else '')
                        reviewed_date_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('reviewed_date'):
                            try:
                                reviewed_date_val = datetime.strptime(saved_data['data'].get('reviewed_date'), "%Y-%m-%d").date()
                            except:
                                reviewed_date_val = datetime.now().date()
                        reviewed_date = st.date_input("Reviewed Date", value=reviewed_date_val)
                    
                    approved_by = st.text_input("Approved By", value=saved_data['data'].get('approved_by', '') if saved_data and saved_data.get('data') else '')
                    approved_date_val = datetime.now().date()
                    if saved_data and saved_data.get('data') and saved_data['data'].get('approved_date'):
                        try:
                            approved_date_val = datetime.strptime(saved_data['data'].get('approved_date'), "%Y-%m-%d").date()
                        except:
                            approved_date_val = datetime.now().date()
                    approved_date = st.date_input("Approved Date", value=approved_date_val)
                    
                    submitted = st.form_submit_button("💾 Save Audit Checklist", use_container_width=True)
                    
                    if submitted:
                        if not auditor_name or not entity_name:
                            st.error("Please fill in all required fields (marked with *)")
                        else:
                            # Show loading with progress
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.info("💾 Saving audit checklist...")
                                progress_bar.progress(20)
                                
                                from fillable_forms import save_form_data, generate_pdf_from_form
                                
                                form_data = {
                                'control_id': control_id,
                                'control_name': control['title'],
                                'domain': control.get('domain', control.get('category', 'Unknown')),
                                'audit_date': audit_date.strftime("%Y-%m-%d"),
                                'auditor_name': auditor_name,
                                'auditor_title': auditor_title,
                                'entity_name': entity_name,
                                'audit_type': audit_type,
                                'audit_scope': audit_scope,
                                'findings': findings,
                                'recommendations': recommendations,
                                'reviewed_by': reviewed_by,
                                'reviewed_date': reviewed_date.strftime("%Y-%m-%d"),
                                'approved_by': approved_by,
                                'approved_date': approved_date.strftime("%Y-%m-%d")
                            }
                                form_data.update(checklist_results)
                                
                                # Save form data
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(40)
                                json_file = save_form_data("audit_checklist", control_id, "", form_data)
                                
                                # Generate PDF
                                status_text.info("📄 Generating PDF...")
                                progress_bar.progress(70)
                                pdf_file = generate_pdf_from_form("audit_checklist", form_data, control_id, control['title'])
                                
                                progress_bar.progress(100)
                                status_text.success("✅ Audit checklist saved successfully! Scroll down to download.")
                                
                                st.session_state[f'audit_checklist_json_{control_id}'] = json_file
                                st.session_state[f'audit_checklist_pdf_{control_id}'] = pdf_file
                                
                                progress_bar.empty()
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                
                # Download buttons outside form
                if f'audit_checklist_json_{control_id}' in st.session_state:
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(st.session_state[f'audit_checklist_json_{control_id}'], 'rb') as f:
                            st.download_button(
                                "📥 Download JSON Data",
                                f.read(),
                                file_name=f"Audit_Checklist_{control_id}_{datetime.now().strftime('%Y%m%d')}.json",
                                mime="application/json",
                                key=f"download_json_audit_{control_id}"
                            )
                    with col2:
                        with open(st.session_state[f'audit_checklist_pdf_{control_id}'], 'rb') as f:
                            st.download_button(
                                "📥 Download PDF",
                                f.read(),
                                file_name=f"Audit_Checklist_{control_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                key=f"download_pdf_audit_{control_id}"
                            )
        else:  # Download Professional Template
            st.markdown("### Download Professional Audit Checklist")
            st.info("Download a professional audit checklist with logo and classification")
            
            all_controls = get_all_controls()
            
            selected_control = st.selectbox(
                "Select Control",
                [f"{c['id']} - {c['title']}" for c in all_controls],
                key="download_audit_template_control"
            )
            
            if selected_control:
                control_id = selected_control.split(" - ")[0]
                control = next((c for c in all_controls if c['id'] == control_id), None)
                
                if control:
                    if st.button("📥 Generate & Download Professional Audit Checklist", use_container_width=True):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            status_text.info("🔄 Starting PDF generation...")
                            progress_bar.progress(10)
                            
                            from professional_templates import create_professional_audit_checklist
                            
                            status_text.info("📄 Loading specifications...")
                            progress_bar.progress(30)
                            
                            from sans_data_loader import get_all_specifications
                            all_specs = get_all_specifications()
                            specifications = [s for s in all_specs if s.get('control_id') == control_id]
                            
                            status_text.info("📄 Creating template...")
                            progress_bar.progress(60)
                            
                            filename = create_professional_audit_checklist(
                                control_id,
                                control['title'],
                                control.get('domain', control.get('category', 'Unknown')),
                                specifications
                            )
                            
                            progress_bar.progress(90)
                            status_text.info("💾 Finalizing...")
                            
                            template_key = f'audit_checklist_template_{control_id}'
                            st.session_state[template_key] = filename
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Professional checklist generated! Download button appears below.")
                            progress_bar.empty()
                            st.rerun()
                        except Exception as e:
                            progress_bar.empty()
                            status_text.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
    
    # ============================================
    # DATA SHARE TEMPLATES SECTION
    # ============================================
    elif template_category == "🤝 Data Share Templates":
        st.subheader("🤝 Data Share Templates")
        st.info("Fill out data sharing forms directly or download templates")
        
        action_type = st.radio(
            "Choose Action",
            ["Fill Form Directly", "Download Template"],
            horizontal=True,
            key="data_share_action"
        )
        
        data_share_type = st.radio(
            "Select Template Type",
            ["Data Share Agreement", "Data Sharing Report"],
            horizontal=True,
            key="data_share_type"
        )
        
        if action_type == "Fill Form Directly":
            if data_share_type == "Data Share Agreement":
                st.markdown("### Fill Data Share Agreement")
                
                from fillable_data_share import load_data_share_form, save_data_share_form, generate_pdf_from_data_share_form
                saved_data = load_data_share_form("data_share_agreement")
                
                with st.form("data_share_agreement_form", clear_on_submit=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        agreement_id = st.text_input("Agreement ID *", value=saved_data['data'].get('agreement_id', '') if saved_data and saved_data.get('data') else '')
                        data_provider = st.text_input("Data Provider *", value=saved_data['data'].get('data_provider', '') if saved_data and saved_data.get('data') else '')
                        data_recipient = st.text_input("Data Recipient *", value=saved_data['data'].get('data_recipient', '') if saved_data and saved_data.get('data') else '')
                        purpose = st.text_area("Purpose of Data Share *", value=saved_data['data'].get('purpose', '') if saved_data and saved_data.get('data') else '', height=100)
                    with col2:
                        agreement_date_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('agreement_date'):
                            try:
                                agreement_date_val = datetime.strptime(saved_data['data'].get('agreement_date'), "%Y-%m-%d").date()
                            except:
                                agreement_date_val = datetime.now().date()
                        agreement_date = st.date_input("Date", value=agreement_date_val)
                        data_classification = st.selectbox("Data Classification", ["Public", "Internal", "Restricted", "Confidential"],
                                                          index=0 if not saved_data or not saved_data.get('data') else 
                                                          ["Public", "Internal", "Restricted", "Confidential"].index(saved_data['data'].get('data_classification', 'Internal')) if saved_data['data'].get('data_classification') in ["Public", "Internal", "Restricted", "Confidential"] else 0,
                                                          key="data_classification_select")
                        data_categories = st.text_input("Data Categories", value=saved_data['data'].get('data_categories', '') if saved_data and saved_data.get('data') else '')
                        volume = st.text_input("Volume", value=saved_data['data'].get('volume', '') if saved_data and saved_data.get('data') else '')
                        retention_period = st.text_input("Retention Period", value=saved_data['data'].get('retention_period', '') if saved_data and saved_data.get('data') else '')
                        format_type = st.selectbox("Format", ["CSV", "JSON", "XML", "Other"],
                                                  index=0 if not saved_data or not saved_data.get('data') else 
                                                  ["CSV", "JSON", "XML", "Other"].index(saved_data['data'].get('format_type', 'CSV')) if saved_data['data'].get('format_type') in ["CSV", "JSON", "XML", "Other"] else 0,
                                                  key="format_type_select")
                    
                    st.markdown("---")
                    st.markdown("### Terms and Conditions")
                    security_requirements = st.text_area("Security Requirements", value=saved_data['data'].get('security_requirements', '') if saved_data and saved_data.get('data') else '', height=80)
                    access_controls = st.text_area("Access Controls", value=saved_data['data'].get('access_controls', '') if saved_data and saved_data.get('data') else '', height=80)
                    usage_restrictions = st.text_area("Data Usage Restrictions", value=saved_data['data'].get('usage_restrictions', '') if saved_data and saved_data.get('data') else '', height=80)
                    
                    st.markdown("---")
                    st.markdown("### Compliance")
                    col1, col2 = st.columns(2)
                    with col1:
                        ndmo_compliance = st.selectbox("NDMO Compliance", ["Compliant", "Non-Compliant"],
                                                      index=0 if not saved_data or not saved_data.get('data') else 
                                                      ["Compliant", "Non-Compliant"].index(saved_data['data'].get('ndmo_compliance', 'Compliant')) if saved_data['data'].get('ndmo_compliance') in ["Compliant", "Non-Compliant"] else 0)
                        data_protection = st.selectbox("Data Protection", ["Yes", "No"],
                                                       index=0 if not saved_data or not saved_data.get('data') else 
                                                       ["Yes", "No"].index(saved_data['data'].get('data_protection', 'Yes')) if saved_data['data'].get('data_protection') in ["Yes", "No"] else 0)
                    with col2:
                        ndi_compliance = st.selectbox("NDI Compliance", ["Compliant", "Non-Compliant"],
                                                      index=0 if not saved_data or not saved_data.get('data') else 
                                                      ["Compliant", "Non-Compliant"].index(saved_data['data'].get('ndi_compliance', 'Compliant')) if saved_data['data'].get('ndi_compliance') in ["Compliant", "Non-Compliant"] else 0)
                        pia_status = st.selectbox("Privacy Impact Assessment", ["Completed", "Pending"],
                                                 index=0 if not saved_data or not saved_data.get('data') else 
                                                 ["Completed", "Pending"].index(saved_data['data'].get('pia_status', 'Completed')) if saved_data['data'].get('pia_status') in ["Completed", "Pending"] else 0)
                    
                    submitted = st.form_submit_button("💾 Save & Generate PDF", use_container_width=True)
                    
                    if submitted:
                        if not agreement_id or not data_provider or not data_recipient or not purpose:
                            st.error("Please fill in all required fields (marked with *)")
                        else:
                            # Show loading with progress
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.info("💾 Saving data share agreement...")
                                progress_bar.progress(10)
                                
                                form_data = {
                                'agreement_id': agreement_id,
                                'agreement_date': agreement_date.strftime("%Y-%m-%d"),
                                'data_provider': data_provider,
                                'data_recipient': data_recipient,
                                'purpose': purpose,
                                'data_classification': data_classification,
                                'data_categories': data_categories,
                                'volume': volume,
                                'retention_period': retention_period,
                                'format_type': format_type,
                                'security_requirements': security_requirements,
                                'access_controls': access_controls,
                                'usage_restrictions': usage_restrictions,
                                'ndmo_compliance': ndmo_compliance,
                                'ndi_compliance': ndi_compliance,
                                'data_protection': data_protection,
                                'pia_status': pia_status
                            }
                                
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(30)
                                
                                json_file = save_data_share_form("data_share_agreement", form_data)
                                
                                status_text.info("📄 Generating PDF...")
                                progress_bar.progress(60)
                                
                                pdf_file = generate_pdf_from_data_share_form("data_share_agreement", form_data)
                                
                                progress_bar.progress(90)
                                status_text.info("✅ Finalizing...")
                                
                                st.session_state['data_share_agreement_json'] = json_file
                                st.session_state['data_share_agreement_pdf'] = pdf_file
                                
                                progress_bar.progress(100)
                                status_text.success("✅ Form saved successfully! Scroll down to download.")
                                progress_bar.empty()
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                
                # Download buttons outside form
                if 'data_share_agreement_json' in st.session_state and 'data_share_agreement_pdf' in st.session_state:
                    st.markdown("---")
                    st.markdown("### 📥 Download Files")
                    col1, col2 = st.columns(2)
                    with col1:
                        try:
                            with open(st.session_state['data_share_agreement_json'], 'rb') as f:
                                json_data = f.read()
                                st.download_button(
                                    "📥 Download JSON", 
                                    json_data, 
                                    file_name=f"Data_Share_Agreement_{datetime.now().strftime('%Y%m%d')}.json",
                                    mime="application/json",
                                    key="download_json_agreement",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading JSON: {str(e)}")
                    with col2:
                        try:
                            with open(st.session_state['data_share_agreement_pdf'], 'rb') as f:
                                pdf_data = f.read()
                                st.download_button(
                                    "📥 Download PDF", 
                                    pdf_data,
                                    file_name=f"Data_Share_Agreement_{datetime.now().strftime('%Y%m%d')}.pdf",
                                    mime="application/pdf",
                                    key="download_pdf_agreement",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading PDF: {str(e)}")
            
            elif data_share_type == "Data Sharing Report":
                st.markdown("### Fill Data Sharing Report")
                
                from fillable_data_share import load_data_share_form, save_data_share_form, generate_pdf_from_data_share_form
                saved_data = load_data_share_form("data_sharing_report")
                
                with st.form("data_sharing_report_form", clear_on_submit=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        report_period_from_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('report_period_from'):
                            try:
                                report_period_from_val = datetime.strptime(saved_data['data'].get('report_period_from'), "%Y-%m-%d").date()
                            except:
                                report_period_from_val = datetime.now().date()
                        report_period_from = st.date_input("Report Period From", value=report_period_from_val)
                        
                        entity_name = st.text_input("Entity Name *", value=saved_data['data'].get('entity_name', '') if saved_data and saved_data.get('data') else '')
                        prepared_by = st.text_input("Prepared By *", value=saved_data['data'].get('prepared_by', '') if saved_data and saved_data.get('data') else '')
                    with col2:
                        report_period_to_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('report_period_to'):
                            try:
                                report_period_to_val = datetime.strptime(saved_data['data'].get('report_period_to'), "%Y-%m-%d").date()
                            except:
                                report_period_to_val = datetime.now().date()
                        report_period_to = st.date_input("Report Period To", value=report_period_to_val)
                        
                        department = st.text_input("Department", value=saved_data['data'].get('department', '') if saved_data and saved_data.get('data') else '')
                        
                        review_date_val = datetime.now().date()
                        if saved_data and saved_data.get('data') and saved_data['data'].get('review_date'):
                            try:
                                review_date_val = datetime.strptime(saved_data['data'].get('review_date'), "%Y-%m-%d").date()
                            except:
                                review_date_val = datetime.now().date()
                        review_date = st.date_input("Review Date", value=review_date_val)
                    
                    st.markdown("---")
                    st.markdown("### Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        total_agreements = st.number_input("Total Agreements", min_value=0, value=saved_data['data'].get('total_agreements', 0) if saved_data and saved_data.get('data') else 0)
                        data_providers = st.number_input("Data Providers", min_value=0, value=saved_data['data'].get('data_providers', 0) if saved_data and saved_data.get('data') else 0)
                    with col2:
                        active_agreements = st.number_input("Active Agreements", min_value=0, value=saved_data['data'].get('active_agreements', 0) if saved_data and saved_data.get('data') else 0)
                        data_recipients = st.number_input("Data Recipients", min_value=0, value=saved_data['data'].get('data_recipients', 0) if saved_data and saved_data.get('data') else 0)
                    with col3:
                        data_volume = st.text_input("Data Volume Shared", value=saved_data['data'].get('data_volume', '') if saved_data and saved_data.get('data') else '')
                    with col4:
                        compliance_rate = st.number_input("Compliance Rate (%)", min_value=0, max_value=100, value=saved_data['data'].get('compliance_rate', 0) if saved_data and saved_data.get('data') else 0)
                    
                    st.markdown("---")
                    st.markdown("### Findings and Recommendations")
                    key_findings = st.text_area("Key Findings", value=saved_data['data'].get('key_findings', '') if saved_data and saved_data.get('data') else '', height=100)
                    recommendations = st.text_area("Recommendations", value=saved_data['data'].get('recommendations', '') if saved_data and saved_data.get('data') else '', height=100)
                    
                    submitted = st.form_submit_button("💾 Save & Generate PDF", use_container_width=True)
                    
                    if submitted:
                        if not entity_name or not prepared_by:
                            st.error("Please fill in all required fields (marked with *)")
                        else:
                            form_data = {
                                'report_period_from': report_period_from.strftime("%Y-%m-%d"),
                                'report_period_to': report_period_to.strftime("%Y-%m-%d"),
                                'entity_name': entity_name,
                                'department': department,
                                'prepared_by': prepared_by,
                                'review_date': review_date.strftime("%Y-%m-%d"),
                                'total_agreements': total_agreements,
                                'active_agreements': active_agreements,
                                'data_providers': data_providers,
                                'data_recipients': data_recipients,
                                'data_volume': data_volume,
                                'compliance_rate': compliance_rate,
                                'key_findings': key_findings,
                                'recommendations': recommendations
                            }
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(20)
                                
                                json_file = save_data_share_form("data_sharing_report", form_data)
                                
                                status_text.info("📄 Generating PDF...")
                                progress_bar.progress(50)
                                
                                pdf_file = generate_pdf_from_data_share_form("data_sharing_report", form_data)
                                
                                progress_bar.progress(80)
                                status_text.info("✅ Finalizing...")
                                
                                st.session_state['data_sharing_report_json'] = json_file
                                st.session_state['data_sharing_report_pdf'] = pdf_file
                                
                                progress_bar.progress(100)
                                status_text.success("✅ Form saved successfully! Scroll down to download.")
                                progress_bar.empty()
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                
                # Download buttons outside form
                if 'data_sharing_report_json' in st.session_state and 'data_sharing_report_pdf' in st.session_state:
                    st.markdown("---")
                    st.markdown("### 📥 Download Files")
                    col1, col2 = st.columns(2)
                    with col1:
                        try:
                            with open(st.session_state['data_sharing_report_json'], 'rb') as f:
                                json_data = f.read()
                                st.download_button(
                                    "📥 Download JSON", 
                                    json_data,
                                    file_name=f"Data_Sharing_Report_{datetime.now().strftime('%Y%m%d')}.json",
                                    mime="application/json",
                                    key="download_json_report",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading JSON: {str(e)}")
                    with col2:
                        try:
                            with open(st.session_state['data_sharing_report_pdf'], 'rb') as f:
                                pdf_data = f.read()
                                st.download_button(
                                    "📥 Download PDF", 
                                    pdf_data,
                                    file_name=f"Data_Sharing_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                                    mime="application/pdf",
                                    key="download_pdf_report",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading PDF: {str(e)}")
        
        else:  # Download Template
            if data_share_type == "Data Share Agreement":
                st.markdown("### Download Data Share Agreement Template")
                st.write("Download a blank template to fill manually")
                
                # Check if template already generated in session
                template_key = 'data_share_agreement_template_file'
                
                if template_key not in st.session_state:
                    generate_button = st.button("📥 Generate & Download Data Share Agreement Template", use_container_width=True, key="generate_agreement_btn")
                    if generate_button:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        try:
                            status_text.info("🔄 Starting PDF generation...")
                            progress_bar.progress(10)
                            
                            from data_share_templates import create_data_share_agreement_template
                            
                            status_text.info("📄 Creating template structure...")
                            progress_bar.progress(30)
                            
                            status_text.info("🖼️ Adding logo and formatting...")
                            progress_bar.progress(60)
                            
                            filename = create_data_share_agreement_template()
                            
                            progress_bar.progress(90)
                            status_text.info("💾 Saving file...")
                            
                            st.session_state[template_key] = filename
                            st.session_state['agreement_template_generated'] = True
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Template generated successfully! Download button appears below.")
                            progress_bar.empty()
                            st.rerun()  # Refresh to show download button
                        except Exception as e:
                            progress_bar.empty()
                            status_text.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
                
                # Show download button if template is ready
                if template_key in st.session_state:
                    try:
                        with open(st.session_state[template_key], 'rb') as f:
                            pdf_data = f.read()
                            st.markdown("---")
                            st.markdown("### 📥 Download Template")
                            st.download_button(
                                "📥 Download Data Share Agreement (PDF)",
                                pdf_data,
                                file_name=f"Data_Share_Agreement_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                key="download_template_agreement"
                            )
                            if st.button("🔄 Generate New Template", use_container_width=True, key="regenerate_agreement_btn"):
                                if template_key in st.session_state:
                                    try:
                                        os.remove(st.session_state[template_key])
                                    except:
                                        pass
                                del st.session_state[template_key]
                                if 'agreement_template_generated' in st.session_state:
                                    del st.session_state['agreement_template_generated']
                                st.success("🔄 Template cleared. Click 'Generate & Download' to create a new one.")
                    except Exception as e:
                        st.error(f"Error loading template: {str(e)}")
                        if template_key in st.session_state:
                            del st.session_state[template_key]
            
            elif data_share_type == "Data Sharing Report":
                st.markdown("### Download Data Sharing Report Template")
                st.write("Download a blank template to fill manually")
                
                # Check if template already generated in session
                template_key = 'data_sharing_report_template_file'
                
                if template_key not in st.session_state:
                    generate_button = st.button("📥 Generate & Download Data Sharing Report Template", use_container_width=True, key="generate_report_btn")
                    if generate_button:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        try:
                            status_text.info("🔄 Starting PDF generation...")
                            progress_bar.progress(10)
                            
                            from data_share_templates import create_data_sharing_report_template
                            
                            status_text.info("📄 Creating template structure...")
                            progress_bar.progress(30)
                            
                            status_text.info("🖼️ Adding logo and formatting...")
                            progress_bar.progress(60)
                            
                            filename = create_data_sharing_report_template()
                            
                            progress_bar.progress(90)
                            status_text.info("💾 Saving file...")
                            
                            st.session_state[template_key] = filename
                            st.session_state['report_template_generated'] = True
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Template generated successfully! Download button appears below.")
                            progress_bar.empty()
                            st.rerun()  # Refresh to show download button
                        except Exception as e:
                            progress_bar.empty()
                            status_text.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
                
                # Show download button if template is ready
                if template_key in st.session_state:
                    try:
                        with open(st.session_state[template_key], 'rb') as f:
                            pdf_data = f.read()
                            st.markdown("---")
                            st.markdown("### 📥 Download Template")
                            st.download_button(
                                "📥 Download Data Sharing Report (PDF)",
                                pdf_data,
                                file_name=f"Data_Sharing_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                key="download_template_report"
                            )
                            if st.button("🔄 Generate New Template", use_container_width=True, key="regenerate_report_btn"):
                                if template_key in st.session_state:
                                    try:
                                        os.remove(st.session_state[template_key])
                                    except:
                                        pass
                                del st.session_state[template_key]
                                if 'report_template_generated' in st.session_state:
                                    del st.session_state['report_template_generated']
                                st.success("🔄 Template cleared. Click 'Generate & Download' to create a new one.")
                    except Exception as e:
                        st.error(f"Error loading template: {str(e)}")
                        if template_key in st.session_state:
                            del st.session_state[template_key]
        
        st.markdown("---")
        st.markdown("### ✨ Data Share Template Features")
        col1, col2 = st.columns(2)
        with col1:
            st.write("✅ Agreement information")
            st.write("✅ Terms and conditions")
            st.write("✅ Security requirements")
        with col2:
            st.write("✅ Compliance tracking")
            st.write("✅ Signatures section")
            st.write("✅ Professional layout")
    
    # ============================================
    # USE CASE BRIEF SECTION
    # ============================================
    elif template_category == "📋 Use Case Brief":
        st.subheader("📋 Use Case Brief")
        st.info("Create a simple Use Case Brief template with product image support")
        
        use_case_action = st.radio(
            "Choose Action",
            ["Fill Form Directly", "Download Template"],
            horizontal=True,
            key="use_case_action"
        )
        
        if use_case_action == "Fill Form Directly":
            st.markdown("### Fill Use Case Brief")
            
            from fillable_use_case_brief import load_use_case_brief_form, save_use_case_brief_form, generate_pdf_from_use_case_brief
            saved_data = load_use_case_brief_form()
            
            with st.form("use_case_brief_form", clear_on_submit=False):
                st.markdown("#### Document Information")
                col1, col2 = st.columns(2)
                with col1:
                    use_case_id = st.text_input("Use Case ID *", value=saved_data['data'].get('use_case_id', '') if saved_data and saved_data.get('data') else '')
                    use_case_name = st.text_input("Use Case Name *", value=saved_data['data'].get('use_case_name', '') if saved_data and saved_data.get('data') else '')
                    date = st.date_input("Date *", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('date') else datetime.strptime(saved_data['data'].get('date'), "%Y-%m-%d").date())
                with col2:
                    version = st.text_input("Version", value=saved_data['data'].get('version', '1.0') if saved_data and saved_data.get('data') else '1.0')
                    department = st.text_input("Department", value=saved_data['data'].get('department', '') if saved_data and saved_data.get('data') else '')
                    status = st.selectbox("Status", ["Draft", "Review", "Approved"], 
                                         index=0 if not saved_data or not saved_data.get('data') or saved_data['data'].get('status') not in ["Draft", "Review", "Approved"] else ["Draft", "Review", "Approved"].index(saved_data['data'].get('status')))
                
                st.markdown("---")
                st.markdown("#### Use Case Overview")
                description = st.text_area("Description *", value=saved_data['data'].get('description', '') if saved_data and saved_data.get('data') else '', height=100)
                business_objective = st.text_area("Business Objective *", value=saved_data['data'].get('business_objective', '') if saved_data and saved_data.get('data') else '', height=100)
                stakeholders = st.text_input("Stakeholders", value=saved_data['data'].get('stakeholders', '') if saved_data and saved_data.get('data') else '')
                
                st.markdown("---")
                st.markdown("#### Product Image")
                product_image = st.file_uploader("Upload Product Image", type=['png', 'jpg', 'jpeg'], 
                                                help="Upload an image of the product (PNG, JPG, JPEG)")
                
                # Show uploaded image if exists
                if product_image:
                    st.image(product_image, caption="Product Image Preview", width=400)
                
                # Check if saved image exists
                saved_image_path = None
                if saved_data and saved_data.get('image_path'):
                    try:
                        if os.path.exists(saved_data['image_path']):
                            st.image(saved_data['image_path'], caption="Saved Product Image", width=400)
                            saved_image_path = saved_data['image_path']
                    except:
                        pass
                
                st.markdown("---")
                st.markdown("#### Capabilities & Features")
                capabilities = st.text_area("Capabilities", value=saved_data['data'].get('capabilities', '') if saved_data and saved_data.get('data') else '', height=100, help="Describe the key capabilities and features of the product/use case")
                
                st.markdown("---")
                st.markdown("#### Links & Resources")
                col1, col2 = st.columns(2)
                with col1:
                    documentation_link = st.text_input("Documentation Link", value=saved_data['data'].get('documentation_link', '') if saved_data and saved_data.get('data') else '', help="URL to product documentation")
                    demo_link = st.text_input("Demo Link", value=saved_data['data'].get('demo_link', '') if saved_data and saved_data.get('data') else '', help="URL to product demo")
                with col2:
                    repository_link = st.text_input("Repository Link", value=saved_data['data'].get('repository_link', '') if saved_data and saved_data.get('data') else '', help="URL to code repository")
                    additional_links = st.text_area("Additional Links", value=saved_data['data'].get('additional_links', '') if saved_data and saved_data.get('data') else '', height=60, help="Additional relevant links (one per line)")
                
                st.markdown("---")
                st.markdown("#### Technical Details")
                col1, col2 = st.columns(2)
                with col1:
                    data_sources = st.text_input("Data Sources", value=saved_data['data'].get('data_sources', '') if saved_data and saved_data.get('data') else '')
                    data_types = st.text_input("Data Types", value=saved_data['data'].get('data_types', '') if saved_data and saved_data.get('data') else '')
                with col2:
                    data_volume = st.text_input("Data Volume", value=saved_data['data'].get('data_volume', '') if saved_data and saved_data.get('data') else '')
                processing_requirements = st.text_area("Processing Requirements", value=saved_data['data'].get('processing_requirements', '') if saved_data and saved_data.get('data') else '', height=80)
                
                st.markdown("---")
                st.markdown("#### Compliance & Security")
                col1, col2 = st.columns(2)
                with col1:
                    ndmo_compliance = st.selectbox("NDMO Compliance", ["Compliant", "Non-Compliant"], 
                                                   index=0 if not saved_data or not saved_data.get('data') or saved_data['data'].get('ndmo_compliance') not in ["Compliant", "Non-Compliant"] else ["Compliant", "Non-Compliant"].index(saved_data['data'].get('ndmo_compliance')))
                    data_classification = st.selectbox("Data Classification", ["Public", "Internal", "Restricted", "Confidential"], 
                                                      index=0 if not saved_data or not saved_data.get('data') or saved_data['data'].get('data_classification') not in ["Public", "Internal", "Restricted", "Confidential"] else ["Public", "Internal", "Restricted", "Confidential"].index(saved_data['data'].get('data_classification')))
                with col2:
                    ndi_compliance = st.selectbox("NDI Compliance", ["Compliant", "Non-Compliant"], 
                                                  index=0 if not saved_data or not saved_data.get('data') or saved_data['data'].get('ndi_compliance') not in ["Compliant", "Non-Compliant"] else ["Compliant", "Non-Compliant"].index(saved_data['data'].get('ndi_compliance')))
                security_requirements = st.text_area("Security Requirements", value=saved_data['data'].get('security_requirements', '') if saved_data and saved_data.get('data') else '', height=80)
                
                st.markdown("---")
                st.markdown("#### Signatures")
                col1, col2 = st.columns(2)
                with col1:
                    prepared_by = st.text_input("Prepared By", value=saved_data['data'].get('prepared_by', '') if saved_data and saved_data.get('data') else '')
                    prepared_date = st.date_input("Prepared Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('prepared_date') else datetime.strptime(saved_data['data'].get('prepared_date'), "%Y-%m-%d").date())
                    reviewed_by = st.text_input("Reviewed By", value=saved_data['data'].get('reviewed_by', '') if saved_data and saved_data.get('data') else '')
                    reviewed_date = st.date_input("Reviewed Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('reviewed_date') else datetime.strptime(saved_data['data'].get('reviewed_date'), "%Y-%m-%d").date())
                with col2:
                    approved_by = st.text_input("Approved By", value=saved_data['data'].get('approved_by', '') if saved_data and saved_data.get('data') else '')
                    approved_date = st.date_input("Approved Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('approved_date') else datetime.strptime(saved_data['data'].get('approved_date'), "%Y-%m-%d").date())
                
                submitted = st.form_submit_button("💾 Save & Generate PDF", use_container_width=True)
                
                if submitted:
                    if not use_case_id or not use_case_name or not description or not business_objective:
                        st.error("Please fill in all required fields (marked with *)")
                    else:
                        # Show loading with progress
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            status_text.info("💾 Saving Use Case Brief...")
                            progress_bar.progress(10)
                            
                            # Save uploaded image
                            image_path = saved_image_path
                            if product_image:
                                try:
                                    os.makedirs("uploaded_images", exist_ok=True)
                                    image_path = f"uploaded_images/product_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{product_image.name}"
                                    with open(image_path, "wb") as f:
                                        f.write(product_image.getbuffer())
                                except Exception as e:
                                    st.warning(f"Could not save image: {str(e)}")
                                    image_path = None
                            
                            form_data = {
                            'use_case_id': use_case_id,
                            'use_case_name': use_case_name,
                            'date': date.strftime("%Y-%m-%d"),
                            'version': version,
                            'department': department,
                            'status': status,
                            'description': description,
                            'business_objective': business_objective,
                            'stakeholders': stakeholders,
                            'capabilities': capabilities,
                            'documentation_link': documentation_link,
                            'demo_link': demo_link,
                            'repository_link': repository_link,
                            'additional_links': additional_links,
                            'data_sources': data_sources,
                            'data_types': data_types,
                            'data_volume': data_volume,
                            'processing_requirements': processing_requirements,
                            'ndmo_compliance': ndmo_compliance,
                            'ndi_compliance': ndi_compliance,
                            'data_classification': data_classification,
                            'security_requirements': security_requirements,
                            'prepared_by': prepared_by,
                            'prepared_date': prepared_date.strftime("%Y-%m-%d"),
                            'reviewed_by': reviewed_by,
                            'reviewed_date': reviewed_date.strftime("%Y-%m-%d"),
                            'approved_by': approved_by,
                            'approved_date': approved_date.strftime("%Y-%m-%d")
                        }
                            
                            status_text.info("💾 Saving form data...")
                            progress_bar.progress(30)
                            
                            json_file = save_use_case_brief_form(form_data, image_path)
                            
                            status_text.info("📄 Generating PDF...")
                            progress_bar.progress(50)
                            
                            pdf_file = generate_pdf_from_use_case_brief(form_data, image_path)
                            
                            progress_bar.progress(80)
                            status_text.info("✅ Finalizing...")
                            
                            st.session_state['use_case_brief_json'] = json_file
                            st.session_state['use_case_brief_pdf'] = pdf_file
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Form saved successfully! Scroll down to download.")
                            progress_bar.empty()
                        except Exception as e:
                            progress_bar.empty()
                            status_text.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
            
            # Download buttons outside form
            if 'use_case_brief_json' in st.session_state and 'use_case_brief_pdf' in st.session_state:
                st.markdown("---")
                st.markdown("### 📥 Download Files")
                col1, col2 = st.columns(2)
                with col1:
                    try:
                        with open(st.session_state['use_case_brief_json'], 'rb') as f:
                            json_data = f.read()
                            st.download_button(
                                "📥 Download JSON", 
                                json_data, 
                                file_name=f"Use_Case_Brief_{datetime.now().strftime('%Y%m%d')}.json",
                                mime="application/json",
                                key="download_json_use_case",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error loading JSON: {str(e)}")
                with col2:
                    try:
                        with open(st.session_state['use_case_brief_pdf'], 'rb') as f:
                            pdf_data = f.read()
                            st.download_button(
                                "📥 Download PDF", 
                                pdf_data,
                                file_name=f"Use_Case_Brief_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                key="download_pdf_use_case",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error loading PDF: {str(e)}")
        
        else:  # Download Template
            st.markdown("### Download Use Case Brief Template")
            st.write("Download a blank template to fill manually")
            
            template_key = 'use_case_brief_template_file'
            
            if template_key not in st.session_state:
                generate_button = st.button("📥 Generate & Download Use Case Brief Template", use_container_width=True, key="generate_use_case_btn")
                if generate_button:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    try:
                        status_text.info("🔄 Starting PDF generation...")
                        progress_bar.progress(10)
                        
                        from use_case_brief_template import create_use_case_brief_template
                        
                        status_text.info("📄 Creating template structure...")
                        progress_bar.progress(30)
                        
                        status_text.info("🖼️ Adding logo and formatting...")
                        progress_bar.progress(60)
                        
                        filename = create_use_case_brief_template()
                        
                        progress_bar.progress(90)
                        status_text.info("💾 Saving file...")
                        
                        st.session_state[template_key] = filename
                        st.session_state['use_case_template_generated'] = True
                        
                        progress_bar.progress(100)
                        status_text.success("✅ Template generated successfully! Download button appears below.")
                        progress_bar.empty()
                        st.rerun()  # Refresh to show download button
                    except Exception as e:
                        progress_bar.empty()
                        status_text.error(f"❌ Error: {str(e)}")
                        import traceback
                        with st.expander("Error Details"):
                            st.code(traceback.format_exc())
            
            if template_key in st.session_state:
                try:
                    with open(st.session_state[template_key], 'rb') as f:
                        pdf_data = f.read()
                        st.markdown("---")
                        st.markdown("### 📥 Download Template")
                        st.download_button(
                            "📥 Download Use Case Brief (PDF)",
                            pdf_data,
                            file_name=f"Use_Case_Brief_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_template_use_case"
                        )
                        if st.button("🔄 Generate New Template", use_container_width=True, key="regenerate_use_case_btn"):
                            if template_key in st.session_state:
                                try:
                                    os.remove(st.session_state[template_key])
                                except:
                                    pass
                            del st.session_state[template_key]
                            if 'use_case_template_generated' in st.session_state:
                                del st.session_state['use_case_template_generated']
                            st.success("🔄 Template cleared. Click 'Generate & Download' to create a new one.")
                except Exception as e:
                    st.error(f"Error loading template: {str(e)}")
                    if template_key in st.session_state:
                        del st.session_state[template_key]
    
    # ============================================
    # TECHNICAL REPORTS SECTION
    # ============================================
    elif template_category == "📈 Technical Reports":
        st.subheader("📈 Technical Reports")
        st.info("Additional technical reports for comprehensive compliance documentation")
        
        tech_report_type = st.radio(
            "Select Technical Report",
            ["Gap Analysis Report", "Risk Assessment Report"],
            horizontal=True,
            key="tech_report_type"
        )
        
        action_type = st.radio(
            "Choose Action",
            ["Fill Form Directly", "Download Template"],
            horizontal=True,
            key="tech_report_action"
        )
        
        if action_type == "Fill Form Directly":
            if tech_report_type == "Gap Analysis Report":
                st.markdown("### Fill Gap Analysis Report")
                
                from fillable_technical_reports import load_technical_report_form, save_technical_report_form, generate_pdf_from_technical_report
                saved_data = load_technical_report_form("gap_analysis")
                
                with st.form("gap_analysis_form", clear_on_submit=False):
                    st.markdown("#### Report Information")
                    col1, col2 = st.columns(2)
                    with col1:
                        report_date = st.date_input("Report Date *", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('report_date') else datetime.strptime(saved_data['data'].get('report_date'), "%Y-%m-%d").date())
                        entity_name = st.text_input("Entity Name *", value=saved_data['data'].get('entity_name', '') if saved_data and saved_data.get('data') else '')
                        period_from = st.date_input("Assessment Period From *", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('period_from') else datetime.strptime(saved_data['data'].get('period_from'), "%Y-%m-%d").date())
                        department = st.text_input("Department", value=saved_data['data'].get('department', '') if saved_data and saved_data.get('data') else '')
                    with col2:
                        period_to = st.date_input("Assessment Period To *", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('period_to') else datetime.strptime(saved_data['data'].get('period_to'), "%Y-%m-%d").date())
                        prepared_by = st.text_input("Prepared By *", value=saved_data['data'].get('prepared_by', '') if saved_data and saved_data.get('data') else '')
                        review_date = st.date_input("Review Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('review_date') else datetime.strptime(saved_data['data'].get('review_date'), "%Y-%m-%d").date())
                    
                    st.markdown("---")
                    st.markdown("#### Gap Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        total_controls = st.number_input("Total Controls Assessed", min_value=0, value=saved_data['data'].get('total_controls', 0) if saved_data and saved_data.get('data') else 0)
                        compliant_controls = st.number_input("Compliant Controls", min_value=0, value=saved_data['data'].get('compliant_controls', 0) if saved_data and saved_data.get('data') else 0)
                    with col2:
                        partially_compliant = st.number_input("Partially Compliant", min_value=0, value=saved_data['data'].get('partially_compliant', 0) if saved_data and saved_data.get('data') else 0)
                        non_compliant = st.number_input("Non-Compliant", min_value=0, value=saved_data['data'].get('non_compliant', 0) if saved_data and saved_data.get('data') else 0)
                    with col3:
                        gap_percentage = st.number_input("Gap Percentage", min_value=0.0, max_value=100.0, value=float(saved_data['data'].get('gap_percentage', 0)) if saved_data and saved_data.get('data') else 0.0)
                        priority_gaps = st.number_input("Priority Gaps (P1)", min_value=0, value=saved_data['data'].get('priority_gaps', 0) if saved_data and saved_data.get('data') else 0)
                    
                    st.markdown("---")
                    st.markdown("#### Gap Details")
                    gap_details = st.text_area("Gap Details", value=saved_data['data'].get('gap_details', '') if saved_data and saved_data.get('data') else '', height=150)
                    
                    st.markdown("---")
                    st.markdown("#### Remediation Plan")
                    remediation_plan = st.text_area("Remediation Plan", value=saved_data['data'].get('remediation_plan', '') if saved_data and saved_data.get('data') else '', height=150)
                    
                    st.markdown("---")
                    st.markdown("#### Signatures")
                    col1, col2 = st.columns(2)
                    with col1:
                        prepared_by_signature = st.text_input("Prepared By", value=saved_data['data'].get('prepared_by_signature', '') if saved_data and saved_data.get('data') else '')
                        prepared_date = st.date_input("Prepared Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('prepared_date') else datetime.strptime(saved_data['data'].get('prepared_date'), "%Y-%m-%d").date())
                        reviewed_by = st.text_input("Reviewed By", value=saved_data['data'].get('reviewed_by', '') if saved_data and saved_data.get('data') else '')
                        reviewed_date = st.date_input("Reviewed Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('reviewed_date') else datetime.strptime(saved_data['data'].get('reviewed_date'), "%Y-%m-%d").date())
                    with col2:
                        approved_by = st.text_input("Approved By", value=saved_data['data'].get('approved_by', '') if saved_data and saved_data.get('data') else '')
                        approved_date = st.date_input("Approved Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('approved_date') else datetime.strptime(saved_data['data'].get('approved_date'), "%Y-%m-%d").date())
                    
                    submitted = st.form_submit_button("💾 Save & Generate PDF", use_container_width=True)
                    
                    if submitted:
                        if not entity_name or not prepared_by or not period_from or not period_to:
                            st.error("Please fill in all required fields (marked with *)")
                        else:
                            form_data = {
                                'report_date': report_date.strftime("%Y-%m-%d"),
                                'entity_name': entity_name,
                                'period_from': period_from.strftime("%Y-%m-%d"),
                                'period_to': period_to.strftime("%Y-%m-%d"),
                                'department': department,
                                'prepared_by': prepared_by,
                                'review_date': review_date.strftime("%Y-%m-%d"),
                                'total_controls': total_controls,
                                'compliant_controls': compliant_controls,
                                'partially_compliant': partially_compliant,
                                'non_compliant': non_compliant,
                                'gap_percentage': gap_percentage,
                                'priority_gaps': priority_gaps,
                                'gap_details': gap_details,
                                'remediation_plan': remediation_plan,
                                'prepared_by_signature': prepared_by_signature,
                                'prepared_date': prepared_date.strftime("%Y-%m-%d"),
                                'reviewed_by': reviewed_by,
                                'reviewed_date': reviewed_date.strftime("%Y-%m-%d"),
                                'approved_by': approved_by,
                                'approved_date': approved_date.strftime("%Y-%m-%d")
                            }
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(20)
                                
                                json_file = save_technical_report_form("gap_analysis", form_data)
                                
                                status_text.info("📄 Generating PDF...")
                                progress_bar.progress(50)
                                
                                pdf_file = generate_pdf_from_technical_report("gap_analysis", form_data)
                                
                                progress_bar.progress(80)
                                status_text.info("✅ Finalizing...")
                                
                                st.session_state['gap_analysis_json'] = json_file
                                st.session_state['gap_analysis_pdf'] = pdf_file
                                
                                progress_bar.progress(100)
                                status_text.success("✅ Form saved successfully! Scroll down to download.")
                                progress_bar.empty()
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                
                # Download buttons outside form
                if 'gap_analysis_json' in st.session_state and 'gap_analysis_pdf' in st.session_state:
                    st.markdown("---")
                    st.markdown("### 📥 Download Files")
                    col1, col2 = st.columns(2)
                    with col1:
                        try:
                            with open(st.session_state['gap_analysis_json'], 'rb') as f:
                                json_data = f.read()
                                st.download_button(
                                    "📥 Download JSON", 
                                    json_data, 
                                    file_name=f"Gap_Analysis_Report_{datetime.now().strftime('%Y%m%d')}.json",
                                    mime="application/json",
                                    key="download_json_gap",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading JSON: {str(e)}")
                    with col2:
                        try:
                            with open(st.session_state['gap_analysis_pdf'], 'rb') as f:
                                pdf_data = f.read()
                                st.download_button(
                                    "📥 Download PDF", 
                                    pdf_data,
                                    file_name=f"Gap_Analysis_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                                    mime="application/pdf",
                                    key="download_pdf_gap",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading PDF: {str(e)}")
            
            elif tech_report_type == "Risk Assessment Report":
                st.markdown("### Fill Risk Assessment Report")
                
                from fillable_technical_reports import load_technical_report_form, save_technical_report_form, generate_pdf_from_technical_report
                saved_data = load_technical_report_form("risk_assessment")
                
                with st.form("risk_assessment_form", clear_on_submit=False):
                    st.markdown("#### Report Information")
                    col1, col2 = st.columns(2)
                    with col1:
                        report_date = st.date_input("Report Date *", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('report_date') else datetime.strptime(saved_data['data'].get('report_date'), "%Y-%m-%d").date())
                        entity_name = st.text_input("Entity Name *", value=saved_data['data'].get('entity_name', '') if saved_data and saved_data.get('data') else '')
                        assessment_date = st.date_input("Assessment Date *", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('assessment_date') else datetime.strptime(saved_data['data'].get('assessment_date'), "%Y-%m-%d").date())
                        department = st.text_input("Department", value=saved_data['data'].get('department', '') if saved_data and saved_data.get('data') else '')
                    with col2:
                        assessed_by = st.text_input("Assessed By *", value=saved_data['data'].get('assessed_by', '') if saved_data and saved_data.get('data') else '')
                        review_date = st.date_input("Review Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('review_date') else datetime.strptime(saved_data['data'].get('review_date'), "%Y-%m-%d").date())
                    
                    st.markdown("---")
                    st.markdown("#### Risk Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        total_risks = st.number_input("Total Risks Identified", min_value=0, value=saved_data['data'].get('total_risks', 0) if saved_data and saved_data.get('data') else 0)
                        high_risk = st.number_input("High Risk", min_value=0, value=saved_data['data'].get('high_risk', 0) if saved_data and saved_data.get('data') else 0)
                    with col2:
                        medium_risk = st.number_input("Medium Risk", min_value=0, value=saved_data['data'].get('medium_risk', 0) if saved_data and saved_data.get('data') else 0)
                        low_risk = st.number_input("Low Risk", min_value=0, value=saved_data['data'].get('low_risk', 0) if saved_data and saved_data.get('data') else 0)
                    with col3:
                        risk_score = st.number_input("Risk Score (Average)", min_value=0.0, max_value=10.0, value=float(saved_data['data'].get('risk_score', 0)) if saved_data and saved_data.get('data') else 0.0)
                        mitigation_status = st.selectbox("Mitigation Status", ["Planned", "In Progress", "Completed"], 
                                                         index=0 if not saved_data or not saved_data.get('data') or saved_data['data'].get('mitigation_status') not in ["Planned", "In Progress", "Completed"] else ["Planned", "In Progress", "Completed"].index(saved_data['data'].get('mitigation_status')))
                    
                    st.markdown("---")
                    st.markdown("#### Risk Details")
                    risk_details = st.text_area("Risk Details", value=saved_data['data'].get('risk_details', '') if saved_data and saved_data.get('data') else '', height=150)
                    
                    st.markdown("---")
                    st.markdown("#### Mitigation Plan")
                    mitigation_plan = st.text_area("Mitigation Plan", value=saved_data['data'].get('mitigation_plan', '') if saved_data and saved_data.get('data') else '', height=150)
                    
                    st.markdown("---")
                    st.markdown("#### Signatures")
                    col1, col2 = st.columns(2)
                    with col1:
                        assessed_by_signature = st.text_input("Assessed By", value=saved_data['data'].get('assessed_by_signature', '') if saved_data and saved_data.get('data') else '')
                        assessed_date = st.date_input("Assessed Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('assessed_date') else datetime.strptime(saved_data['data'].get('assessed_date'), "%Y-%m-%d").date())
                        reviewed_by = st.text_input("Reviewed By", value=saved_data['data'].get('reviewed_by', '') if saved_data and saved_data.get('data') else '')
                        reviewed_date = st.date_input("Reviewed Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('reviewed_date') else datetime.strptime(saved_data['data'].get('reviewed_date'), "%Y-%m-%d").date())
                    with col2:
                        approved_by = st.text_input("Approved By", value=saved_data['data'].get('approved_by', '') if saved_data and saved_data.get('data') else '')
                        approved_date = st.date_input("Approved Date", value=datetime.now().date() if not saved_data or not saved_data.get('data') or not saved_data['data'].get('approved_date') else datetime.strptime(saved_data['data'].get('approved_date'), "%Y-%m-%d").date())
                    
                    submitted = st.form_submit_button("💾 Save & Generate PDF", use_container_width=True)
                    
                    if submitted:
                        if not entity_name or not assessed_by or not assessment_date:
                            st.error("Please fill in all required fields (marked with *)")
                        else:
                            form_data = {
                                'report_date': report_date.strftime("%Y-%m-%d"),
                                'entity_name': entity_name,
                                'assessment_date': assessment_date.strftime("%Y-%m-%d"),
                                'department': department,
                                'assessed_by': assessed_by,
                                'review_date': review_date.strftime("%Y-%m-%d"),
                                'total_risks': total_risks,
                                'high_risk': high_risk,
                                'medium_risk': medium_risk,
                                'low_risk': low_risk,
                                'risk_score': risk_score,
                                'mitigation_status': mitigation_status,
                                'risk_details': risk_details,
                                'mitigation_plan': mitigation_plan,
                                'assessed_by_signature': assessed_by_signature,
                                'assessed_date': assessed_date.strftime("%Y-%m-%d"),
                                'reviewed_by': reviewed_by,
                                'reviewed_date': reviewed_date.strftime("%Y-%m-%d"),
                                'approved_by': approved_by,
                                'approved_date': approved_date.strftime("%Y-%m-%d")
                            }
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.info("💾 Saving form data...")
                                progress_bar.progress(20)
                                
                                json_file = save_technical_report_form("risk_assessment", form_data)
                                
                                status_text.info("📄 Generating PDF...")
                                progress_bar.progress(50)
                                
                                pdf_file = generate_pdf_from_technical_report("risk_assessment", form_data)
                                
                                progress_bar.progress(80)
                                status_text.info("✅ Finalizing...")
                                
                                st.session_state['risk_assessment_json'] = json_file
                                st.session_state['risk_assessment_pdf'] = pdf_file
                                
                                progress_bar.progress(100)
                                status_text.success("✅ Form saved successfully! Scroll down to download.")
                                progress_bar.empty()
                            except Exception as e:
                                progress_bar.empty()
                                status_text.error(f"❌ Error: {str(e)}")
                                import traceback
                                with st.expander("Error Details"):
                                    st.code(traceback.format_exc())
                
                # Download buttons outside form
                if 'risk_assessment_json' in st.session_state and 'risk_assessment_pdf' in st.session_state:
                    st.markdown("---")
                    st.markdown("### 📥 Download Files")
                    col1, col2 = st.columns(2)
                    with col1:
                        try:
                            with open(st.session_state['risk_assessment_json'], 'rb') as f:
                                json_data = f.read()
                                st.download_button(
                                    "📥 Download JSON", 
                                    json_data, 
                                    file_name=f"Risk_Assessment_Report_{datetime.now().strftime('%Y%m%d')}.json",
                                    mime="application/json",
                                    key="download_json_risk",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading JSON: {str(e)}")
                    with col2:
                        try:
                            with open(st.session_state['risk_assessment_pdf'], 'rb') as f:
                                pdf_data = f.read()
                                st.download_button(
                                    "📥 Download PDF", 
                                    pdf_data,
                                    file_name=f"Risk_Assessment_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                                    mime="application/pdf",
                                    key="download_pdf_risk",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error loading PDF: {str(e)}")
        
        else:  # Download Template
            if tech_report_type == "Gap Analysis Report":
                st.markdown("### Download Gap Analysis Report Template")
                st.write("Download a blank template to fill manually")
                
                template_key = 'gap_analysis_template_file'
                
                if template_key not in st.session_state:
                    generate_button = st.button("📥 Generate & Download Gap Analysis Report Template", use_container_width=True, key="generate_gap_btn")
                    if generate_button:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        try:
                            status_text.info("🔄 Starting PDF generation...")
                            progress_bar.progress(10)
                            
                            from technical_reports import create_gap_analysis_report
                            
                            status_text.info("📄 Creating template structure...")
                            progress_bar.progress(30)
                            
                            status_text.info("🖼️ Adding logo and formatting...")
                            progress_bar.progress(60)
                            
                            filename = create_gap_analysis_report()
                            
                            progress_bar.progress(90)
                            status_text.info("💾 Saving file...")
                            
                            st.session_state[template_key] = filename
                            st.session_state['gap_template_generated'] = True
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Template generated successfully! Download button appears below.")
                            progress_bar.empty()
                            st.rerun()  # Refresh to show download button
                        except Exception as e:
                            progress_bar.empty()
                            status_text.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
                
                if template_key in st.session_state:
                    try:
                        with open(st.session_state[template_key], 'rb') as f:
                            pdf_data = f.read()
                            st.markdown("---")
                            st.markdown("### 📥 Download Template")
                            st.download_button(
                                "📥 Download Gap Analysis Report (PDF)",
                                pdf_data,
                                file_name=f"Gap_Analysis_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                key="download_template_gap"
                            )
                            if st.button("🔄 Generate New Template", use_container_width=True, key="regenerate_gap_btn"):
                                if template_key in st.session_state:
                                    try:
                                        os.remove(st.session_state[template_key])
                                    except:
                                        pass
                                del st.session_state[template_key]
                                if 'gap_template_generated' in st.session_state:
                                    del st.session_state['gap_template_generated']
                                st.success("🔄 Template cleared. Click 'Generate & Download' to create a new one.")
                    except Exception as e:
                        st.error(f"Error loading template: {str(e)}")
                        if template_key in st.session_state:
                            del st.session_state[template_key]
            
            elif tech_report_type == "Risk Assessment Report":
                st.markdown("### Download Risk Assessment Report Template")
                st.write("Download a blank template to fill manually")
                
                template_key = 'risk_assessment_template_file'
                
                if template_key not in st.session_state:
                    generate_button = st.button("📥 Generate & Download Risk Assessment Report Template", use_container_width=True, key="generate_risk_btn")
                    if generate_button:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        try:
                            status_text.info("🔄 Starting PDF generation...")
                            progress_bar.progress(10)
                            
                            from technical_reports import create_risk_assessment_report
                            
                            status_text.info("📄 Creating template structure...")
                            progress_bar.progress(30)
                            
                            status_text.info("🖼️ Adding logo and formatting...")
                            progress_bar.progress(60)
                            
                            filename = create_risk_assessment_report()
                            
                            progress_bar.progress(90)
                            status_text.info("💾 Saving file...")
                            
                            st.session_state[template_key] = filename
                            st.session_state['risk_template_generated'] = True
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Template generated successfully! Download button appears below.")
                            progress_bar.empty()
                            st.rerun()  # Refresh to show download button
                        except Exception as e:
                            progress_bar.empty()
                            status_text.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Error Details"):
                                st.code(traceback.format_exc())
                
                if template_key in st.session_state:
                    try:
                        with open(st.session_state[template_key], 'rb') as f:
                            pdf_data = f.read()
                            st.markdown("---")
                            st.markdown("### 📥 Download Template")
                            st.download_button(
                                "📥 Download Risk Assessment Report (PDF)",
                                pdf_data,
                                file_name=f"Risk_Assessment_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                key="download_template_risk"
                            )
                            if st.button("🔄 Generate New Template", use_container_width=True, key="regenerate_risk_btn"):
                                if template_key in st.session_state:
                                    try:
                                        os.remove(st.session_state[template_key])
                                    except:
                                        pass
                                del st.session_state[template_key]
                                if 'risk_template_generated' in st.session_state:
                                    del st.session_state['risk_template_generated']
                                st.success("🔄 Template cleared. Click 'Generate & Download' to create a new one.")
                    except Exception as e:
                        st.error(f"Error loading template: {str(e)}")
                        if template_key in st.session_state:
                            del st.session_state[template_key]

def show_import_data():
    st.header("📥 Import Data from Excel")
    st.markdown("Upload an Excel file containing controls, specifications, and evidence requirements")
    
    st.info("""
    **Expected Excel Structure:**
    - **Sheet 1 (Controls):** Control ID, Control Name, Domain, Category, Description, Phase, Priority
    - **Sheet 2 (Specifications):** Spec ID, Control ID, Specification Text, Priority
    - **Sheet 3 (Evidence):** Spec ID/Control ID, Evidence Type, Description, Format, Required
    
    The importer will automatically detect column names in both English and Arabic.
    """)
    
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=['xlsx', 'xls'],
        help="Upload an Excel file with controls and specifications data"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            from excel_importer import import_controls_from_excel
            
            with st.spinner("Importing data from Excel..."):
                result = import_controls_from_excel(tmp_path)
            
            if result:
                st.success("✅ Data imported successfully!")
                
                # Display statistics
                stats = result['statistics']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Controls", stats['total_controls'])
                with col2:
                    st.metric("Specifications", stats['total_specifications'])
                with col3:
                    st.metric("Evidence Items", stats['total_evidence_items'])
                
                st.markdown("---")
                
                # Show sample data
                st.subheader("Sample Imported Data")
                
                tab1, tab2, tab3 = st.tabs(["Controls", "Specifications", "Evidence"])
                
                with tab1:
                    if result['controls']:
                        st.write(f"Showing first 10 of {len(result['controls'])} controls:")
                        controls_df = pd.DataFrame(result['controls'][:10])
                        st.dataframe(controls_df[['id', 'title', 'category', 'domain']], use_container_width=True)
                    else:
                        st.info("No controls found in the import")
                
                with tab2:
                    if result['specifications']:
                        st.write(f"Showing first 10 of {len(result['specifications'])} specifications:")
                        specs_df = pd.DataFrame(result['specifications'][:10])
                        st.dataframe(specs_df[['spec_id', 'control_id', 'priority', 'specification_text']], use_container_width=True)
                    else:
                        st.info("No specifications found in the import")
                
                with tab3:
                    if result['evidence']:
                        evidence_list = []
                        for key, items in list(result['evidence'].items())[:10]:
                            for item in items:
                                evidence_list.append({
                                    'Control/Spec ID': key,
                                    'Type': item['type'],
                                    'Description': item['description'],
                                    'Format': item['format'],
                                    'Required': item['required']
                                })
                        if evidence_list:
                            st.write(f"Showing sample evidence items:")
                            evidence_df = pd.DataFrame(evidence_list)
                            st.dataframe(evidence_df, use_container_width=True)
                    else:
                        st.info("No evidence requirements found in the import")
                
                st.markdown("---")
                
                # Option to use imported data
                st.subheader("Use Imported Data")
                st.info("The imported data has been saved. You can now use it in the application.")
                
                if st.button("🔄 Reload Application with Imported Data", use_container_width=True):
                    # Store imported data in session state
                    st.session_state['imported_data'] = result
                    st.success("✅ Imported data loaded! The application will now use this data.")
                    st.info("💡 Refresh the page or navigate to other pages to see the imported data.")
                    st.rerun()
                
                # Auto-load SANS file if exists
                if "SANS" in uploaded_file.name or "sans" in uploaded_file.name.lower():
                    st.info("💡 This appears to be a SANS file. The data structure has been automatically detected!")
                
                # Download imported data as JSON
                import json
                json_data = json.dumps(result, indent=2, ensure_ascii=False)
                st.download_button(
                    "📥 Download Imported Data as JSON",
                    json_data.encode('utf-8'),
                    file_name=f"imported_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            else:
                st.error("❌ Failed to import data. Please check the Excel file format.")
        
        except Exception as e:
            st.error(f"❌ Error importing data: {str(e)}")
            import traceback
            with st.expander("Error Details"):
                st.code(traceback.format_exc())
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    else:
        st.info("👆 Please upload an Excel file to begin import")
        
        # Check if SANS file exists and offer to import it
        import os
        sans_file = "SANS - NDI  NDMO Assessment Tool_(Data Management).xlsx"
        if os.path.exists(sans_file):
            st.markdown("---")
            st.subheader("📁 Found SANS Assessment Tool File")
            st.info(f"Found: {sans_file}")
            
            if st.button("🚀 Import SANS File Automatically", use_container_width=True):
                try:
                    from import_from_sans_excel import import_from_sans_excel
                    with st.spinner("Importing SANS file..."):
                        result = import_from_sans_excel(sans_file)
                    if result:
                        st.success("✅ SANS file imported successfully!")
                        st.session_state['imported_data'] = result
                        st.rerun()
                except Exception as e:
                    st.error(f"Error importing SANS file: {str(e)}")
        
        # Show example structure
        with st.expander("📋 Example Excel Structure"):
            st.markdown("""
            ### Sheet 1: Controls
            | Control ID | Control Name | Domain | Category | Description | Phase | Priority |
            |------------|--------------|--------|----------|-------------|-------|----------|
            | DG-001 | Data Governance Framework | Data Governance | Framework | Establish governance framework | Assessment & Planning | High |
            
            ### Sheet 2: Specifications
            | Spec ID | Control ID | Specification Text | Priority |
            |---------|------------|-------------------|----------|
            | DG.1.1 | DG-001 | Establish data governance charter | P1 |
            
            ### Sheet 3: Evidence
            | Spec ID | Evidence Type | Description | Format | Required |
            |---------|--------------|-------------|--------|----------|
            | DG.1.1 | Policy Document | Governance charter document | PDF | Yes |
            """)

def show_compliance_phases():
    st.header("📋 Compliance Phases")
    
    phases = get_phases()
    
    for phase in phases:
        phase_id = phase.get('id', phase.get('number', 'N/A'))
        phase_name = phase.get('name', 'Unknown')
        
        with st.expander(f"**Phase {phase_id}: {phase_name}**", expanded=False):
            st.markdown(f"**Description:** {phase.get('description', 'N/A')}")
            st.markdown(f"**Controls Count:** {phase.get('controls_count', 0)}")
            
            # Phase activities (generic)
            st.markdown("### Key Activities")
            activities = phase.get('activities', [
                "Define compliance objectives",
                "Identify required controls",
                "Assign responsibilities",
                "Establish timelines",
                "Document processes"
            ])
            for activity in activities[:5]:
                st.write(f"• {activity}")
            
            # Phase deliverables (generic)
            st.markdown("### Expected Deliverables")
            deliverables = phase.get('deliverables', [
                "Compliance documentation",
                "Control implementation reports",
                "Evidence collection",
                "Status updates"
            ])
            for deliverable in deliverables[:5]:
                st.write(f"• {deliverable}")
            
            # Controls in this phase
            all_controls = get_all_controls()
            phase_controls = [c for c in all_controls if c.get('phase') == phase_name or phase_name.lower() in str(c.get('phase', '')).lower()]
            
            if phase_controls:
                st.markdown(f"### Controls in {phase_name} Phase")
                st.info(f"Found {len(phase_controls)} control(s) in this phase")
                for ctrl in phase_controls[:10]:  # Show first 10
                    ctrl_id = ctrl.get('id') or ctrl.get('control_id', 'N/A')
                    ctrl_title = ctrl.get('title') or ctrl.get('control_name', 'N/A')
                    st.write(f"• **{ctrl_id}**: {ctrl_title}")
                if len(phase_controls) > 10:
                    st.info(f"Showing 10 of {len(phase_controls)} controls")
            else:
                st.info(f"No controls assigned to {phase_name} phase yet")
            if phase_controls:
                st.markdown(f"### Controls in {phase_name} Phase ({len(phase_controls)})")
                for ctrl in phase_controls:
                    ctrl_id = ctrl.get('id') or ctrl.get('control_id', 'N/A')
                    ctrl_title = ctrl.get('title') or ctrl.get('control_name', 'N/A')
                    status = st.session_state.compliance_data.get(ctrl_id, {}).get('status', 'Not Started')
                    status_color = {
                        'Compliant': '🟢',
                        'In Progress': '🟡',
                        'Non-Compliant': '🔴',
                        'Not Started': '⚪'
                    }
                    st.write(f"{status_color.get(status, '⚪')} **{ctrl_id}**: {ctrl_title}")
            else:
                st.info(f"No controls assigned to {phase_name} phase yet")

def show_calculations_scoring():
    st.header("📊 Calculations & Scoring")
    st.markdown("View calculation methods and scoring from SANS assessment tool")
    
    try:
        calculations = get_calculations()
        
        if calculations:
            st.info(f"Found {len(calculations)} calculation records")
            
            # Show calculation structure
            calc_ids = list(calculations.keys())[:20]  # First 20
            selected_calc = st.selectbox("Select NDI ID", ["All"] + calc_ids, key="select_ndi_id_calc")
            
            if selected_calc != "All":
                calc_data = calculations[selected_calc]
                st.subheader(f"Calculation for {selected_calc}")
                
                # Display calculation data
                calc_df = pd.DataFrame([calc_data])
                st.dataframe(calc_df.T, use_container_width=True)
            else:
                st.subheader("Calculation Overview")
                st.write(f"Total calculation records: {len(calculations)}")
                
                # Show sample
                st.write("Sample calculations (first 5):")
                sample_calcs = {k: calculations[k] for k in list(calculations.keys())[:5]}
                st.json(sample_calcs)
        else:
            st.info("No calculation data available. Please import SANS file first.")
    except Exception as e:
        st.error(f"Error loading calculations: {str(e)}")

def show_maturity_assessment():
    st.header("📈 Maturity Assessment")
    st.markdown("View maturity questions and levels from SANS assessment tool")
    
    try:
        maturity_questions = get_maturity_questions()
        
        if maturity_questions:
            st.info(f"Found {len(maturity_questions)} maturity questions")
            
            # Group by domain
            domains = sorted(list(set([q.get('domain', 'Unknown') for q in maturity_questions])))
            selected_domain = st.selectbox("Select Domain", ["All"] + domains, key="select_domain_maturity")
            
            filtered_questions = maturity_questions
            if selected_domain != "All":
                filtered_questions = [q for q in maturity_questions if q.get('domain') == selected_domain]
            
            for question in filtered_questions:
                with st.expander(f"**{question.get('domain', 'Unknown')}**", expanded=False):
                    st.write("**Maturity Levels:**")
                    for level, description in question.get('levels', {}).items():
                        st.write(f"**{level}:** {description[:200]}...")
        else:
            st.info("No maturity questions available. Please import SANS file first.")
    except Exception as e:
        st.error(f"Error loading maturity questions: {str(e)}")

def show_documents_evidence():
    st.header("📄 Documents & Evidence")
    
    all_controls = get_all_controls()
    
    selected_control = st.selectbox(
        "Select Control",
        [f"{c['id']} - {c['title']}" for c in all_controls],
        key="select_control_documents"
    )
    
    control_id = selected_control.split(" - ")[0]
    control = next((c for c in all_controls if c['id'] == control_id), None)
    
    if control:
        st.subheader(f"Documents Required for {control_id}")
        
        # Try to get evidence from SANS system first
        evidence_found = False
        if control.get('specifications'):
            st.markdown("### Evidence by Specification")
            for spec in control.get('specifications', []):
                spec_id = spec.get('spec_id', '')
                evidence = get_evidence_by_spec(spec_id)
                if evidence:
                    evidence_found = True
                    with st.expander(f"**{spec_id}** - {spec.get('specification_text', '')[:50]}...", expanded=False):
                        for ev in evidence:
                            st.write(f"**Type:** {ev.get('type', 'Document')}")
                            st.write(f"**Description:** {ev.get('description', '')}")
                            if ev.get('acceptance_criteria'):
                                st.write(f"**Acceptance Criteria:** {ev.get('acceptance_criteria')}")
                            if ev.get('document_name'):
                                st.write(f"**Document Name:** {ev.get('document_name')}")
                            st.write(f"**Format:** {ev.get('format', 'PDF/DOCX')}")
                            st.write(f"**Required:** {'Yes' if ev.get('required') else 'No'}")
                            if ev.get('maturity_level'):
                                st.write(f"**Maturity Level:** {ev.get('maturity_level')}")
                            st.markdown("---")
        
        # Fallback to default documents
        if not evidence_found:
            documents = get_documents_by_control(control_id)
            
            if documents:
                doc_df = pd.DataFrame(documents)
                st.dataframe(doc_df, use_container_width=True)
                
                st.subheader("Evidence Requirements")
                evidence_reqs = get_evidence_requirements(control_id)
                
                for evidence in evidence_reqs:
                    with st.expander(f"**{evidence['type']}**", expanded=False):
                        st.write(f"**Description:** {evidence['description']}")
                        st.write(f"**Format:** {evidence['format']}")
                        st.write(f"**Required:** {evidence['required']}")
                        
                        # Evidence upload/status
                        evidence_key = f"evidence_{control_id}_{evidence['type']}"
                        if evidence_key not in st.session_state.evidence_data:
                            st.session_state.evidence_data[evidence_key] = {}
                        
                        uploaded_file = st.file_uploader(
                            f"Upload {evidence['type']}",
                            type=['pdf', 'doc', 'docx', 'xlsx', 'xls', 'txt'],
                            key=f"upload_{evidence_key}"
                        )
                        
                        if uploaded_file is not None:
                            st.session_state.evidence_data[evidence_key]['file_name'] = uploaded_file.name
                            st.session_state.evidence_data[evidence_key]['upload_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.success(f"File uploaded: {uploaded_file.name}")
                        
                        if evidence_key in st.session_state.evidence_data:
                            ev_data = st.session_state.evidence_data[evidence_key]
                            if 'file_name' in ev_data:
                                st.info(f"✅ Evidence uploaded: {ev_data['file_name']} on {ev_data.get('upload_date', 'N/A')}")
            else:
                st.info("No specific documents required for this control.")

def show_compliance_measurement():
    st.header("📊 Compliance Measurement")
    
    all_controls = get_all_controls()
    
    st.subheader("Measure Compliance by Control")
    
    selected_control = st.selectbox(
        "Select Control to Measure",
        [f"{c['id']} - {c['title']}" for c in all_controls],
        key="select_control_measure"
    )
    
    control_id = selected_control.split(" - ")[0]
    control = next((c for c in all_controls if c['id'] == control_id), None)
    
    if control:
        st.markdown(f"### {control['id']} - {control['title']}")
        
        # Initialize control data if not exists
        if control_id not in st.session_state.compliance_data:
            st.session_state.compliance_data[control_id] = {
                'status': 'Not Started',
                'score': 0,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # Status selection
        current_status = st.session_state.compliance_data[control_id].get('status', 'Not Started')
        status_options = ["Not Started", "In Progress", "Compliant", "Non-Compliant"]
        current_index = status_options.index(current_status) if current_status in status_options else 0
        new_status = st.selectbox(
            "Compliance Status",
            status_options,
            index=current_index,
            key=f"status_update_{selected_control}"
        )
        
        # Score input
        current_score = st.session_state.compliance_data[control_id].get('score', 0)
        new_score = st.slider(
            "Compliance Score (%)",
            min_value=0,
            max_value=100,
            value=current_score,
            key=f"measure_score_{control_id}"
        )
        
        # Notes
        notes_key = f"notes_{control_id}"
        if notes_key not in st.session_state.compliance_data[control_id]:
            st.session_state.compliance_data[control_id][notes_key] = ""
        
        notes = st.text_area(
            "Notes/Comments",
            value=st.session_state.compliance_data[control_id].get(notes_key, ""),
            key=f"measure_notes_{control_id}",
            height=150
        )
        
        # Save button
        if st.button("Save Measurement", key=f"save_{control_id}"):
            st.session_state.compliance_data[control_id]['status'] = new_status
            st.session_state.compliance_data[control_id]['score'] = new_score
            st.session_state.compliance_data[control_id][notes_key] = notes
            st.session_state.compliance_data[control_id]['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success("Compliance measurement saved successfully!")
        
        # Display current measurement
        st.markdown("---")
        st.subheader("Current Measurement")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", st.session_state.compliance_data[control_id].get('status', 'Not Started'))
        with col2:
            st.metric("Score", f"{st.session_state.compliance_data[control_id].get('score', 0)}%")
        with col3:
            st.metric("Last Updated", st.session_state.compliance_data[control_id].get('last_updated', 'N/A'))
        
        # Export data
        st.markdown("---")
        st.subheader("Export Data")
        if st.button("Export Compliance Data to JSON"):
            export_data = {
                'control_id': control_id,
                'measurement': st.session_state.compliance_data[control_id]
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"compliance_{control_id}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

def show_data_quality_dashboard():
    """Data Quality Dashboard - SANS Data Quality System"""
    st.header("🛡️ SANS Data Quality System")
    st.info("Professional NDMO Compliance Dashboard with Advanced Pipeline Processing")
    
    # Import data quality modules
    try:
        from ndmo_quality_standards import NDMOQualityStandards
        from smart_schema_analyzer import SmartSchemaAnalyzer
        from smart_data_processor import SmartDataProcessor
    except ImportError as e:
        st.error(f"Error importing data quality modules: {str(e)}")
        return
    
    # Initialize components
    if 'ndmo_standards' not in st.session_state:
        st.session_state.ndmo_standards = NDMOQualityStandards()
    if 'schema_analyzer' not in st.session_state:
        st.session_state.schema_analyzer = SmartSchemaAnalyzer()
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = SmartDataProcessor()
    
    # Main tabs for Data Quality
    dq_tab1, dq_tab2, dq_tab3, dq_tab4 = st.tabs([
        "📋 Schema Analysis",
        "⚙️ Data Processing",
        "🛡️ NDMO Compliance",
        "📊 Quality Reports"
    ])
    
    with dq_tab1:
        st.subheader("📋 Schema Analysis")
        st.markdown("Upload and analyze your schema file to check NDMO compliance")
        
        uploaded_schema = st.file_uploader(
            "Upload Schema File (Excel)",
            type=['xlsx', 'xls'],
            key="schema_upload"
        )
        
        if uploaded_schema:
            # Display file info
            file_size = len(uploaded_schema.getvalue())
            file_size_mb = file_size / (1024 * 1024)
            st.info(f"📄 File uploaded: **{uploaded_schema.name}** ({file_size_mb:.2f} MB)")
            
            # Validate file size
            if file_size > 200 * 1024 * 1024:  # 200MB limit
                st.error("❌ File size exceeds 200MB limit. Please upload a smaller file.")
            else:
                # Save uploaded file temporarily
                import tempfile
                import os
                tmp_path = None
                
                try:
                    # Determine file extension
                    file_ext = '.xlsx' if uploaded_schema.name.endswith('.xlsx') else '.xls'
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                        tmp_file.write(uploaded_schema.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Verify file was created
                    if not os.path.exists(tmp_path):
                        st.error("❌ Error: Failed to save uploaded file temporarily")
                    else:
                        st.success(f"✅ File saved successfully ({file_size_mb:.2f} MB)")
                
                except Exception as e:
                    st.error(f"❌ Error saving file: {str(e)}")
                    import traceback
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())
                    tmp_path = None
            
            if tmp_path and os.path.exists(tmp_path):
                if st.button("🔍 Analyze Schema", use_container_width=True):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.info("🔄 Analyzing schema structure...")
                        progress_bar.progress(20)
                        
                        # Verify file exists and is readable
                        if not os.path.exists(tmp_path):
                            raise FileNotFoundError(f"Temporary file not found: {tmp_path}")
                        
                        analysis = st.session_state.schema_analyzer.analyze_schema(tmp_path)
                        
                        if 'error' in analysis:
                            progress_bar.empty()
                            status_text.error(f"❌ {analysis['error']}")
                        else:
                            progress_bar.progress(100)
                            status_text.success("✅ Schema analysis completed!")
                            progress_bar.empty()
                            
                            # Store results
                            st.session_state.schema_analysis = analysis
                            
                            # Display results
                            st.markdown("### 📊 Analysis Summary")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                # Count actual columns from column_analysis (more accurate)
                                actual_cols = len(analysis.get('column_analysis', []))
                                total_cols_display = max(actual_cols, analysis.get('total_columns', 0))
                                st.metric("Total Columns", total_cols_display)
                                
                                # Show column names count
                                if analysis.get('columns'):
                                    st.caption(f"Column names: {len(analysis.get('columns', []))}")
                            with col2:
                                st.metric("Has Primary Key", "✅ Yes" if analysis.get('has_primary_key') else "❌ No")
                            with col3:
                                st.metric("Has Audit Trail", "✅ Yes" if analysis.get('has_audit_trail') else "❌ No")
                            with col4:
                                total_cols = len(analysis.get('column_analysis', []))
                                compliant_cols = sum(1 for col in analysis.get('ndmo_compliance', {}).values() if col.get('score', 0) >= 0.7)
                                st.metric("NDMO Compliant Columns", f"{compliant_cols}/{total_cols}")
                            
                            # Data Types Distribution
                            st.markdown("### 📈 Data Types Distribution")
                            if analysis.get('data_types'):
                                data_types_df = pd.DataFrame(list(analysis['data_types'].items()), columns=['Data Type', 'Count'])
                                st.bar_chart(data_types_df.set_index('Data Type'))
                            
                            # Detailed Column Analysis
                            st.markdown("### 🔍 Detailed Column Analysis")
                            st.markdown("Comprehensive analysis of each column according to NDMO standards")
                            
                            column_analysis = analysis.get('column_analysis', [])
                            ndmo_compliance = analysis.get('ndmo_compliance', {})
                            
                            # Always show column analysis section, even if empty
                            if not column_analysis:
                                st.info("ℹ️ No column analysis data available. The report will still be generated with available information.")
                            
                            if column_analysis:
                                # Show all column names first
                                st.markdown("#### 📋 All Column Names")
                                all_column_names = [col_info['column_name'] for col_info in column_analysis]
                                st.write(f"**Total:** {len(all_column_names)} columns")
                                st.write(", ".join(all_column_names[:50]))  # Show first 50
                                if len(all_column_names) > 50:
                                    st.write(f"... and {len(all_column_names) - 50} more columns")
                                
                                st.markdown("---")
                                
                                # Create DataFrame for better display
                                display_data = []
                                for col_info in column_analysis:
                                    col_name = col_info['column_name']
                                    compliance_info = ndmo_compliance.get(col_name, {})
                                    
                                    display_data.append({
                                        'Column Name': col_name,
                                        'Data Type': col_info.get('detected_type', 'Unknown'),
                                        'Completeness %': f"{col_info.get('completeness', 0):.1f}%",
                                        'Uniqueness %': f"{col_info.get('uniqueness', 0):.1f}%",
                                        'Non-Null': col_info.get('non_null_count', 0),
                                        'Null': col_info.get('null_count', 0),
                                        'Unique Values': col_info.get('unique_count', 0),
                                        'NDMO Score': f"{compliance_info.get('score', 0)*100:.1f}%",
                                        'Standards': ', '.join(compliance_info.get('standards', [])) or 'N/A',
                                        'Primary Key': "✅" if col_info.get('is_primary_key') else "❌",
                                        'Audit Field': "✅" if col_info.get('is_audit_field') else "❌"
                                    })
                                
                                df_display = pd.DataFrame(display_data)
                                st.dataframe(df_display, use_container_width=True, height=400)
                                
                                # Column-by-column detailed view
                                st.markdown("### 📋 Column Details")
                                
                                selected_column = st.selectbox(
                                    "Select Column for Detailed Analysis",
                                    [col['column_name'] for col in column_analysis],
                                    key="column_detail_select"
                                )
                                
                                if selected_column:
                                    col_info = next((c for c in column_analysis if c['column_name'] == selected_column), None)
                                    compliance_info = ndmo_compliance.get(selected_column, {})
                                    
                                    if col_info:
                                        st.markdown(f"#### Column: **{selected_column}**")
                                        
                                        col1, col2, col3, col4 = st.columns(4)
                                        with col1:
                                            st.metric("Data Type", col_info.get('detected_type', 'Unknown'))
                                        with col2:
                                            st.metric("Completeness", f"{col_info.get('completeness', 0):.1f}%")
                                        with col3:
                                            st.metric("Uniqueness", f"{col_info.get('uniqueness', 0):.1f}%")
                                        with col4:
                                            score = compliance_info.get('score', 0) * 100
                                            st.metric("NDMO Score", f"{score:.1f}%")
                                        
                                        st.markdown("---")
                                        
                                        # NDMO Standards Assessment
                                        st.markdown("#### 🛡️ NDMO Standards Assessment")
                                        standards_list = compliance_info.get('standards', [])
                                        
                                        if standards_list:
                                            for std_id in standards_list:
                                                st.success(f"✅ **{std_id}**: Applicable to this column")
                                        else:
                                            st.info("No specific NDMO standards identified for this column")
                                        
                                        # Column Statistics
                                        st.markdown("#### 📊 Column Statistics")
                                        stats_col1, stats_col2 = st.columns(2)
                                        with stats_col1:
                                            st.write(f"**Total Rows:** {col_info.get('total_count', 0)}")
                                            st.write(f"**Non-Null Values:** {col_info.get('non_null_count', 0)}")
                                            st.write(f"**Null Values:** {col_info.get('null_count', 0)}")
                                        with stats_col2:
                                            st.write(f"**Unique Values:** {col_info.get('unique_count', 0)}")
                                            st.write(f"**Primary Key:** {'Yes' if col_info.get('is_primary_key') else 'No'}")
                                            st.write(f"**Audit Field:** {'Yes' if col_info.get('is_audit_field') else 'No'}")
                                        
                                        # Recommendations for this column
                                        recommendations = []
                                        if col_info.get('completeness', 100) < 100:
                                            recommendations.append("⚠️ **DQ001**: Improve data completeness - some values are missing")
                                        if col_info.get('uniqueness', 100) < 100 and col_info.get('is_primary_key'):
                                            recommendations.append("⚠️ **DQ004**: Primary key should have 100% uniqueness")
                                        if not col_info.get('is_primary_key') and 'id' in selected_column.lower():
                                            recommendations.append("💡 **DG001**: Consider making this column a primary key")
                                        if not col_info.get('is_audit_field') and any(kw in selected_column.lower() for kw in ['date', 'time', 'created', 'updated']):
                                            recommendations.append("💡 **DS004**: This could be an audit trail field")
                                        
                                        if recommendations:
                                            st.markdown("#### 💡 Recommendations")
                                            for rec in recommendations:
                                                st.info(rec)
                            
                            # Issues
                            if analysis.get('issues'):
                                st.markdown("### ⚠️ Issues Found")
                                for issue in analysis['issues']:
                                    st.warning(f"**{issue.get('severity', 'Unknown')}**: {issue.get('issue', '')} - {issue.get('impact', '')}")
                            
                            # Recommendations
                            if analysis.get('recommendations'):
                                st.markdown("### 💡 General Recommendations")
                                for rec in analysis['recommendations']:
                                    st.info(f"**{rec.get('type', 'Info')}**: {rec.get('message', '')}")
                            
                            # Generate Professional Technical Report
                            st.markdown("---")
                            st.markdown("### 📄 Generate Technical Report")
                            st.markdown("Generate a comprehensive professional technical report with NDMO compliance analysis, SQL scripts, and implementation guide.")
                            
                            # Debug: Show analysis keys
                            if st.session_state.get('debug_mode', False):
                                with st.expander("🔍 Debug: Analysis Data"):
                                    st.write("Analysis keys:", list(analysis.keys()) if analysis else "No analysis data")
                                    st.write("Has column_analysis:", 'column_analysis' in analysis if analysis else False)
                                    st.write("Has ndmo_compliance:", 'ndmo_compliance' in analysis if analysis else False)
                            
                            # Two buttons: Technical Report and Assessment Report
                            col_btn1, col_btn2 = st.columns(2)
                            
                            with col_btn1:
                                if st.button("📄 Generate Technical Report", use_container_width=True, key="generate_dq_report"):
                                    try:
                                        # Show loading
                                        loading_placeholder = st.empty()
                                        loading_placeholder.info("🔄 Generating professional technical report...")
                                        
                                        # Import here to avoid issues
                                        try:
                                            from data_quality_report import create_data_quality_report
                                        except ImportError as import_error:
                                            st.error(f"❌ Error importing report generator: {str(import_error)}")
                                            raise
                                        
                                        # Get logo path
                                        logo_path = "logo@3x.png"
                                        if not os.path.exists(logo_path):
                                            logo_path = None
                                        
                                        # Ensure analysis has required fields
                                        if 'column_analysis' not in analysis:
                                            analysis['column_analysis'] = []
                                        if 'ndmo_compliance' not in analysis:
                                            analysis['ndmo_compliance'] = {}
                                        if 'total_columns' not in analysis:
                                            analysis['total_columns'] = len(analysis.get('columns', []))
                                        if 'total_fields' not in analysis:
                                            analysis['total_fields'] = len(analysis.get('fields', []))
                                        
                                        report_filename = create_data_quality_report(
                                            analysis,
                                            analysis.get('file_name', 'schema_file.xlsx'),
                                            logo_path=logo_path
                                        )
                                        
                                        # Store report filename in session state
                                        st.session_state.dq_report_filename = report_filename
                                        st.session_state.dq_report_generated = True
                                        
                                        loading_placeholder.empty()
                                        st.success("✅ Technical report generated successfully!")
                                        
                                        # Force rerun to show download button
                                        st.rerun()
                                    
                                    except Exception as e:
                                        st.error(f"❌ Error generating report: {str(e)}")
                                        import traceback
                                        with st.expander("Error Details"):
                                            st.code(traceback.format_exc())
                                
                                # Show download button if report was generated
                                if st.session_state.get('dq_report_generated', False) and st.session_state.get('dq_report_filename'):
                                    report_filename = st.session_state.dq_report_filename
                                    if os.path.exists(report_filename):
                                        try:
                                            with open(report_filename, 'rb') as f:
                                                report_data = f.read()
                                            st.download_button(
                                                "📥 Download Technical Report",
                                                report_data,
                                                file_name=os.path.basename(report_filename),
                                                mime="application/pdf",
                                                use_container_width=True,
                                                key="download_dq_report"
                                            )
                                        except Exception as e:
                                            st.error(f"❌ Error reading report file: {str(e)}")
                                    else:
                                        st.warning(f"⚠️ Report file not found: {report_filename}")
                            
                            with col_btn2:
                                if st.button("📊 Generate Assessment Report", use_container_width=True, key="generate_assessment_report"):
                                    try:
                                        with st.spinner("🔄 Generating professional assessment report..."):
                                            from data_quality_report import create_schema_assessment_report
                                            
                                            # Get logo path
                                            logo_path = "logo@3x.png"
                                            if not os.path.exists(logo_path):
                                                logo_path = None
                                            
                                            # Ensure analysis has required fields
                                            if 'column_analysis' not in analysis:
                                                analysis['column_analysis'] = []
                                            if 'ndmo_compliance' not in analysis:
                                                analysis['ndmo_compliance'] = {}
                                            if 'total_columns' not in analysis:
                                                analysis['total_columns'] = len(analysis.get('columns', []))
                                            
                                            assessment_filename = create_schema_assessment_report(
                                                analysis,
                                                analysis.get('file_name', 'schema_file.xlsx'),
                                                logo_path=logo_path
                                            )
                                            
                                            # Store report filename in session state
                                            st.session_state.dq_assessment_filename = assessment_filename
                                            st.session_state.dq_assessment_generated = True
                                            
                                            st.success("✅ Assessment report generated successfully!")
                                            st.rerun()
                                    
                                    except Exception as e:
                                        st.error(f"❌ Error generating assessment: {str(e)}")
                                        import traceback
                                        with st.expander("Error Details"):
                                            st.code(traceback.format_exc())
                                
                                # Show download button if assessment was generated
                                if st.session_state.get('dq_assessment_generated', False) and st.session_state.get('dq_assessment_filename'):
                                    assessment_filename = st.session_state.dq_assessment_filename
                                    if os.path.exists(assessment_filename):
                                        try:
                                            with open(assessment_filename, 'rb') as f:
                                                assessment_data = f.read()
                                            st.download_button(
                                                "📥 Download Assessment Report",
                                                assessment_data,
                                                file_name=os.path.basename(assessment_filename),
                                                mime="application/pdf",
                                                use_container_width=True,
                                                key="download_assessment_report"
                                            )
                                        except Exception as e:
                                            st.error(f"❌ Error reading assessment file: {str(e)}")
                                    else:
                                        st.warning(f"⚠️ Assessment file not found: {assessment_filename}")
                
                    except Exception as e:
                        progress_bar.empty()
                        error_msg = str(e)
                        status_text.error(f"❌ Error analyzing schema: {error_msg}")
                        import traceback
                        error_details = traceback.format_exc()
                        with st.expander("🔍 Error Details (Click to expand)"):
                            st.code(error_details)
                        
                        # Provide helpful suggestions
                        st.warning("💡 **Troubleshooting Tips:**")
                        st.markdown("""
                        - Make sure the file is a valid Excel file (.xlsx or .xls)
                        - Check that the file is not corrupted
                        - Ensure the file is not password protected
                        - Try opening the file in Excel first to verify it's valid
                        - If the file is very large, try reducing the number of rows/columns
                        """)
                    finally:
                        # Clean up temp file
                        if tmp_path and os.path.exists(tmp_path):
                            try:
                                os.unlink(tmp_path)
                            except Exception as cleanup_error:
                                # Log but don't show cleanup errors to user
                                pass
    
    with dq_tab2:
        st.subheader("⚙️ Data Processing")
        st.markdown("Process your data file according to schema requirements")
        
        # Show workflow status
        workflow_status = st.container()
        with workflow_status:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                schema_done = 'schema_analysis' in st.session_state
                st.markdown(f"**Schema Analysis:** {'✅ Done' if schema_done else '❌ Pending'}")
            with col2:
                data_done = 'data_processing_result' in st.session_state
                st.markdown(f"**Data Processing:** {'✅ Done' if data_done else '❌ Pending'}")
            with col3:
                compliance_done = 'compliance_results' in st.session_state
                st.markdown(f"**NDMO Compliance:** {'✅ Done' if compliance_done else '❌ Pending'}")
            with col4:
                reports_done = st.session_state.get('dq_report_generated', False) or st.session_state.get('dq_assessment_generated', False)
                st.markdown(f"**Reports:** {'✅ Generated' if reports_done else '❌ Pending'}")
        
        st.markdown("---")
        
        uploaded_data = st.file_uploader(
            "Upload Data File (Excel)",
            type=['xlsx', 'xls'],
            key="data_upload"
        )
        
        if uploaded_data:
            # Display file info
            file_size = len(uploaded_data.getvalue())
            file_size_mb = file_size / (1024 * 1024)
            st.info(f"📄 Data file uploaded: **{uploaded_data.name}** ({file_size_mb:.2f} MB)")
            
            if 'schema_analysis' not in st.session_state:
                st.warning("⚠️ Please analyze schema first in the 'Schema Analysis' tab")
                st.info("💡 **Steps to follow:**")
                st.markdown("""
                1. Go to **Schema Analysis** tab
                2. Upload your schema file (Excel)
                3. Click **Analyze Schema** button
                4. Come back here to process your data file
                """)
            else:
                st.success("✅ Schema analysis found! Ready to process data.")
                
                if st.button("⚙️ Process Data", use_container_width=True, key="process_data_btn"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.info("🔄 Saving uploaded file...")
                        progress_bar.progress(10)
                        
                        # Save uploaded file temporarily
                        import tempfile
                        import os
                        
                        # Determine file extension
                        file_ext = '.xlsx' if uploaded_data.name.endswith('.xlsx') else '.xls'
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                            tmp_file.write(uploaded_data.getvalue())
                            tmp_path = tmp_file.name
                        
                        status_text.info("🔄 Processing data file...")
                        progress_bar.progress(30)
                        
                        # Verify data_processor exists
                        if 'data_processor' not in st.session_state:
                            st.error("❌ Data processor not initialized. Please refresh the page.")
                            return
                        
                        # Process data
                        status_text.info("🔄 Analyzing data quality...")
                        progress_bar.progress(50)
                        
                        result = st.session_state.data_processor.process_data(
                            tmp_path,
                            st.session_state.schema_analysis
                        )
                        
                        progress_bar.progress(80)
                        
                        if result and result.get('success'):
                            # Store results
                            st.session_state.data_processing_result = result
                            
                            progress_bar.progress(100)
                            status_text.success("✅ Data processing completed!")
                            progress_bar.empty()
                            
                            st.balloons()  # Celebration animation
                            st.rerun()
                        else:
                            progress_bar.empty()
                            error_msg = result.get('error', 'Processing failed') if result else 'Processing failed - no result returned'
                            status_text.error(f"❌ {error_msg}")
                            
                            # Show detailed error if available
                            if result and result.get('processing_log'):
                                with st.expander("📋 Processing Log"):
                                    for log_entry in result.get('processing_log', []):
                                        st.write(f"**{log_entry.get('timestamp', '')}**: {log_entry.get('message', '')}")
                    
                    except Exception as e:
                        progress_bar.empty()
                        error_msg = str(e)
                        status_text.error(f"❌ Error processing data: {error_msg}")
                        import traceback
                        error_details = traceback.format_exc()
                        with st.expander("🔍 Error Details (Click to expand)"):
                            st.code(error_details)
                        
                        st.warning("💡 **Troubleshooting Tips:**")
                        st.markdown("""
                        - Make sure the data file matches the schema structure
                        - Check that column names in data file match schema columns
                        - Ensure the file is not corrupted
                        - Try opening the file in Excel first to verify it's valid
                        """)
                    finally:
                        # Clean up temp file
                        if 'tmp_path' in locals() and tmp_path and os.path.exists(tmp_path):
                            try:
                                os.unlink(tmp_path)
                            except:
                                pass
        
        # Show results if available
        if 'data_processing_result' in st.session_state:
            result = st.session_state.data_processing_result
            st.markdown("### 📊 Quality Metrics")
            metrics = result.get('quality_metrics', {})
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Completeness", f"{metrics.get('completeness', 0)*100:.1f}%")
            with col2:
                st.metric("Accuracy", f"{metrics.get('accuracy', 0)*100:.1f}%")
            with col3:
                st.metric("Consistency", f"{metrics.get('consistency', 0)*100:.1f}%")
            with col4:
                st.metric("Uniqueness", f"{metrics.get('uniqueness', 0)*100:.1f}%")
            with col5:
                st.metric("Overall Score", f"{metrics.get('overall_score', 0)*100:.1f}%")
            
            # Display processed data preview
            st.markdown("### 📋 Processed Data Preview")
            processed_df = result.get('processed_data')
            if processed_df is not None and isinstance(processed_df, pd.DataFrame) and not processed_df.empty:
                st.dataframe(processed_df.head(10), use_container_width=True)
                
                # Download processed data
                st.markdown("### 📥 Download Processed Data")
                try:
                    import io
                    output = io.BytesIO()
                    processed_df.to_excel(output, index=False, engine='openpyxl')
                    output.seek(0)
                    st.download_button(
                        "📥 Download Processed Data (Excel)",
                        output.getvalue(),
                        file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_processed_data"
                    )
                except Exception as e:
                    st.error(f"❌ Error preparing download: {str(e)}")
            elif processed_df is not None:
                st.warning("⚠️ Processed data is empty or invalid")
            else:
                st.info("ℹ️ No processed data available")
    
    with dq_tab3:
        st.subheader("🛡️ NDMO Compliance Assessment")
        st.markdown("Assess NDMO compliance based on schema analysis and data quality")
        
        # Show prerequisites
        schema_ready = 'schema_analysis' in st.session_state
        data_ready = 'data_processing_result' in st.session_state
        
        # Show workflow status
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Schema Analysis:** {'✅ Done' if schema_ready else '❌ Pending'}")
        with col2:
            st.markdown(f"**Data Processing:** {'✅ Done' if data_ready else '❌ Pending'}")
        
        st.markdown("---")
        
        if not schema_ready:
            st.warning("⚠️ Please complete Schema Analysis first")
            st.info("💡 Go to **Schema Analysis** tab and analyze your schema file")
        elif not data_ready:
            st.warning("⚠️ Please complete Data Processing first")
            st.info("💡 Go to **Data Processing** tab and process your data file")
        else:
            st.success("✅ All prerequisites completed! Ready to assess compliance.")
            
            if st.button("🛡️ Assess NDMO Compliance", use_container_width=True, key="assess_compliance_btn"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.info("🔄 Calculating compliance scores...")
                    progress_bar.progress(20)
                    
                    schema_analysis = st.session_state.schema_analysis
                    data_quality = st.session_state.data_processing_result.get('quality_metrics', {})
                    
                    progress_bar.progress(50)
                    status_text.info("🔄 Analyzing NDMO standards...")
                    
                    # Verify ndmo_standards exists
                    if 'ndmo_standards' not in st.session_state:
                        st.error("❌ NDMO standards not initialized. Please refresh the page.")
                        return
                    
                    compliance_results = st.session_state.ndmo_standards.calculate_compliance_score(
                        schema_analysis,
                        data_quality
                    )
                    
                    progress_bar.progress(80)
                    status_text.info("🔄 Finalizing results...")
                    
                    # Store results
                    st.session_state.compliance_results = compliance_results
                    
                    progress_bar.progress(100)
                    status_text.success("✅ Compliance assessment completed!")
                    progress_bar.empty()
                    
                    st.balloons()  # Celebration animation
                    st.rerun()
                
                except Exception as e:
                    progress_bar.empty()
                    error_msg = str(e)
                    status_text.error(f"❌ Error assessing compliance: {error_msg}")
                    import traceback
                    error_details = traceback.format_exc()
                    with st.expander("🔍 Error Details (Click to expand)"):
                        st.code(error_details)
                    
                    st.warning("💡 **Troubleshooting Tips:**")
                    st.markdown("""
                    - Make sure both schema analysis and data processing are completed
                    - Check that the data quality metrics are available
                    - Verify that NDMO standards are properly loaded
                    """)
        
        # Show results if available
        if 'compliance_results' in st.session_state:
            compliance_results = st.session_state.compliance_results
            
            # Display overall compliance
            st.markdown("### 📊 Overall Compliance")
            overall_score = compliance_results.get('overall_score', 0)
            status = compliance_results.get('status', 'Unknown')
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Compliance Score", f"{overall_score*100:.1f}%")
            with col2:
                status_color = {
                    'Compliant': '🟢',
                    'Partially Compliant': '🟡',
                    'Non-Compliant': '🔴'
                }
                st.metric("Status", f"{status_color.get(status, '⚪')} {status}")
            
            # Category scores
            st.markdown("### 📈 Compliance by Category")
            category_scores = compliance_results.get('category_scores', {})
            if category_scores:
                cat_df = pd.DataFrame(list(category_scores.items()), columns=['Category', 'Score'])
                cat_df['Score'] = cat_df['Score'] * 100
                st.bar_chart(cat_df.set_index('Category'))
            
            # Recommendations
            try:
                recommendations = st.session_state.ndmo_standards.get_recommendations(compliance_results)
                if recommendations:
                    st.markdown("### 💡 Recommendations")
                    for rec in recommendations[:10]:  # Show top 10
                        priority_icon = "🔴" if rec.get('priority') == 'High' else "🟡"
                        st.info(f"{priority_icon} **{rec.get('standard_name', '')}** ({rec.get('standard_id', '')}): {rec.get('recommendation', '')}")
            except:
                pass
    
    with dq_tab4:
        st.subheader("📊 Quality Reports")
        st.markdown("View comprehensive quality reports and export results")
        
        # Generate comprehensive reports
        st.markdown("### 📄 Generate Professional Reports")
        
        if 'schema_analysis' in st.session_state:
            analysis = st.session_state.schema_analysis
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("📄 Generate Technical Report", use_container_width=True, key="generate_tech_report_tab4"):
                    try:
                        with st.spinner("🔄 Generating professional technical report..."):
                            from data_quality_report import create_data_quality_report
                            
                            logo_path = "logo@3x.png"
                            if not os.path.exists(logo_path):
                                logo_path = None
                            
                            # Ensure analysis has required fields
                            if 'column_analysis' not in analysis:
                                analysis['column_analysis'] = []
                            if 'ndmo_compliance' not in analysis:
                                analysis['ndmo_compliance'] = {}
                            if 'total_columns' not in analysis:
                                analysis['total_columns'] = len(analysis.get('columns', []))
                            if 'total_fields' not in analysis:
                                analysis['total_fields'] = len(analysis.get('fields', []))
                            
                            report_filename = create_data_quality_report(
                                analysis,
                                analysis.get('file_name', 'schema_file.xlsx'),
                                logo_path=logo_path
                            )
                            
                            st.session_state.dq_report_filename = report_filename
                            st.session_state.dq_report_generated = True
                            
                            st.success("✅ Technical report generated successfully!")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        with st.expander("Error Details"):
                            st.code(traceback.format_exc())
            
            with col_btn2:
                if st.button("📊 Generate Assessment Report", use_container_width=True, key="generate_assess_report_tab4"):
                    try:
                        with st.spinner("🔄 Generating professional assessment report..."):
                            from data_quality_report import create_schema_assessment_report
                            
                            logo_path = "logo@3x.png"
                            if not os.path.exists(logo_path):
                                logo_path = None
                            
                            # Ensure analysis has required fields
                            if 'column_analysis' not in analysis:
                                analysis['column_analysis'] = []
                            if 'ndmo_compliance' not in analysis:
                                analysis['ndmo_compliance'] = {}
                            if 'total_columns' not in analysis:
                                analysis['total_columns'] = len(analysis.get('columns', []))
                            
                            assessment_filename = create_schema_assessment_report(
                                analysis,
                                analysis.get('file_name', 'schema_file.xlsx'),
                                logo_path=logo_path
                            )
                            
                            st.session_state.dq_assessment_filename = assessment_filename
                            st.session_state.dq_assessment_generated = True
                            
                            st.success("✅ Assessment report generated successfully!")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        with st.expander("Error Details"):
                            st.code(traceback.format_exc())
            
            # Show download buttons if reports were generated
            if st.session_state.get('dq_report_generated', False) and st.session_state.get('dq_report_filename'):
                report_filename = st.session_state.dq_report_filename
                if os.path.exists(report_filename):
                    try:
                        with open(report_filename, 'rb') as f:
                            report_data = f.read()
                        st.download_button(
                            "📥 Download Technical Report",
                            report_data,
                            file_name=os.path.basename(report_filename),
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_tech_report_tab4"
                        )
                    except Exception as e:
                        st.error(f"❌ Error reading report file: {str(e)}")
                else:
                    st.warning(f"⚠️ Report file not found: {report_filename}")
            
            if st.session_state.get('dq_assessment_generated', False) and st.session_state.get('dq_assessment_filename'):
                assessment_filename = st.session_state.dq_assessment_filename
                if os.path.exists(assessment_filename):
                    try:
                        with open(assessment_filename, 'rb') as f:
                            assessment_data = f.read()
                        st.download_button(
                            "📥 Download Assessment Report",
                            assessment_data,
                            file_name=os.path.basename(assessment_filename),
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_assess_report_tab4"
                        )
                    except Exception as e:
                        st.error(f"❌ Error reading assessment file: {str(e)}")
                else:
                    st.warning(f"⚠️ Assessment file not found: {assessment_filename}")
        
        st.markdown("---")
        
        # Export JSON reports
        if 'schema_analysis' in st.session_state:
            st.markdown("### 📋 Schema Analysis Report")
            with st.expander("View Schema Analysis Details"):
                st.json(st.session_state.schema_analysis)
            
            # Export schema analysis
            schema_json = json.dumps(st.session_state.schema_analysis, indent=2, default=str)
            st.download_button(
                "📥 Export Schema Analysis (JSON)",
                schema_json,
                file_name=f"schema_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="export_schema_json"
            )
        
        if 'data_processing_result' in st.session_state:
            st.markdown("### ⚙️ Data Processing Report")
            with st.expander("View Processing Results"):
                result = st.session_state.data_processing_result.copy()
                if 'processed_data' in result:
                    result['processed_data'] = "DataFrame (see preview above)"
                st.json(result)
            
            # Export processing results
            processing_json = json.dumps(result, indent=2, default=str)
            st.download_button(
                "📥 Export Processing Results (JSON)",
                processing_json,
                file_name=f"processing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="export_processing_json"
            )
        
        if 'compliance_results' in st.session_state:
            st.markdown("### 🛡️ NDMO Compliance Report")
            with st.expander("View Compliance Results"):
                st.json(st.session_state.compliance_results)
            
            # Export compliance report
            compliance_json = json.dumps(st.session_state.compliance_results, indent=2, default=str)
            st.download_button(
                "📥 Export Compliance Report (JSON)",
                compliance_json,
                file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="export_compliance_json"
            )

if __name__ == "__main__":
    main()

