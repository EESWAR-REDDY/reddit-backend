from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from models import RedditPost  # noqa: F401 - register model with Base
from routes.analysis import router as analysis_router

app = FastAPI(
    title="Reddit Social Sentiment & Trend Analysis API",
    description="API for Reddit-based sentiment monitoring and trend analysis using ML",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
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
    return {"message": "Reddit Sentiment Analysis API", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}
