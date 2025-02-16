import streamlit as st
import stripe
import os
import base64
import io
from pymongo import MongoClient
from dotenv import load_dotenv
from PIL import Image
import pdf2image
import google.generativeai as genai
from datetime import datetime
from login import create_user, verify_user

load_dotenv()

# MongoDB Configuration
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.ats_database
analyses_collection = db.analyses

# Stripe Configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS
st.markdown("""
    <style>
    :root {
        --primary: #2E86AB;
        --secondary: #3AA6B9;
        --accent: #FF6B6B;
    }
    
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        min-height: 100vh;
        padding: 2rem;
    }
    
    .header {
        font-size: 2.5em;
        padding: 20px 0;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .custom-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
        color: black;
    }
    
    .price-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
        transition: all 0.3s cubic-bezier(.25,.8,.25,1);
        color: black;
        height: 400px;
    }
    
    .price-card:hover {
        box-shadow: 0 14px 28px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.08);
        border-color: var(--secondary);
    }
    
    .stButton button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        border: none !important;
        background: linear-gradient(135deg, var(--secondary), var(--primary)) !important;
        width: 100%;
    }
    
    .response-box {
        animation: fadeIn 0.5s ease-out;
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-left: 4px solid var(--secondary);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: black;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .auth-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        align-items: center;
        padding: 4rem 0;
    }
    
    .credit-counter {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        color:black;
    }
    </style>
""", unsafe_allow_html=True)


