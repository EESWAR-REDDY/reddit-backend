# Reddit Sentiment Analysis - Backend API

FastAPI backend for Reddit-based social sentiment monitoring and trend analysis using Machine Learning.

## 🚀 Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ML**: TextBlob (Sentiment), HuggingFace Transformers (Emotion)
- **NLP**: NLTK

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL database (Supabase)

## 🔧 Local Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/EESWAR-REDDY/reddit-backend.git
   cd reddit-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

5. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your Supabase DATABASE_URL
   ```

6. **Run server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   API docs: http://localhost:8000/docs

## 🚂 Railway Deployment

1. **Connect GitHub repository**
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `reddit-backend` repository

2. **Add Environment Variables**
   - Go to your project → Variables
   - Add:
     ```
     DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
     USE_HF_EMOTION_MODEL=false
     REDDIT_CLIENT_ID=your_client_id (optional)
     REDDIT_CLIENT_SECRET=your_client_secret (optional)
     REDDIT_USER_AGENT=RedditSentimentApp/1.0 (optional)
     ```

3. **Get Supabase Connection String**
   - Go to Supabase Dashboard
   - Project Settings → Database
   - Copy "Connection string" (URI format)
   - Replace `[YOUR-PASSWORD]` with your database password
   - Add to Railway variables as `DATABASE_URL`

4. **Deploy**
   - Railway will auto-detect Python and deploy
   - Your API will be available at: `https://your-app.railway.app`

## 📊 API Endpoints

- `POST /api/analysis/topic` - Analyze a topic
- `GET /api/analysis/results?topic=...` - Get stored results
- `GET /api/analysis/trends?topic=...&days=7` - Get trend data
- `GET /health` - Health check
- `GET /docs` - API documentation

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `USE_HF_EMOTION_MODEL` | Enable HuggingFace emotion model | No (default: false) |
| `REDDIT_CLIENT_ID` | Reddit API client ID | No (uses mock data) |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | No (uses mock data) |
| `REDDIT_USER_AGENT` | Reddit API user agent | No |

## 📝 Notes

- First deployment may take 5-10 minutes (installing dependencies)
- Emotion model is disabled by default for faster responses
- Mock Reddit data is used if Reddit API credentials are not provided
