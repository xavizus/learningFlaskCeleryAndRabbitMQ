from celery import Celery

from config import BACKEND_URL, BROKER_URL

app = Celery('tasks', backend=BACKEND_URL, broker=BROKER_URL)

@app.task
def add(x, y):
    return x + y
