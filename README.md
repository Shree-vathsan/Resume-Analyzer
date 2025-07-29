# ResumeMatch AI ✨

[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](https://github.com/your-username/resume-ai-agent/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Frontend](https://img.shields.io/badge/Frontend-React.js-61DAFB?style=for-the-badge&logo=react)](https://react.dev/)
[![Backend](https://img.shields.io/badge/Backend-Python_Flask-000000?style=for-the-badge&logo=python&logoColor=FFD43B)](https://flask.palletsprojects.com/)
[![NLP](https://img.shields.io/badge/NLP-Sentence--Transformers-DDDDDD?style=for-the-badge&logo=pytorch)](https://www.sbert.net/)
[![AI](https://img.shields.io/badge/AI-Google_Gemini_API-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/gemini-api)

---

## 🚀 Project Overview

**ResumeMatch AI** is an intelligent web application designed to help SDE job seekers optimize their resumes for specific roles. Users upload their resume (PDF/DOCX) and paste a job description.

The AI agent, built with a **Python (Flask) backend** for advanced Natural Language Processing (NLP) and a dynamic **React.js frontend**, performs a deep analysis. It provides a **match score**, highlights **missing key skills**, identifies **strongest matches**, and offers **actionable, AI-generated feedback** (via Gemini API). This tool empowers applicants to precisely tailor their resumes, significantly enhancing their chances by identifying crucial alignment and areas for improvement.

---

## 💡 Key Features

* 📄 **Resume & Job Description Upload:** Seamlessly upload PDF/DOCX resumes and input job descriptions.
* 📊 **Intelligent Match Scoring:** Get a precise percentage score indicating resume-JD alignment.
* 🔍 **Skill Gap Analysis:** Pinpoint specific skills missing from your resume that are crucial for the job.
* 🎯 **Strongest Match Highlighting:** Discover areas where your resume perfectly aligns with job requirements.
* ✨ **AI-Powered Feedback:** Receive personalized, actionable advice from Google's Gemini API to refine your resume.
* 🛠️ **Robust Text Processing:** Leverages `spaCy` for advanced text cleaning and lemmatization.

---

## 🎬 Demo / How It Works

See ResumeMatch AI in action!

*(**Important:** Replace `your-demo-video.gif` with the actual path to your GIF. You'll need to record a short demo of your app and convert it to a GIF. Tools like ScreenToGif or online converters can help.)*

![ResumeMatch AI Demo](https://via.placeholder.com/600x400/007bff/FFFFFF?text=YOUR_DEMO_GIF_HERE)

*(Alternatively, if you prefer a static screenshot for now:)*
![ResumeMatch AI Screenshot](https://via.placeholder.com0x400/007bff/FFFFFF?text=YOUR_SCREENSHOT_HERE)

---

## ⚙️ Tech Stack

* **Frontend:** [React.js](https://react.dev/)
* **Backend:** [Python](https://www.python.org/) / [Flask](https://flask.palletsprojects.com/)
* **NLP & ML:** [Sentence-Transformers](https://www.sbert.net/), [spaCy](https://spacy.io/), [scikit-learn](https://scikit-learn.org/)
* **AI/LLM:** [Google Gemini API](https://ai.google.dev/gemini-api)
* **File Parsing:** [PyPDF2](https://pypdf2.readthedocs.io/), [python-docx](https://python-docx.readthedocs.io/)
* **Environment Management:** [Python Virtual Environments (venv)](https://docs.python.org/3/library/venv.html)

---

## 🚀 Setup & Run Locally

Follow these steps to get ResumeMatch AI up and running on your local machine.

### Prerequisites

* Python 3.10+ (Recommended: 3.11.x)
* Node.js (LTS version) & npm
* Git

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/resume-ai-agent.git](https://github.com/your-username/resume-ai-agent.git)
cd resume-ai-agent
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # On Windows
# source venv/bin/activate # On macOS/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create a .env file in the 'backend' directory and add your Gemini API Key
# GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

python app.py
# The backend server should start on [http://127.0.0.1:5000](http://127.0.0.1:5000)
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
npm start
# The React app should open in your browser on http://localhost:3000
```

## 🌐 Deployment
This project is designed for deployment on various platforms.

Frontend Hosting: Netlify / Vercel (for static React build)

Backend Hosting: Render / Railway (for Python Flask API)

(You can add specific deployment instructions here later if you complete that step.)

## 📞 Connect with Me
GitHub: Shree-vathsan
LinkedIn: https://www.linkedin.com/in/shreevathsan/

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
