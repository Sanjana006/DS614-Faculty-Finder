import math
import pickle
from config.settings import INDEX_FILE
from recommender.preprocessing import preprocess
from recommender.vectorizer import compute_tf, compute_tfidf

def cosine(v1, v2):
    common = set(v1) & set(v2)

    num = sum(v1[w]*v2[w] for w in common)

    d1 = math.sqrt(sum(x*x for x in v1.values()))
    d2 = math.sqrt(sum(x*x for x in v2.values()))

    if d1 == 0 or d2 == 0:
        return 0

    return num/(d1*d2)

def get_recommendations(query, top_k=5):

    # load index
    with open(INDEX_FILE, "rb") as f:
        vectors, meta, idf = pickle.load(f)

    # preprocess query
    tokens = preprocess(query)
    tf = compute_tf(tokens)
    q_vec = compute_tfidf(tf, idf)

    # compute similarities
    scores = []
    for vec, row in zip(vectors, meta):
        s = cosine(q_vec, vec)
        scores.append((s, row))

    # sort by score
    scores.sort(reverse=True, key=lambda x: x[0])

    # build UI-friendly output
    results = []
    for score, row in scores[:top_k]:
        name = row.get("name", "")
        
        # Generate faculty profile URL based on name
        profile_url = row.get("profile_url", "")
        
        # Fallback only if missing in data (e.g. legacy index)
        if not profile_url:
            faculty_slug = name.lower().replace(" ", "-").replace(".", "")
            profile_url = f"https://www.daiict.ac.in/faculty/{faculty_slug}"
        
        results.append({
            "name": name,
            "specialization": row.get("specialization", ""),
            "research": row.get("research", ""),
            "mail": row.get("mail", ""),
            "publications": row.get("publications", ""),
            "pub_links": row.get("pub_links", []),   # if available
            "profile_url": profile_url,
            "score": score
        })

    return results