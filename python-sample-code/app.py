import os
import time
from flask import Flask
from redis import Redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis-service")
redis_client = Redis(host=redis_host, port=6379, decode_responses=True)

def increment_hit_count():
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