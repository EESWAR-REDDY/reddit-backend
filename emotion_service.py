import os

# Lazy import to avoid breaking server startup
emotion_classifier = None
_transformers_available = None

def _check_transformers():
    """Check if transformers can be imported"""
    global _transformers_available
    # Default to OFF to keep the app fast and demo-friendly on first run.
    # Enable by setting USE_HF_EMOTION_MODEL=true in backend/.env
    use_hf = os.getenv("USE_HF_EMOTION_MODEL", "false").strip().lower() in ("1", "true", "yes", "on")
    if not use_hf:
        _transformers_available = False
        return False
    if _transformers_available is None:
        try:
            from transformers import pipeline
            import torch
            _transformers_available = True
            return True
        except Exception as e:
            print(f"Warning: Transformers not available: {e}")
            _transformers_available = False
            return False
    return _transformers_available

def get_emotion_classifier():
    """Lazy load the emotion classifier to avoid loading on import"""
    global emotion_classifier
    
    if not _check_transformers():
        return None
        
    if emotion_classifier is None:
        try:
            from transformers import pipeline
            import torch
            
            print("Loading emotion classification model (this may take a minute on first run)...")
            emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=False
            )
            print("Emotion model loaded successfully!")
        except Exception as e:
            print(f"Error loading emotion model: {e}")
            return None
    return emotion_classifier

def detect_emotion(text: str) -> str:
    """
    Detect emotion using HuggingFace transformers.
    Returns: 'Joy', 'Anger', 'Sadness', 'Fear', 'Surprise', or 'Neutral'
    """
    if not text or len(text.strip()) == 0:
        return "Neutral"
    
    try:
        classifier = get_emotion_classifier()
        if classifier is None:
            # Fallback to simple keyword-based emotion detection if model fails
            return detect_emotion_simple(text)
        
        # Truncate very long text to avoid model issues
        text_to_analyze = text[:512] if len(text) > 512 else text
        
        result = classifier(text_to_analyze, top_k=1)
        
        if result and len(result) > 0:
            emotion_label = result[0]['label']
            
            # Map model labels to our emotion categories
            emotion_mapping = {
                'joy': 'Joy',
                'anger': 'Anger',
                'sadness': 'Sadness',
                'fear': 'Fear',
                'surprise': 'Surprise',
                'neutral': 'Neutral'
            }
            
            # Handle case-insensitive mapping
            emotion_lower = emotion_label.lower()
            return emotion_mapping.get(emotion_lower, 'Neutral')
        else:
            return "Neutral"
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        # Fallback to simple detection
        return detect_emotion_simple(text)

def detect_emotion_simple(text: str) -> str:
    """Simple keyword-based emotion detection as fallback"""
    text_lower = text.lower()
    
    joy_words = ['happy', 'excited', 'thrilled', 'joy', 'delighted', 'pleased', 'wonderful', 'amazing', 'great']
    anger_words = ['angry', 'furious', 'mad', 'rage', 'frustrated', 'annoyed', 'irritated', 'disgusted']
    sadness_words = ['sad', 'depressed', 'disappointed', 'unhappy', 'miserable', 'sorrow']
    fear_words = ['afraid', 'scared', 'fear', 'worried', 'anxious', 'terrified', 'frightened']
    surprise_words = ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected']
    
    joy_count = sum(1 for word in joy_words if word in text_lower)
    anger_count = sum(1 for word in anger_words if word in text_lower)
    sadness_count = sum(1 for word in sadness_words if word in text_lower)
    fear_count = sum(1 for word in fear_words if word in text_lower)
    surprise_count = sum(1 for word in surprise_words if word in text_lower)
    
    counts = {
        'Joy': joy_count,
        'Anger': anger_count,
        'Sadness': sadness_count,
        'Fear': fear_count,
        'Surprise': surprise_count
    }
    
    max_emotion = max(counts.items(), key=lambda x: x[1])
    return max_emotion[0] if max_emotion[1] > 0 else 'Neutral'

