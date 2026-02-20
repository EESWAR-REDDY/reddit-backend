from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from collections import Counter

from database import get_db
from models import RedditPost
from schemas import (
    TopicAnalysisRequest,
    TopicAnalysisResponse,
    RedditPostResponse,
    TrendResponse,
    TrendDataPoint
)
from reddit_service import fetch_reddit_posts
from preprocessing import preprocess_text
from sentiment_service import analyze_sentiment
from emotion_service import detect_emotion

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.post("/topic", response_model=TopicAnalysisResponse)
async def analyze_topic(request: TopicAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze a topic by fetching Reddit posts, performing sentiment and emotion analysis,
    and storing results in the database.
    """
    try:
        # Fetch Reddit posts
        reddit_posts = fetch_reddit_posts(request.topic, request.limit)
        
        if not reddit_posts:
            raise HTTPException(status_code=404, detail="No Reddit posts found for the given topic")
        
        saved_posts = []
        sentiments = []
        emotions = []
        
        # Process each post
        for post_data in reddit_posts:
            # Combine title and text for analysis
            full_text = f"{post_data['title']} {post_data.get('text', '')}"
            
            # Preprocess text
            processed_text = preprocess_text(full_text)
            
            # Analyze sentiment
            sentiment = analyze_sentiment(full_text)
            
            # Detect emotion
            emotion = detect_emotion(full_text)
            
            # Store in database
            db_post = RedditPost(
                topic=request.topic,
                post_text=full_text[:5000],  # Limit text length
                sentiment=sentiment,
                emotion=emotion
            )
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            
            saved_posts.append(RedditPostResponse.model_validate(db_post))
            sentiments.append(sentiment)
            emotions.append(emotion)
        
        # Calculate distributions
        sentiment_distribution = dict(Counter(sentiments))
        emotion_distribution = dict(Counter(emotions))
        
        return TopicAnalysisResponse(
            topic=request.topic,
            total_posts=len(saved_posts),
            posts=saved_posts,
            sentiment_distribution=sentiment_distribution,
            emotion_distribution=emotion_distribution
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing topic: {str(e)}")

@router.get("/results", response_model=List[RedditPostResponse])
async def get_results(topic: str = None, limit: int = 50, db: Session = Depends(get_db)):
    """
    Fetch stored analysis results. Optionally filter by topic.
    """
    try:
        query = db.query(RedditPost)
        
        if topic:
            query = query.filter(RedditPost.topic.ilike(f"%{topic}%"))
        
        posts = query.order_by(RedditPost.created_at.desc()).limit(limit).all()
        
        return [RedditPostResponse.model_validate(post) for post in posts]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching results: {str(e)}")

@router.get("/trends", response_model=TrendResponse)
async def get_trends(topic: str, days: int = 7, db: Session = Depends(get_db)):
    """
    Get historical trend data for a topic over the specified number of days.
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query posts for the topic in the date range
        posts = db.query(RedditPost).filter(
            RedditPost.topic.ilike(f"%{topic}%"),
            RedditPost.created_at >= start_date,
            RedditPost.created_at <= end_date
        ).all()
        
        # Group by date and sentiment
        trend_dict = {}
        
        for post in posts:
            date_str = post.created_at.date().isoformat()
            
            if date_str not in trend_dict:
                trend_dict[date_str] = {"positive": 0, "negative": 0, "neutral": 0}
            
            sentiment_lower = post.sentiment.lower()
            if sentiment_lower == "positive":
                trend_dict[date_str]["positive"] += 1
            elif sentiment_lower == "negative":
                trend_dict[date_str]["negative"] += 1
            else:
                trend_dict[date_str]["neutral"] += 1
        
        # Convert to list of TrendDataPoint
        trend_data = [
            TrendDataPoint(
                date=date,
                positive=data["positive"],
                negative=data["negative"],
                neutral=data["neutral"]
            )
            for date, data in sorted(trend_dict.items())
        ]
        
        return TrendResponse(topic=topic, trend_data=trend_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trends: {str(e)}")

