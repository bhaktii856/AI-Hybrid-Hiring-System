from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def candidate_text(candidate):
    profile = candidate.get("profile", {})

    text = ""

    text += profile.get("headline", "") + " "
    text += profile.get("summary", "") + " "

    for skill in candidate.get("skills", []):
        text += skill.get("name", "") + " "

    for job in candidate.get("career_history", []):
        text += job.get("title", "") + " "
        text += job.get("description", "") + " "

    return text


def embedding_score(jd_text, candidate):

    jd_embedding = model.encode([jd_text])

    candidate_embedding = model.encode(
        [candidate_text(candidate)]
    )

    score = cosine_similarity(
        jd_embedding,
        candidate_embedding
    )[0][0]

    return float(score)