# Update the auth_page function with these changes
# Authentication Page
def auth_page():
    st.markdown("""
    <div class="auth-container">
        <div>
            <h1 class="header">🔐 Smart ATS Analyzer</h1>
            <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
                AI-powered resume optimization for modern job seekers
            </p>
        </div>
        <div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📲 Login", "📝 Register"])
    
    with tab1:
        with st.form("Login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🚀 Login")
            
            if submit:
                user = verify_user(email, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['user'] = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    with tab2:
        with st.form("Register"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("✨ Create Account")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    try:
                        create_user(new_email, new_password)
                        st.success("Account created! Please login")
                    except ValueError as e:
                        st.error(str(e))

    st.markdown("</div></div>", unsafe_allow_html=True)

# Payment Page
def payment_page():
    st.markdown('<div class="header">💳 Premium Services</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container():
            st.markdown("""
            <div class="price-card">
                <h3>🚀 Basic</h3>
                <h2>$49</h2>
                <hr style="margin: 1rem 0;">
                <ul style="padding-left: 1.2rem;">
                    <li>Resume Evaluation</li>
                    <li>Basic ATS Check</li>
                    <li>3 Revisions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Choose Basic", key="basic"):
                initiate_payment(4900)

    with col2:
        with st.container():
            st.markdown("""
            <div class="price-card">
                <h3>💎 Pro</h3>
                <h2>$99</h2>
                <hr style="margin: 1rem 0;">
                <ul style="padding-left: 1.2rem;">
                    <li>Advanced Analysis</li>
                    <li>ATS Optimization</li>
                    <li>Unlimited Revisions</li>
                    <li>Priority Support</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Choose Pro", key="pro"):
                initiate_payment(9900)

    with col3:
        with st.container():
            st.markdown("""
            <div class="price-card">
                <h3>🎯 Custom</h3>
                <h2>Contact</h2>
                <hr style="margin: 1rem 0;">
                <p>Tailored solutions for:</p>
                <ul style="padding-left: 1.2rem;">
                    <li>Enterprise</li>
                    <li>Recruitment Agencies</li>
                    <li>Custom Integration</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Contact Us", key="custom"):
                st.info("✉️ shuvamghosh375@gmail.com")

def initiate_payment(amount):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Service Plan'},
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=os.getenv("SUCCESS_URL"),
            cancel_url=os.getenv("CANCEL_URL"),
        )
        st.markdown(f"[![Pay Now](https://img.icons8.com/color/48/000000/stripe.png)]({session.url})", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Payment failed: {str(e)}")

def show_remaining_credits_sidebar(analysis_count):
    remaining_credits = 5 - analysis_count
    
    with st.sidebar:
        st.markdown(f'<div class="credit-counter">✨ Remaining Credits: {remaining_credits}/5</div>', unsafe_allow_html=True)
        if remaining_credits <= 0:
            st.error("Please upgrade to continue")

# Main Application
def main_app():
    st.markdown('<div class="header">📄 ATS Resume Analyzer</div>', unsafe_allow_html=True)

    user = st.session_state.get('user')
    analysis_count = analyses_collection.count_documents({"user_id": user['_id']})
    show_remaining_credits_sidebar(analysis_count)

    if analysis_count >= 5:
        st.warning("Please upgrade your plan to continue using the service")
        return

    with st.container():
        st.markdown("""
        <div class="custom-card">
            <h3 style="margin-top: 0;">🔍 Start Your Analysis</h3>
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
                <div>
                    <p style="font-weight: 500; margin-bottom: 0.5rem;">📝 Paste Job Description</p>
        """, unsafe_allow_html=True)
        
        input_text = st.text_area("", height=200, label_visibility="collapsed")

        st.markdown("""
                </div>
                <div>
                    <p style="font-weight: 500; margin-bottom: 0.5rem;">📤 Upload Resume</p>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

        st.markdown("</div></div></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        analysis_type = st.selectbox("Select Analysis Type", [
            "Resume Evaluation", 
            "Improvement Tips", 
            "Match Percentage"
        ])

    if st.button("🚀 Run Analysis", use_container_width=True):
        if uploaded_file and input_text:
            try:
                with st.spinner("🔍 Analyzing your resume..."):
                    pdf_content = input_pdf_setup(uploaded_file)
                    if analysis_type == "Resume Evaluation":
                        prompt = f"""
                        You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
                        Please share your professional evaluation on whether the candidate's profile aligns with the role. 
                        Highlight the strengths and weaknesses of the applicant in relation to the specified 
                        """
                        response = get_gemini_response(prompt, pdf_content, input_text)
                        show_response(response)
                        log_analysis(input_text, analysis_type, response)
                        st.session_state.last_analysis = response
                    elif analysis_type == "Resume Evaluation":
                        prompt = f"""
                        You are a career coach and industry expert with years of experience in helping professionals enhance their skills. 
                        Your task is to analyze the provided resume and the job description. Based on this, suggest specific skills or certifications 
                        the candidate should acquire to improve their alignment with the desired role.
                        """
                        response = get_gemini_response(prompt, pdf_content, input_text)
                        show_response(response)
                        log_analysis(input_text, analysis_type, response)
                        st.session_state.last_analysis = response
                    else:
                        analysis_type = "Improvement Tips"
                        prompt = f"""
                        You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
                        your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
                        the job description. First the output should come as percentage and then keywords mis
                        """
                        response = get_gemini_response(prompt, pdf_content, input_text)
                        show_response(response)
                        log_analysis(input_text, analysis_type, response)
                        st.session_state.last_analysis = response

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
        else:
            st.warning("Please provide both resume and job description")



# Helper Functions
def input_pdf_setup(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]

def get_gemini_response(prompt, pdf_content, job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, pdf_content[0], job_description])
    return response.text

def log_analysis(input_text, analysis_type, response):
    user = st.session_state.get('user')
    if not user:
        st.error("Authentication error. Please log in again.")
        return
    analysis_data = {
        "user_id": user['_id'],
        "job_description": input_text,
        "analysis_type": analysis_type,
        "result": response,
        "created_at": datetime.utcnow()
    }
    analyses_collection.insert_one(analysis_data)

def show_response(response_text):
    st.markdown(f'<div class="response-box">{response_text}</div>', unsafe_allow_html=True)

# App Flow
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/resume.png", width=100)
    menu = st.radio("Navigation", ["Home", "Premium", "Account"])
    
    if st.session_state.get('authenticated'):
        if st.button("🚪 Logout"):
            st.session_state['authenticated'] = False
            st.rerun()

if st.session_state['authenticated']:
    if menu == "Home":
        main_app()
    elif menu == "Premium":
        payment_page()
    elif menu == "Account":
        st.write("Account Settings")
else:
    auth_page()

