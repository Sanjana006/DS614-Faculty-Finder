import math
from collections import Counter

def compute_tf(tokens):
    c = Counter(tokens)
    total = len(tokens)
    return {w: c[w]/total for w in c}

def compute_idf(all_tokens):
    N = len(all_tokens)
    df = {}

    for tokens in all_tokens:
        for w in set(tokens):
            df[w] = df.get(w, 0) + 1

    return {w: math.log((N+1)/(df[w]+1)) + 1 for w in df}

def compute_tfidf(tf, idf):
    return {w: tf[w]*idf.get(w, 0) for w in tf}
