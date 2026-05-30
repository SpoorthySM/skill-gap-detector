import pickle
import numpy as np
from analyzer import analyze_gap
from data.job_roles import JOB_ROLES

# Load the trained model and vectorizer
with open('skill_gap_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

# Map ML model categories to job_roles.py keys
ROLE_MAPPING = {
    'Data Scientist': 'Data Scientist',
    'Data Analyst': 'Data Analyst',
    'Data Engineer': 'Data Scientist',
    'ML Engineer': 'Machine Learning Engineer',
    'DevOps Engineer': 'DevOps Engineer',
    'Frontend Developer': 'Frontend Developer',
    'Backend Developer': 'Backend Developer',
    'Full Stack Developer': 'Software Development Engineer',
    'Java Developer': 'Software Development Engineer',
    'Python Developer': 'Software Development Engineer',
    'Software Engineer': 'Software Development Engineer',
}

def predict_role(skills_list):
    """Given a list of skills, predict the best matching job role."""
    skills_text = ' '.join(skills_list)
    vec = tfidf.transform([skills_text])
    
    # Get prediction + probabilities for all roles
    prediction = model.predict(vec)[0]
    probabilities = model.predict_proba(vec)[0]
    classes = model.classes_
    
    # Top 3 matching roles with confidence
    top_indices = np.argsort(probabilities)[::-1][:3]
    top_roles = [
        {
            "role": classes[i],
            "confidence": round(probabilities[i] * 100, 1)
        }
        for i in top_indices
    ]
    
    return {
        "predicted_role": prediction,
        "confidence": round(probabilities.max() * 100, 1),
        "top_matches": top_roles
    }

def ml_analyze(skills_list, job_role=None):
    """Full ML-powered analysis."""
    # If no role given, predict it
    if not job_role:
        prediction = predict_role(skills_list)
        predicted_role = prediction['predicted_role']
        confidence = prediction['confidence']
        top_matches = prediction['top_matches']
    else:
        predicted_role = job_role
        confidence = None
        top_matches = []

    # Map to our job roles database
    mapped_role = ROLE_MAPPING.get(predicted_role, 'Software Development Engineer')

    # Run gap analysis
    gap_result = analyze_gap(skills_list, mapped_role)
    if not gap_result:
        return None

    # Add ML-specific fields
    gap_result['ml_predicted_role'] = predicted_role
    gap_result['ml_confidence'] = confidence
    gap_result['ml_top_matches'] = top_matches

    return gap_result