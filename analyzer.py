import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.job_roles import JOB_ROLES, SKILL_CATEGORIES, LEARNING_RESOURCES

def normalize(text):
    return text.lower().strip()

def extract_skills_from_text(text):
    """Extract skills from free-form text (resume or manual input)."""
    text_lower = text.lower()
    found_skills = set()

    all_known_skills = set()
    for role_data in JOB_ROLES.values():
        all_known_skills.update([s.lower() for s in role_data["technical"]])
        all_known_skills.update([s.lower() for s in role_data["soft"]])
        all_known_skills.update([s.lower() for s in role_data["tools"]])
    for skills in SKILL_CATEGORIES.values():
        all_known_skills.update(skills)

    # Also add common aliases
    aliases = {
        "oop": "object oriented programming", "oops": "object oriented programming",
        "dsa": "data structures", "ml": "machine learning", "dl": "deep learning",
        "ds": "data structures", "ai": "machine learning", "js": "javascript",
        "ts": "typescript", "cpp": "c++", "nlp": "nlp",
        "cv": "computer vision", "vis": "data visualization"
    }

    for alias, full in aliases.items():
        if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
            found_skills.add(full)

    for skill in all_known_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return sorted(found_skills)


def parse_manual_skills(skills_text):
    """Parse comma/newline separated manual skill input."""
    separators = r'[,\n;|]'
    raw = re.split(separators, skills_text)
    skills = [s.strip().lower() for s in raw if s.strip()]
    return skills


def analyze_gap(student_skills_raw, job_role):
    """Core gap analysis: returns matched, missing, partial, score."""
    student_skills = set(normalize(s) for s in student_skills_raw)

    if job_role not in JOB_ROLES:
        return None

    role = JOB_ROLES[job_role]
    required_technical = [normalize(s) for s in role["technical"]]
    required_soft = [normalize(s) for s in role["soft"]]
    required_tools = [normalize(s) for s in role["tools"]]

    all_required = set(required_technical + required_soft + required_tools)

    matched = []
    missing = []
    partial = []

    for skill in required_technical:
        if skill in student_skills:
            matched.append({"skill": skill, "category": "technical"})
        else:
            # Check partial match
            is_partial = any(
                (skill in s or s in skill) and skill != s
                for s in student_skills
            )
            if is_partial:
                partial.append({"skill": skill, "category": "technical"})
            else:
                missing.append({"skill": skill, "category": "technical"})

    for skill in required_soft:
        if skill in student_skills:
            matched.append({"skill": skill, "category": "soft"})
        else:
            missing.append({"skill": skill, "category": "soft"})

    for skill in required_tools:
        if skill in student_skills:
            matched.append({"skill": skill, "category": "tools"})
        else:
            is_partial = any(
                (skill in s or s in skill) and skill != s
                for s in student_skills
            )
            if is_partial:
                partial.append({"skill": skill, "category": "tools"})
            else:
                missing.append({"skill": skill, "category": "tools"})

    # Scoring: matched = 1pt, partial = 0.5pt
    total = len(all_required)
    score_raw = len(matched) + (len(partial) * 0.5)
    readiness_score = round((score_raw / total) * 100, 1) if total > 0 else 0

    # Technical-only score (more important for placements)
    tech_total = len(required_technical)
    tech_matched = sum(1 for m in matched if m["category"] == "technical")
    tech_partial = sum(1 for p in partial if p["category"] == "technical")
    tech_score = round(((tech_matched + tech_partial * 0.5) / tech_total) * 100, 1) if tech_total > 0 else 0

    # Get priority missing (technical first)
    priority_missing = [m for m in missing if m["category"] == "technical"]

    # Add recommendations
    recommendations = []
    for item in priority_missing[:8]:  # top 8
        skill = item["skill"]
        # Find matching resource (case-insensitive)
        resource = next(
            (v for k, v in LEARNING_RESOURCES.items() if k.lower() == skill),
            {"platform": "Google / YouTube", "link": f"https://www.google.com/search?q=learn+{skill.replace(' ', '+')}", "time": "2-4 weeks"}
        )
        recommendations.append({
            "skill": skill,
            "platform": resource["platform"],
            "link": resource["link"],
            "estimated_time": resource["time"],
            "priority": "High" if item["category"] == "technical" else "Medium"
        })

    # Readiness label
    if readiness_score >= 80:
        label = "Job Ready"
        label_color = "green"
    elif readiness_score >= 60:
        label = "Almost There"
        label_color = "yellow"
    elif readiness_score >= 40:
        label = "Needs Work"
        label_color = "orange"
    else:
        label = "Early Stage"
        label_color = "red"

    # Categorize student's extra skills (not in job req but still valuable)
    bonus_skills = [s for s in student_skills if s not in all_required and len(s) > 2]

    return {
        "job_role": job_role,
        "readiness_score": readiness_score,
        "tech_score": tech_score,
        "label": label,
        "label_color": label_color,
        "matched": matched,
        "missing": missing,
        "partial": partial,
        "recommendations": recommendations,
        "bonus_skills": bonus_skills[:10],
        "stats": {
            "total_required": total,
            "total_matched": len(matched),
            "total_partial": len(partial),
            "total_missing": len(missing),
            "tech_matched": tech_matched,
            "tech_total": tech_total,
        }
    }


def get_all_roles():
    return list(JOB_ROLES.keys())