from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class RedditPost(Base):
    __tablename__ = "reddit_posts"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    post_text = Column(Text)
    sentiment = Column(String)
    emotion = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

