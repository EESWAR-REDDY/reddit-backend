from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class RedditPostCreate(BaseModel):
    topic: str
    post_text: str
    sentiment: str
    emotion: str

class RedditPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    post_text: str
    sentiment: str
    emotion: str
    created_at: datetime

class TopicAnalysisRequest(BaseModel):
    topic: str
    limit: Optional[int] = 10

class TopicAnalysisResponse(BaseModel):
    topic: str
    total_posts: int
    posts: List[RedditPostResponse]
    sentiment_distribution: dict
    emotion_distribution: dict

class TrendDataPoint(BaseModel):
    date: str
    positive: int
    negative: int
    neutral: int

class TrendResponse(BaseModel):
    topic: str
    trend_data: List[TrendDataPoint]

