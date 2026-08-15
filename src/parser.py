import re

def parse_jd(jd_text):

    jd = {
        "required_skills": [],
        "preferred_skills": [],
        "experience": 0,
        "keywords": []
    }

    skills = [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "llm",
        "rag",
        "retrieval",
        "vector database",
        "faiss",
        "pinecone",
        "sql",
        "aws",
        "docker",
        "kubernetes",
        "git",
        "linux",
        "fastapi",
        "flask",
        "langchain",
        "huggingface",
        "embedding",
        "transformers",
        "search",
        "ranking"
    ]

    text = jd_text.lower()

    for skill in skills:
        if skill in text:
            jd["required_skills"].append(skill)

    exp = re.findall(r"(\d+)\+?\s*years", text)

    if exp:
        jd["experience"] = int(exp[0])

    jd["keywords"] = jd["required_skills"]

    return jd