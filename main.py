import json
import csv
from docx import Document

from src.scorer import score_candidate
from src.reasoning import generate_reason

DATASET_PATH = "data/candidates.jsonl"
JD_PATH = "data/job_description.docx"


def load_candidates(path):
    candidates = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))

    return candidates


if __name__ == "__main__":

    print("Loading candidates...")
    candidates = load_candidates(DATASET_PATH)
    print(f"Loaded {len(candidates)} candidates.")

    print("Loading Job Description...")

    doc = Document(JD_PATH)

    jd_text = "\n".join(
    para.text for para in doc.paragraphs
)
    print("Scoring candidates...\n")

    ranked_candidates = []

    for candidate in candidates:

        score = score_candidate(candidate, jd_text)

        ranked_candidates.append(
            (score, candidate)
        )

    ranked_candidates.sort(
        key=lambda x: x[0],
        reverse=True
    )

    print("Top 10 Candidates\n")

    for score, candidate in ranked_candidates[:10]:
        print(
            candidate["candidate_id"],
            score,
            candidate["profile"]["current_title"]
        )

    print("\nSaving submission...\n")
    print("\nTop 20 Candidates\n")

    for rank, (score, candidate) in enumerate(ranked_candidates[:20], start=1):
        print(
            rank,
            candidate["candidate_id"],
            score,
            candidate["profile"]["current_title"]
        )

    print("\nRank 50\n")

    score, candidate = ranked_candidates[49]

    print(
        candidate["candidate_id"],
        score,
        candidate["profile"]["current_title"]
    )

    print("\nRank 100\n")

    score, candidate = ranked_candidates[99]

    print(
        candidate["candidate_id"],
        score,
        candidate["profile"]["current_title"]
    )

    with open(
        "output/submission.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "candidate_id",
                "rank",
                "score",
                "reasoning"
            ]
        )

        max_score = ranked_candidates[0][0]

        for rank, (score, candidate) in enumerate(
            ranked_candidates[:100],
            start=1
        ):

            normalized_score = round(
                score / max_score,
                4
            )

            reasoning = generate_reason(
                candidate,
                score
            )
            print("\nReasoning Output:")
            print(reasoning)

            writer.writerow(
                [
                    candidate["candidate_id"],
                    rank,
                    normalized_score,
                    reasoning
                ]
            )

    print("Submission saved successfully!")