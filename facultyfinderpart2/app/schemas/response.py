from pydantic import BaseModel
from typing import List

class FacultyRecommendation(BaseModel):
    faculty_id: str
    name: str
    email: str
    score: float
    specialization: str

class RecommendationResponse(BaseModel):
    query: str
    top_k: int
    recommendations: List[FacultyRecommendation]
