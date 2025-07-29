# backend/nlp_processor.py
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import os # <--- UNCOMMENT/ADD THIS IMPORT
import google.generativeai as genai # <--- UNCOMMENT/ADD THIS IMPORT
from google.generativeai.types import HarmCategory, HarmBlockThreshold # <--- UNCOMMENT/ADD THIS IMPORT

# Configure Gemini API with the key from environment variable
# This must be done BEFORE trying to use genai.GenerativeModel
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # <--- UNCOMMENT THIS LINE

# Load pre-trained spaCy model
# This needs to be done once at the start of your application
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
    exit()

# Load Sentence-BERT model
# 'all-MiniLM-L6-v2' is a good balance of size and performance
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example list of common SDE/AIML skills (expand this extensively!)
# You can get more comprehensive lists online or from job board APIs
COMMON_SKILLS = [
    "python", "java", "c++", "javascript", "react", "angular", "node.js", "flask", "django",
    "sql", "nosql", "postgresql", "mongodb", "mysql", "redis",
    "aws", "azure", "google cloud", "docker", "kubernetes", "git", "jenkins", "ci/cd",
    "data structures", "algorithms", "object-oriented programming", "system design",
    "restful apis", "microservices", "agile", "scrum", "devops",
    "machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn",
    "nlp", "computer vision", "data analysis", "big data", "spark", "hadoop",
    "cloud computing", "linux", "unix", "shell scripting", "bash", "testing",
    "troubleshooting", "problem-solving", "communication", "teamwork", "leadership",
    "api development", "web development", "mobile development", "backend development",
    "frontend development", "full stack development"
]

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers (keep letters and spaces)
    text = re.sub(r'[^a-z\s]', '', text)
    # Tokenize and remove stop words, lemmatize
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def extract_skills_from_text(text):
    processed_text = preprocess_text(text)
    found_skills = set()
    for skill in COMMON_SKILLS:
        # Simple check for now: if the exact skill (or its components) is in the processed text
        if skill in processed_text:
            found_skills.add(skill)
        # More advanced: use spaCy's PhraseMatcher or Rule-based Matcher for multi-word skills
        # Or train a custom NER model for skill extraction
    return list(found_skills)

def get_text_embedding(text):
    # Generate sentence embedding for the preprocessed text
    processed_text = preprocess_text(text)
    if not processed_text: # Handle empty string after preprocessing
        return np.zeros(model.get_sentence_embedding_dimension()) # Return zero vector
    embedding = model.encode(processed_text, convert_to_tensor=True)
    return embedding.cpu().numpy().reshape(1, -1) # Convert to numpy array and reshape for cosine_similarity

def get_resume_jd_match_score(resume_text, jd_text):
    resume_embedding = get_text_embedding(resume_text)
    jd_embedding = get_text_embedding(jd_text)

    if np.all(resume_embedding == 0) or np.all(jd_embedding == 0):
           return 0.0 # Return 0 if either text is empty or couldn't be processed

    # Calculate cosine similarity
    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    # Scale score to 0-100 percentage and ensure it's not negative
    # Cosine similarity is -1 to 1. We want 0-100.
    percentage_score = ((score + 1) / 2) * 100
    return max(0.0, min(100.0, percentage_score)) # Clamp between 0 and 100

def get_missing_skills(resume_skills, jd_skills):
    # Skills in JD that are NOT in resume
    missing = set(jd_skills) - set(resume_skills)
    return missing

def get_strongest_matches(resume_skills, jd_skills):
    # Skills present in BOTH resume and JD
    strong_matches = set(resume_skills) & set(jd_skills)
    return strong_matches

# --- Gemini API Integration ---
# You can use the Gemini API here for more advanced text understanding,
# like identifying nuances, suggesting resume phrasing, or even
# generating more detailed feedback.
# REMOVE THE COMMENTS BELOW FOR THE GEMINI API INTEGRATION TO BE ACTIVE

def get_gemini_feedback(resume_content, jd_text, overall_score, missing_skills):
    try:
        # Choose a Gemini model. 'gemini-pro' is good for text.
        # 'gemini-1.5-flash' is faster and cheaper if available for your API key.
        model_gemini = genai.GenerativeModel('gemini-pro')

        # Prepare the prompt for Gemini
        # Truncate content to fit within typical token limits (adjust as needed, 2000 chars is a rough estimate)
        prompt = f"""
        Analyze the following resume and job description.
        The applicant's current calculated match score is {overall_score:.2f}%.
        Identified missing key skills for this job are: {', '.join(missing_skills) if missing_skills else 'None'}.

        ---
        Resume (Applicant's Profile):
        {resume_content[:4000]}

        ---
        Job Description (Target Role):
        {jd_text[:4000]}

        ---

        Provide concise, professional, and actionable feedback for the applicant to improve their resume specifically for this job role. Focus on:
        1.  **Strengths:** Briefly mention what the resume aligns well with based on the job description.
        2.  **Areas for Improvement:** Specifically address the "missing skills" and suggest how the applicant might bridge those gaps (e.g., mention relevant projects, online courses, or self-study).
        3.  **Tailoring Suggestions:** Suggest how to rephrase or emphasize existing experiences or projects to better align with the job description's keywords and requirements.
        4.  **Overall Advice:** Any other actionable tips.

        Format your response as a series of bullet points. Be encouraging and constructive. Limit the total output to around 150-200 words.
        """

        # Generate content using Gemini
        response = model_gemini.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,  # Controls randomness. Lower for more focused.
                top_p=0.9,      # Top-p sampling
                top_k=20,       # Top-k sampling
            ),
            safety_settings=[ # Optional: Adjust safety settings if needed
                {
                    "category": HarmCategory.HARASSMENT,
                    "threshold": HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": HarmCategory.HATE_SPEECH,
                    "threshold": HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": HarmCategory.SEXUALLY_EXPLICIT,
                    "threshold": HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": HarmCategory.DANGEROUS_CONTENT,
                    "threshold": HarmBlockThreshold.BLOCK_NONE,
                },
            ]
        )

        # Access the generated text. Handle cases where no text is generated.
        return response.text if response.text else "Gemini could not generate detailed feedback."

    except genai.types.BlockedPromptException as e:
        print(f"Gemini API BlockedPromptException: {e}")
        return "Gemini feedback blocked due to safety concerns with the prompt."
    except Exception as e:
        print(f"Error calling Gemini API for feedback: {e}")
        return f"Could not generate advanced feedback from AI: {str(e)}"