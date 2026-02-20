"""Test database connection"""
import sys
from database import engine, DATABASE_URL

print("Testing database connection...")
print(f"Database URL: {DATABASE_URL}")

try:
    with engine.connect() as conn:
        print("[OK] Database connection successful!")
        sys.exit(0)
except Exception as e:
    print(f"[ERROR] Database connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure PostgreSQL is running")
    print("2. Check database 'reddit_sentiment_db' exists")
    print("3. Verify username and password in .env file")
    sys.exit(1)
