from fastapi import FastAPI, Query
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.preprocessing.corpus_builder import build_weighted_corpus
from app.recommender.vectorizer import train_vectorizer
from app.recommender.recommend import recommend

app = FastAPI(title="Faculty Finder API")

with open("app/data/faculty.json", "r", encoding="utf-8") as f:
    faculty_data = json.load(f)["results"]

corpus = build_weighted_corpus(faculty_data)
vectorizer, tfidf_matrix = train_vectorizer(corpus)

@app.get("/recommend")
def recommend_faculty(
    query: str = Query(..., description="Research interest description"),
    top_k: int = 5
):
    return {
        "query": query,
        "top_k": top_k,
        "recommendations": recommend(
            query, vectorizer, tfidf_matrix, faculty_data, top_k
        )
    }
