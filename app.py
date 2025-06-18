import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fpdf import FPDF
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

st.set_page_config(
    page_title="PitchPerfectAI – Smart Cover Letter Generator",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS styling
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 38px;
            font-weight: 700;
            color: #4B8BBE;
            margin-bottom: 10px;
        }
        input, textarea {
            background-color: #f9f9f9 !important;
            color: #000 !important;
            border: 0.5px solid #ccc !important;
            border-radius: 6px !important;
        }
        input::placeholder, textarea::placeholder {
            background-color: #f9f9f9 !important;
            color: #000 !important;
        }
        .stButton>button {
            background-color: #4B8BBE;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 24px;
            font-size: 16px;
        }
        .footer {
            text-align: center;
            font-size: 13px;
            color: #666;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>✉️ PitchPerfectAI – AI Cover Letter Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# Form for user input
with st.form("cover_letter_form"):
    job_title = st.text_input("Job Title", placeholder="e.g. Software Engineer")
    company = st.text_input("Company Name", placeholder="e.g. Google")
    experience = st.text_input("Years of Experience", placeholder="e.g. 3")
    key_skills = st.text_area("Key Skills", placeholder="e.g. Python, Data Analysis, APIs")
    achievements = st.text_area("Achievements (optional)", placeholder="e.g. Increased user retention by 20%")
    tone = st.selectbox("Tone of the Letter", ["Professional", "Persuasive", "Formal", "Friendly"])
    job_description = st.text_area("Paste the Job Description", placeholder="Copy the full job posting here...")
    submitted = st.form_submit_button("Generate Cover Letter")

import unicodedata
def generate_pdf(text):
    # Normalize and remove unsupported characters
    cleaned_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in cleaned_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest='S').encode('latin-1')

def download_pdf_button(text):
    pdf_data = generate_pdf(text)
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="cover_letter.pdf">📥 Download as PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# Submission handling
if submitted:
    with st.spinner("✍️ Crafting your personalized cover letter..."):
        prompt = f"""
        Write a compelling cover letter for the following job application:

        Position: {job_title}
        Company: {company}
        Experience: {experience} years
        Key Skills: {key_skills}
        Achievements: {achievements if achievements else "Not specified"}
        Tone: {tone}

        Requirements:
        1. Professional business letter format
        2. Strong opening paragraph
        3. Highlight experience and skills
        4. Mention why the applicant wants to work at {company}
        5. Include quantifiable achievements
        6. Use action verbs and avoid clichés
        7. Be ATS-friendly and concise (300–400 words)

        Format:
        [Date]
        [Hiring Manager's Name or Hiring Team]
        {company}

        Dear Hiring Manager,

        [Cover letter content]

        Sincerely,
        [Your Name]
        """

        response = model.generate_content(prompt)
        cover_letter = response.text

        st.success("✅ Cover letter generated successfully!")
        st.text_area("📄 Generated Cover Letter", value=cover_letter, height=400)

        # PDF Download
        download_pdf_button(cover_letter)

        # ATS Match Scoring
        if job_description:
            with st.spinner("🔍 Analyzing ATS match..."):
                ats_prompt = f"""
                Evaluate the following cover letter against this job description.

                Provide:
                1. An ATS match score out of 100
                2. A short explanation for the score
                3. Three suggestions to improve the cover letter

                --- COVER LETTER ---
                {cover_letter}

                --- JOB DESCRIPTION ---
                {job_description}
                """

                ats_response = model.generate_content(ats_prompt)
                st.markdown("---")
                st.subheader("📊 ATS Match Analysis")
                st.markdown(ats_response.text)

st.markdown("<div class='footer'>Made with ❤️ • Powered by Gemini 1.5 Flash</div>", unsafe_allow_html=True)
