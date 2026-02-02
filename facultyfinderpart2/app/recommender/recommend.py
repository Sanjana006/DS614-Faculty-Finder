import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommend(query, vectorizer, tfidf_matrix, faculty_data, top_k=5):
    query_vec = vectorizer.transform([query.lower()])
    scores = cosine_similarity(query_vec, tfidf_matrix)[0]

    ranked_idx = np.argsort(scores)[::-1][:top_k]

    results = []
    for i in ranked_idx:
        f = faculty_data[i]
        results.append({
            "faculty_id": f["faculty_id"],
            "name": f["name"],
            "email": f["mail"],
            "score": round(float(scores[i]), 4),
            "specialization": f["specialization"]
        })

    return results
