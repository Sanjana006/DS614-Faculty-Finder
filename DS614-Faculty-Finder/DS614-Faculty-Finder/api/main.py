'''
this is the main API file for Faculty Finder application.
it sets up the FastAPI app and includes the necessary routes.
'''
## DS614-Faculty-Finder/api/main.py
from fastapi import FastAPI

import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.routes import router 

app=FastAPI(title="Faculty Finder API",description="API to fetch faculty details",version="1.0.0")
app.include_router(router)

@app.get("/",summary="health check endpoint")
def health_check():
  return {"status":"ok","message":"Faculty Finder API is running"}