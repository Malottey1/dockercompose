from flask import Flask
import redis
import os
import psycopg2

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host="redis", port=6379)

# Connect to PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create a table to log page visits (this should run once)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_visits (
        id SERIAL PRIMARY KEY,
        visit_count INTEGER
    )
""")
conn.commit()

@app.route("/")
def home():
    # Increment the visit counter in Redis
    count = r.incr("hits")
    
    # Log the visit count in PostgreSQL
    cursor.execute("INSERT INTO page_visits (visit_count) VALUES (%s)", (count,))
    conn.commit()
    
    return f"This page has been visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
