# ✉️ PitchPerfectAI – Smart Cover Letter Generator

PitchPerfectAI is a Streamlit-based web application that leverages Google's Gemini 1.5 Flash model to craft compelling, personalized cover letters tailored to job roles, experience, and tone preferences. It also evaluates ATS (Applicant Tracking System) compatibility for improved success rates in hiring pipelines.

## 🚀 Features

- 🎯 **Smart Prompting**: Generates professional cover letters using Gemini 1.5 Flash
- 📝 **Custom Input**: Add your experience, skills, achievements, and job description
- 📊 **ATS Match Analysis**: Get a score and tips to improve your match
- 📥 **Download as PDF**: Save your letter instantly
- 🌐 **Ready to Deploy**: Works locally or on Streamlit Cloud


## 📦 Tech Stack

- **Frontend & App UI**: [Streamlit](https://streamlit.io/)
- **LLM**: Google Gemini 1.5 Flash
- **Environment Variables**: `python-dotenv`
- **Language**: Python 3.11+

## 🧪 Installation & Usage

```bash
git clone https://github.com/your-username/pitchperfect-ai.git
cd pitchperfect-ai

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Add your API key to a .env file
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
