import praw
import os
from dotenv import load_dotenv
from typing import List
import random
from datetime import datetime, timedelta

load_dotenv()

def get_mock_posts(topic: str, limit: int = 10) -> List[dict]:
    """
    Generate mock Reddit-like posts for demonstration when Reddit API is not available.
    These posts are designed to showcase different sentiments and emotions.
    """
    mock_posts = [
        {
            'title': f'Why {topic} is changing everything for the better',
            'text': f'I\'ve been following {topic} closely and I\'m genuinely excited about the positive impact it\'s having. The community response has been amazing and I think we\'re seeing real progress.',
            'score': 1250,
            'subreddit': 'technology',
            'created_utc': (datetime.now() - timedelta(hours=2)).timestamp()
        },
        {
            'title': f'Frustrated with how {topic} is being handled',
            'text': f'This is absolutely ridiculous. The way {topic} is being managed shows complete lack of understanding. I\'m really disappointed and angry about this situation.',
            'score': 890,
            'subreddit': 'discussion',
            'created_utc': (datetime.now() - timedelta(hours=5)).timestamp()
        },
        {
            'title': f'Just learned about {topic} - what should I know?',
            'text': f'Hey everyone, I\'m new to {topic} and looking for some neutral information. Can someone explain the basics? I want to understand both sides before forming an opinion.',
            'score': 450,
            'subreddit': 'askreddit',
            'created_utc': (datetime.now() - timedelta(hours=8)).timestamp()
        },
        {
            'title': f'{topic} exceeded all my expectations!',
            'text': f'I was skeptical at first, but {topic} has completely blown me away. The results speak for themselves and I couldn\'t be happier. This is exactly what we needed!',
            'score': 2100,
            'subreddit': 'technology',
            'created_utc': (datetime.now() - timedelta(hours=1)).timestamp()
        },
        {
            'title': f'Concerned about the future of {topic}',
            'text': f'I\'m worried about where {topic} is heading. There are some serious issues that need to be addressed, and I fear we might be heading in the wrong direction.',
            'score': 670,
            'subreddit': 'discussion',
            'created_utc': (datetime.now() - timedelta(hours=12)).timestamp()
        },
        {
            'title': f'{topic} - A balanced perspective',
            'text': f'Let\'s have a thoughtful discussion about {topic}. There are pros and cons, and I think we need to consider multiple viewpoints. What are your thoughts?',
            'score': 320,
            'subreddit': 'discussion',
            'created_utc': (datetime.now() - timedelta(hours=15)).timestamp()
        },
        {
            'title': f'This {topic} update is incredible!',
            'text': f'I\'m so thrilled about the latest developments in {topic}! Everything is working perfectly and the community is thriving. This is amazing news!',
            'score': 1800,
            'subreddit': 'technology',
            'created_utc': (datetime.now() - timedelta(hours=3)).timestamp()
        },
        {
            'title': f'Why {topic} is a complete disaster',
            'text': f'I can\'t believe how poorly {topic} has been implemented. This is a mess and I\'m furious about the wasted resources. Someone needs to be held accountable.',
            'score': 950,
            'subreddit': 'discussion',
            'created_utc': (datetime.now() - timedelta(hours=6)).timestamp()
        },
        {
            'title': f'Quick question about {topic}',
            'text': f'Can someone explain {topic} in simple terms? I\'m trying to understand what it means and how it affects things. Looking for factual information.',
            'score': 280,
            'subreddit': 'askreddit',
            'created_utc': (datetime.now() - timedelta(hours=20)).timestamp()
        },
        {
            'title': f'{topic} brings hope for the future',
            'text': f'After years of uncertainty, {topic} finally gives me hope. The positive changes are visible and I believe we\'re on the right track. This is wonderful!',
            'score': 1400,
            'subreddit': 'technology',
            'created_utc': (datetime.now() - timedelta(hours=4)).timestamp()
        },
        {
            'title': f'I\'m scared about what {topic} means',
            'text': f'The implications of {topic} are really frightening. I don\'t know what to expect and I\'m genuinely concerned about the consequences. This is worrying.',
            'score': 520,
            'subreddit': 'discussion',
            'created_utc': (datetime.now() - timedelta(hours=10)).timestamp()
        },
        {
            'title': f'{topic} - What a pleasant surprise!',
            'text': f'I wasn\'t expecting much from {topic}, but wow! This is really impressive and I\'m pleasantly surprised by how well it turned out. Great job!',
            'score': 1100,
            'subreddit': 'technology',
            'created_utc': (datetime.now() - timedelta(hours=7)).timestamp()
        },
        {
            'title': f'Neutral analysis of {topic}',
            'text': f'Let me break down {topic} objectively. Here are the facts: it has certain characteristics, some people support it, others don\'t. Let\'s discuss the data.',
            'score': 380,
            'subreddit': 'discussion',
            'created_utc': (datetime.now() - timedelta(hours=18)).timestamp()
        },
        {
            'title': f'{topic} makes me so happy!',
            'text': f'I\'m absolutely delighted by {topic}! Everything about it brings me joy. This is exactly what I hoped for and I couldn\'t be more pleased.',
            'score': 1650,
            'subreddit': 'technology',
            'created_utc': (datetime.now() - timedelta(hours=2)).timestamp()
        },
        {
            'title': f'Disappointed and sad about {topic}',
            'text': f'I had high hopes for {topic}, but I\'m really disappointed. Things didn\'t work out as expected and I feel sad about the missed opportunities.',
            'score': 740,
            'subreddit': 'discussion',
            'created_utc': (datetime.now() - timedelta(hours=9)).timestamp()
        }
    ]
    
    # Shuffle and return requested number
    random.shuffle(mock_posts)
    return mock_posts[:limit]

