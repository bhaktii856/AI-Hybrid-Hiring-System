from src.embeddings import embedding_score  

AI_SKILLS = {
    "python": 5,
    "machine learning": 6,
    "deep learning": 6,
    "tensorflow": 5,
    "pytorch": 5,
    "llm": 7,
    "transformer": 6,
    "langchain": 7,
    "huggingface": 6,
    "rag": 8,
    "retrieval": 8,
    "vector": 6,
    "faiss": 7,
    "pinecone": 7,
    "chroma": 7,
    "embedding": 6,

    # New AI skills
    "nlp": 7,
    "fine-tuning llms": 9,
    "lora": 8,
    "milvus": 8,
    "bentoml": 7,
    "gans": 6,
    "speech recognition": 7,
    "image classification": 7,
    "weights & biases": 6,
    "computer vision": 7,
    "mlops": 7,

    # Supporting infra
    "spark": 3,
    "pyspark": 3,
    "airflow": 3,
    "kafka": 3,

    "sql": 3,
    "docker": 3,
    "kubernetes": 3,
    "aws": 3,
    "git": 2
}

BAD_TITLES = [
    "marketing",
    "sales",
    "content writer",
    "graphic designer",
    "accountant",
    "hr manager",
    "customer support",
    "business analyst",
    "project manager"
]

AI_JOB_KEYWORDS = [
    "machine learning",
    "ml engineer",
    "ai engineer",
    "data scientist",
    "applied scientist",
    "nlp",
    "computer vision",
    "llm",
    "deep learning",
    "artificial intelligence",
    "research engineer"
]
NON_AI_TITLES = [
    "graphic designer",
    "qa engineer",
    "customer support",
    "sales",
    "marketing",
    "hr manager",
    "operations manager",
    "mechanical engineer",
    "civil engineer",
    "project manager"
]
AI_JOB_TITLES = [
    "machine learning",
    "ml engineer",
    "ai engineer",
    "data scientist",
    "applied scientist",
    "recommendation",
    "search engineer",
    "nlp engineer",
    "computer vision"
]
def score_candidate(candidate, jd_text):

    score = 0

    profile = candidate["profile"]
    skills = candidate["skills"]
    history = candidate["career_history"]
    signals = candidate["redrob_signals"]

    # -------------------------
    # 1 Skills
    # -------------------------

    for skill in skills:

        name = skill["name"].lower()

        if name in AI_SKILLS:

            score += AI_SKILLS[name]

            if skill["proficiency"] == "expert":
                score += 4

            elif skill["proficiency"] == "advanced":
                score += 3

            elif skill["proficiency"] == "intermediate":
                score += 2

            score += min(skill.get("duration_months", 0) / 24, 5)

            score += min(skill.get("endorsements", 0) / 25, 5)

    # -------------------------
    # 2 Experience
    # -------------------------

    years = profile["years_of_experience"]

    score += min(years * 2, 20)

    # -------------------------
    # 3 Career
    # -------------------------

    for job in history:

        text = (
            job["title"] +
            " " +
            job["description"]
        ).lower()

        for word in AI_SKILLS:

            if word in text:
                score += 2

 # keywords
    ai_exp_score = 0

    for job in history:

        text = (
            job["title"] + " " +
            job["description"]
        ).lower()

        for keyword in AI_JOB_KEYWORDS:

            if keyword in text:
                ai_exp_score += 5

    score += min(ai_exp_score, 25)

    if ai_exp_score == 0:
        score -= 20
    for job in history:

        title = job["title"].lower()

        for non_ai in NON_AI_TITLES:

            if non_ai in title:
                score -= 10
    # -------------------------
    # AI Job Titles Bonus
   # -------------------------

    for job in history:

        title = job["title"].lower()

        for ai_title in AI_JOB_TITLES:

            if ai_title in title:
                score += 10



    # 4 Behaviour
    # -------------------------

    score += signals["profile_completeness_score"] / 20

    score += signals["github_activity_score"] / 10

    score += signals["recruiter_response_rate"] * 8

    score += signals["interview_completion_rate"] * 8

    score += signals["saved_by_recruiters_30d"] / 3

    score += signals["search_appearance_30d"] / 25

    score += signals["connection_count"] / 200

    if signals["verified_email"]:
        score += 2

    if signals["verified_phone"]:
        score += 2

    if signals["linkedin_connected"]:
        score += 2

    if signals["open_to_work_flag"]:
        score += 2

    # -------------------------
    # 5 Penalties
    # -------------------------

    title = profile["current_title"].lower()

    for bad in BAD_TITLES:

        if bad in title:
            score -= 40

    # -------------------------
    # 6 Semantic Score
    # -------------------------

    
    semantic = embedding_score(
        jd_text,
        candidate
    )


    score += semantic * 35

    return round(score, 3)