import requests
import pickle
from pathlib import Path

from recommender.preprocessing import preprocess
from recommender.vectorizer import compute_tf, compute_idf, compute_tfidf

from config.settings import PHASE1_FACULTY_URL, INDEX_FILE

PHASE1_URL = "http://localhost:8000/faculty"

def fetch_data():

    from config.settings import PROJECT_ROOT
    csv_path = PROJECT_ROOT.parent / "DS614-Faculty-Finder" / "data" / "cleaned" / "transformed_faculty_data.csv"
    
    print(f"Reading from {csv_path}")
    import pandas as pd
    
    # Read CSV and treat specific columns as lists if generic parser fails, though preprocessing usually handles it.
    # We simply convert the dataframe to a list of dicts to match the previous API response format.
    df = pd.read_csv(csv_path)
    
    # Fill NaNs to avoid issues
    df = df.fillna("")
    
    return df.to_dict("records")

def safe(x):
    if x is None:
        return ""
    return str(x)

def build_docs(row):
    return (
        safe(row.get("name")) * 4 + " " +
        safe(row.get("research")) * 3 + " " +
        safe(row.get("specialization")) * 2 + " " +
        safe(row.get("publications")) * 2 + " " +
        safe(row.get("bio"))
    )


def build_index():

    data = fetch_data()

    docs = []
    meta = []

    for row in data:
        text = build_docs(row)
        tokens = preprocess(text)
        docs.append(tokens) #corpus
        meta.append(row)
        print(row.keys()) 

    idf = compute_idf(docs)

    vectors = []

    for tokens in docs:
        tf = compute_tf(tokens)
        vec = compute_tfidf(tf, idf)
        vectors.append(vec)
        

    with open(INDEX_FILE, "wb") as f:
        pickle.dump((vectors, meta, idf), f)


    print("Index built successfully")
