import streamlit as st
from dotenv import load_dotenv
from login import create_user, verify_user
from pymongo import MongoClient
import os
import base64
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from datetime import datetime

load_dotenv()

# MongoDB Configuration
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.ats_database
analyses_collection = db.analyses

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS   
# Add this CSS at the top of app.py (before any other code)
st.markdown("""
    <style>
            
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }

    
    .header {
        font-size: 2.5em;
        color: var(--primary);
        padding: 20px 0;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        background: linear-gradient(45deg, #2E86AB, #3AA6B9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stButton button {
        background: linear-gradient(45deg, #4B6CB7 0%, #182848 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .response-box {
        background: #fff; /* White background */
        color: #000; /* Black text */
        border: 1px solid #000; /* Black border for contrast */
        border-radius: 15px; /* Rounded corners */
        padding: 2rem; /* Spacing inside the box */
        margin-top: 1.5rem; /* Spacing above the box */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        font-family: 'Arial', sans-serif; /* Clean font style */
        transition: transform 0.2s ease-in-out; /* Smooth interaction animation */
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    [data-testid="stExpander"] {
        background: var(--secondary) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .stFileUploader {
        border: 2px dashed var(--primary) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    .success {
        color: #28a745 !important;
        font-weight: 500 !important;
    }
    
    .error {
        color: #dc3545 !important;
        font-weight: 500 !important;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Update the auth_page function with these changes
def auth_page():
    st.markdown('<div class="header">🔒 ATS Resume Analyzer</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📲 Login", "📝 Register"])
    
    with tab1:
        with st.form("Login"):
            st.subheader("Welcome Back!")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="••••••••")
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
            st.subheader("Create New Account")
            new_email = st.text_input("Email", placeholder="Enter your email")
            new_password = st.text_input("Password", type="password", placeholder="••••••••")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
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

# Update the main_app function with these changes
def main_app():
    st.markdown('<div class="header">📄 Smart ATS Resume Analyzer</div>', unsafe_allow_html=True)
    
    # Add logout button
    col1, col2 = st.columns([4,1])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state['authenticated'] = False
            st.rerun()
    
    with st.expander("📌 How to use this tool", expanded=True):
        st.markdown("""
        1. 📝 Paste the job description in the text area<br>
        2. 📤 Upload your resume in PDF format<br>
        3. 🔍 Choose an analysis option from the buttons below<br>
        """, unsafe_allow_html=True)
    
  

    col1, col2 = st.columns([3, 2])
    with col1:
        input_text = st.text_area("**Paste Job Description Here** ✍️", height=200)
    with col2:
        uploaded_file = st.file_uploader("**Upload Resume (PDF)** 📄", type=["pdf"])

    button_col1, button_col2, button_col3 = st.columns(3)  # Added a 4th column for the new button
    with button_col1:
        submit1 = st.button("🔍 Resume Evaluation")
        with button_col2:
            submit2 = st.button("💡 Improvement Tips")
        with button_col3:
            submit3 = st.button("📊 Match Percentage")
        #with button_col4:
            #submit4 = st.button("🏢 Recommended Companies")

    if submit1 or submit2 or submit3 :
        if uploaded_file is not None:
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                
                if submit1:
                    prompt = """
                    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
                    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
                    Highlight the strengths and weaknesses of the applicant in relation to the specified 
                    """
                elif submit2:
                    prompt = """
                    You are a career coach and industry expert with years of experience in helping professionals enhance their skills. 
                    Your task is to analyze the provided resume and the job description. Based on this, suggest specific skills or certifications 
                    the candidate should acquire to improve their alignment with the desired role.
                    """
                else :
                    prompt = """
                    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
                    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
                    the job description. First the output should come as percentage and then keywords mis
                    """

                #else:
                    #prompt = """
                    #You are a professional recruiter with years of experience in the industry. Your task is to evaluate the resume against the job description. 
                    #Based on this, suggest companies that the candidate should consider applying to, given their skills and experience.
                    #"""

                response = get_gemini_response(prompt, pdf_content, input_text)
                show_response(response)
                log_analysis(input_text, "evaluation" if submit1 else "improvement" if submit2 else "match", response)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please upload your resume PDF first!")

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

if st.session_state['authenticated']:
    main_app()
else:
    auth_page()
