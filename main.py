import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from models import RedditPost
from routes.analysis import router as analysis_router

app = FastAPI(
    title="Reddit Social Sentiment & Trend Analysis API",
    version="1.0.0"
)

# 🚨 VERY IMPORTANT — ALLOW VERCEL DOMAIN
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://reddit-frontend-coral.vercel.app",
    "*"   # TEMPORARY — allows all origins (for testing)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(analysis_router)

@app.get("/")
async def root():
    return {"message": "API Running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
