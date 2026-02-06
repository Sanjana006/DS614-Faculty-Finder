import pickle

from recommender.preprocessing import preprocess
from recommender.vectorizer import compute_tf, compute_tfidf
from recommender.similarity import cosine
from recommender.query_parser import parse_query
from config.settings import INDEX_FILE

with open(INDEX_FILE, "rb") as f:
    VECTORS, META, IDF = pickle.load(f)

def search(query: str):

    clean_q, k = parse_query(query)

    tokens = preprocess(clean_q)
    if not tokens:
        return []

    tf = compute_tf(tokens)
    q_vec = compute_tfidf(tf, IDF)

    results = []

    for vec, row in zip(VECTORS, META):
        score = cosine(q_vec, vec)

        results.append({
            "name": row.get("name"),
            "faculty_id": row.get("faculty_id"),
            "score": round(score, 4)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    top = results[:k]

    for r in top:
        print(r)

    return top

