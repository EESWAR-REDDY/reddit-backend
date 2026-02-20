import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to PostgreSQL server (not a specific database)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="EESWAR"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

# Check if database exists
cur.execute("SELECT 1 FROM pg_database WHERE datname = 'reddit_sentiment_db'")
exists = cur.fetchone()

if not exists:
    cur.execute('CREATE DATABASE reddit_sentiment_db')
    print("Database 'reddit_sentiment_db' created successfully!")
else:
    print("Database 'reddit_sentiment_db' already exists.")

cur.close()
conn.close()
