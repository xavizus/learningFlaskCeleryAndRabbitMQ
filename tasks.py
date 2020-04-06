from celery import Celery

from config import RABBITMQ, RESULT_BACKEND

celery = Celery('tasks',backend=RESULT_BACKEND, broker=RABBITMQ)
celery.config_from_object('celeryconfig')

@celery.task
def add(x,y):
    return x + y

# To run a task every specific time.
celery.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