def get_reddit_instance():
    """Create and return a Reddit API instance using PRAW"""
    try:
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        
        # Check if credentials are set (not placeholder values)
        if not client_id or client_id == "your_reddit_client_id" or not client_secret or client_secret == "your_reddit_client_secret":
            return None
            
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=os.getenv("REDDIT_USER_AGENT", "RedditSentimentApp/1.0")
        )
        return reddit
    except Exception:
        return None

def fetch_reddit_posts(topic: str, limit: int = 10) -> List[dict]:
    """
    Fetch Reddit posts related to the given topic.
    Falls back to mock data if Reddit API credentials are not available.
    Returns a list of dictionaries containing post data.
    """
    try:
        reddit = get_reddit_instance()
        
        # If no valid Reddit instance, use mock data
        if reddit is None:
            print(f"Using mock data for topic '{topic}' (Reddit API credentials not configured)")
            return get_mock_posts(topic, limit)
        
        posts = []
        
        # Try to fetch real Reddit posts
        try:
            # Search across all subreddits
            for submission in reddit.subreddit("all").search(topic, limit=limit, sort='relevance'):
                post_data = {
                    'title': submission.title,
                    'text': submission.selftext if hasattr(submission, 'selftext') else '',
                    'url': submission.url,
                    'score': submission.score,
                    'subreddit': submission.subreddit.display_name,
                    'created_utc': submission.created_utc
                }
                posts.append(post_data)
            
            # If no posts found, try hot posts from relevant subreddits
            if not posts:
                for submission in reddit.subreddit("all").hot(limit=limit * 2):
                    if topic.lower() in submission.title.lower() or topic.lower() in (submission.selftext or "").lower():
                        post_data = {
                            'title': submission.title,
                            'text': submission.selftext if hasattr(submission, 'selftext') else '',
                            'url': submission.url,
                            'score': submission.score,
                            'subreddit': submission.subreddit.display_name,
                            'created_utc': submission.created_utc
                        }
                        posts.append(post_data)
                        if len(posts) >= limit:
                            break
            
            if posts:
                return posts
        except Exception as e:
            print(f"Error fetching from Reddit API: {e}")
            print("Falling back to mock data...")
        
        # Fallback to mock data
        return get_mock_posts(topic, limit)
        
    except Exception as e:
        print(f"Error in fetch_reddit_posts: {e}")
        print("Using mock data as fallback...")
        return get_mock_posts(topic, limit)

