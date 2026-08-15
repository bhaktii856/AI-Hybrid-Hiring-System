def generate_reason(candidate, score):

    profile = candidate["profile"]
    skills = candidate["skills"]

    title = profile["current_title"]
    exp = profile["years_of_experience"]

    top_skills = sorted(
        skills,
        key=lambda x: x.get("endorsements", 0),
        reverse=True
    )[:3]

    skill_names = [s["name"] for s in top_skills]

    reason = (
        f"{title} with {exp} years of experience. "
        f"Strong expertise in {', '.join(skill_names)}. "
    )

    if "AI" in title or "ML" in title:
        reason += "Relevant AI/ML professional background. "

    elif "Data" in title:
        reason += "Strong data-driven and analytical experience. "

    elif "Engineer" in title:
        reason += "Solid engineering and technical expertise. "

    reason += "Profile shows strong alignment with AI hiring requirements."

    return reason