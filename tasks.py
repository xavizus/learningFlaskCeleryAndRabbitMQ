from celery import Celery

from config import BROKER_URL, BACKEND_URL

celery = Celery('tasks',backend=BACKEND_URL, broker=BROKER_URL)
celery.config_from_object('celeryconfig')

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, add.s(16,16), name='Add every 30 seconds')

@celery.task
def add(x,y):
    return x + y
