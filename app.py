import os
from redis import Redis
from flask import Flask

app = Flask(__name__)

DATABASE_URI = os.getenv("DATABASE_URI", "redis://db1:6379")

counter = Redis.from_url(DATABASE_URI, encoding="utf-8", decode_responses=True)

@app.route("/")
def index():
    return "Hello Flask"

@app.route("/counter")
def get_counter():
    count = counter.incr("count")
    return dict(counter=count)
