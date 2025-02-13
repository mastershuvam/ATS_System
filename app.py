from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS styling
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 2rem;
        }
        .stTextArea textarea {
            border-radius: 10px;
            padding: 1rem !important;
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
        .header {
            color: #2c3e50;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            font-weight: 700;
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
        .file-uploader {
            border: 2px dashed #4B6CB7;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }
        .highlight {
            color: #4B6CB7;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App Layout
st.markdown('<div class="header">📄 Smart ATS Resume Analyzer</div>', unsafe_allow_html=True)

with st.expander("ℹ️ How to use this tool"):
    st.markdown("""
    1. 📝 Paste the job description in the text area below
    2. 📤 Upload your resume in PDF format
    3. 🔍 Choose an analysis option from the buttons below
    4. 🚀 Get instant feedback to improve your resume!
    """)

col1, col2 = st.columns([3,2])
with col1:
    input_text = st.text_area("**Paste Job Description Here** ✍️", 
                            height=200,
                            help="Copy-paste the job description you want to analyze against")
with col2:
    st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("**Upload Resume (PDF)** 📄", type=["pdf"])
    st.markdown('</div>', unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns(3)
with button_col1:
    submit1 = st.button("🔍 Resume Evaluation", help="Get detailed analysis of your resume")
with button_col2:
    submit2 = st.button("💡 Improvement Tips", help="Get personalized improvement suggestions")
with button_col3:
    submit3 = st.button("📊 Match Percentage", help="Check ATS compatibility score")

# Response handling
def show_response(response_text):
    st.markdown(f'<div class="response-box">{response_text}</div>', 
              unsafe_allow_html=True)
input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a career coach and industry expert with years of experience in helping professionals enhance their skills. 
Your task is to analyze the provided resume and the job description. Based on this, suggest specific skills or certifications 
the candidate should acquire to improve their alignment with the desired role.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""



if submit1 or submit2 or submit3:
    if uploaded_file is not None:
        with st.spinner('🔎 Analyzing your resume...'):
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                
                if submit1:
                    response = get_gemini_response(input_prompt1, pdf_content, input_text)
                elif submit2:
                    response = get_gemini_response(input_prompt2, pdf_content, input_text)
                else:
                    response = get_gemini_response(input_prompt3, pdf_content, input_text)
                
                show_response(response)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please upload your resume PDF first!")