from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment using TextBlob.
    Returns: 'Positive', 'Negative', or 'Neutral'
    """
    if not text or len(text.strip()) == 0:
        return "Neutral"
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

