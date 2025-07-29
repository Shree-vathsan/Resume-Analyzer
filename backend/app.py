# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import io

# Import your custom NLP modules (we'll create these next)
from resume_parser import parse_resume
from nlp_processor import get_resume_jd_match_score, extract_skills_from_text, get_missing_skills, get_strongest_matches

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/')
def health_check():
    return "Backend is running!"

@app.route('/analyze', methods=['POST'])
def analyze_resume_jd():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    if 'job_description' not in request.form:
        return jsonify({"error": "No job description provided"}), 400

    resume_file = request.files['resume']
    job_description_text = request.form['job_description']

    # Determine file type and parse resume
    resume_content = ""
    try:
        if resume_file.filename.endswith('.pdf'):
            resume_content = parse_resume(io.BytesIO(resume_file.read()), 'pdf')
        elif resume_file.filename.endswith('.docx'):
            resume_content = parse_resume(io.BytesIO(resume_file.read()), 'docx')
        else:
            return jsonify({"error": "Unsupported file type. Please upload PDF or DOCX."}), 400
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return jsonify({"error": f"Failed to parse resume: {str(e)}"}), 500

    if not resume_content:
        return jsonify({"error": "Could not extract text from resume."}), 500

    # --- NLP Processing ---
    try:
        # Overall Match Score
        overall_score = get_resume_jd_match_score(resume_content, job_description_text)

        # Extract skills from both for detailed analysis
        resume_skills = extract_skills_from_text(resume_content)
        jd_skills = extract_skills_from_text(job_description_text)

        # Missing Skills
        missing_skills = get_missing_skills(resume_skills, jd_skills)

        # Strongest Matches (simplified for now, can be improved)
        # This would involve more granular comparison, but for a start, just list common skills
        common_skills = list(set(resume_skills) & set(jd_skills))

        # Additional feedback (can be more sophisticated with Gemini API later)
        feedback = "Resume analyzed successfully! Review the match score, missing skills, and strong matches."
        if overall_score < 50:
            feedback = "The match score is low. Consider tailoring your resume more closely to the job description's requirements."
        elif missing_skills:
            feedback += " Focus on gaining or highlighting the missing skills."


        # backend/app.py

# ... (previous code) ...

        # --- NLP Processing ---
        try:
            # Overall Match Score
            overall_score = get_resume_jd_match_score(resume_content, job_description_text)

            # Extract skills from both for detailed analysis
            resume_skills = extract_skills_from_text(resume_content)
            jd_skills = extract_skills_from_text(job_description_text)

            # Missing Skills
            missing_skills = get_missing_skills(resume_skills, jd_skills)

            # Strongest Matches (simplified for now, can be improved)
            common_skills = list(set(resume_skills) & set(jd_skills))

            # Basic Feedback (can be overridden by Gemini)
            feedback = "Resume analyzed successfully! Review the match score, missing skills, and strong matches."
            if overall_score < 50:
                feedback = "The match score is low. Consider tailoring your resume more closely to the job description's requirements."
            elif missing_skills:
                feedback += " Focus on gaining or highlighting the missing skills."

            # --- Gemini API Integration ---
            gemini_feedback = None
            if os.getenv("GEMINI_API_KEY"): # Only call if API key is set
                from nlp_processor import get_gemini_feedback # Import here to avoid circular dependency
                gemini_feedback = get_gemini_feedback(resume_content, job_description_text, overall_score, missing_skills)
            # --- End Gemini API Integration ---

            return jsonify({
                "match_score": float(round(overall_score, 2)), # <--- FIX IS HERE: Convert to standard Python float
                "missing_skills": list(missing_skills),
                "strongest_matches": common_skills,
                "feedback": feedback,
                "gemini_feedback": gemini_feedback
            })

        except Exception as e:
            print(f"Error during NLP processing: {e}")
            return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500

# ... (rest of app.py) ...

    except Exception as e:
        print(f"Error during NLP processing: {e}")
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True) # debug=True for development, turn off in production
    
    