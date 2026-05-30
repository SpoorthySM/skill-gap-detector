from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
import PyPDF2
import io
from dotenv import load_dotenv
from google import genai

from analyzer import analyze_gap, extract_skills_from_text, parse_manual_skills, get_all_roles
from data.job_roles import JOB_ROLES
from ml_predictor import ml_analyze, predict_role

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Gemini client ─────────────────────────────────────────────────────────────
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ── helpers ───────────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    return " ".join(page.extract_text() or "" for page in reader.pages)


def ai_extract_skills(text):
    """Use Gemini to extract skills from resume text."""
    prompt = f"""Extract all technical and soft skills from this resume/text.
Return ONLY a JSON object with this exact format, no markdown, no explanation:
{{
  "skills": ["skill1", "skill2", ...],
  "experience_level": "fresher|junior|mid|senior",
  "summary": "one sentence about the candidate"
}}

Text:
{text[:3000]}"""

    response = gemini.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def ai_generate_recommendations(analysis_result):
    """Use Gemini to generate personalised recommendations."""
    missing_skills = [m["skill"] for m in analysis_result["missing"] if m["category"] == "technical"][:6]
    matched_skills = [m["skill"] for m in analysis_result["matched"] if m["category"] == "technical"][:6]

    prompt = f"""A student is preparing for placement as a {analysis_result['job_role']}.
Their readiness score is {analysis_result['readiness_score']}% ({analysis_result['label']}).
Skills they have: {', '.join(matched_skills)}
Skills they're missing: {', '.join(missing_skills)}

Give 3 specific, actionable, encouraging recommendations to help them get placement-ready.
Return ONLY a JSON array, no markdown, no explanation:
[
  {{"title": "short title", "detail": "2-sentence actionable advice", "timeframe": "X weeks"}},
  ...
]"""

    response = gemini.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ── routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/roles", methods=["GET"])
def get_roles():
    return jsonify({"roles": get_all_roles()})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        skills_text = data.get("skills", "")
        job_role = data.get("job_role", "")
        input_mode = data.get("input_mode", "manual")

        if not skills_text or not job_role:
            return jsonify({"error": "Skills and job role are required"}), 400

        if input_mode == "manual":
            skills = parse_manual_skills(skills_text)
            skills += extract_skills_from_text(skills_text)
            skills = list(set(skills))
        else:
            skills = json.loads(skills_text) if skills_text.startswith("[") else parse_manual_skills(skills_text)

        result = ml_analyze(skills, job_role)
        if not result:
            return jsonify({"error": "Invalid job role"}), 400

        try:
            ai_recs = ai_generate_recommendations(result)
            result["ai_recommendations"] = ai_recs
        except Exception:
            result["ai_recommendations"] = []

        result["student_skills"] = skills
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file.read())
        elif filename.endswith(".txt"):
            text = file.read().decode("utf-8", errors="ignore")
        else:
            return jsonify({"error": "Only PDF and TXT files supported"}), 400

        if not text.strip():
            return jsonify({"error": "Could not extract text from file"}), 400

        try:
            ai_result = ai_extract_skills(text)
            skills = ai_result.get("skills", [])
            experience_level = ai_result.get("experience_level", "fresher")
            summary = ai_result.get("summary", "")
        except Exception:
            skills = extract_skills_from_text(text)
            experience_level = "fresher"
            summary = "Skills extracted from resume."

        return jsonify({
            "skills": skills,
            "experience_level": experience_level,
            "summary": summary,
            "raw_text_preview": text[:300]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/compare-roles", methods=["POST"])
def compare_roles():
    try:
        data = request.get_json()
        skills = data.get("skills", [])
        roles = data.get("roles", get_all_roles()[:5])

        results = []
        for role in roles:
            r = analyze_gap(skills, role)
            if r:
                results.append({
                    "role": role,
                    "score": r["readiness_score"],
                    "label": r["label"],
                    "label_color": r["label_color"],
                    "matched_count": r["stats"]["total_matched"],
                    "missing_count": r["stats"]["total_missing"],
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return jsonify({"comparisons": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)