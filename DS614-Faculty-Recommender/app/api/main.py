from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

from app.engine import search

app = FastAPI(title="Faculty Recommender")


@app.get("/recommend")
def recommend(q: str):
    results = search(q)
    return JSONResponse(
        content=json.loads(json.dumps(results, indent=2))
    )
