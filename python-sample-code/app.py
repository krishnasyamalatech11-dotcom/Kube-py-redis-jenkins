import os
import time
from flask import Flask
from redis import Redis

app = Flask(__name__)

# Read Redis host from environment variable
redis_host = os.getenv("REDIS_HOST", "redis-service")
redis_port = 6379

# Create Redis client
redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

def increment_hit_count():
    """
    Retry Redis connection a few times before giving up.
    This helps when Redis starts a little later than the app.
    """
    for attempt in range(10):
        try:
            return redis_client.incr("hits")
        except Exception as e:
            print(f"Redis not ready yet. Attempt {attempt + 1}/10 failed: {e}")
            time.sleep(3)
    return None

@app.route("/")
def hello():
    count = increment_hit_count()

    if count is None:
        return "Redis is not ready yet. Please try again in a few seconds.\n", 503

    return f"Hello World! I have been seen {count} times updated again\n"

@app.route("/health")
def health():
    return "OK\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)