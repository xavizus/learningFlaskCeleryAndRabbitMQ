# Flask, celery and RabbitMQ learning

# Celery

## To start a worker
There are multiple ways to start workers.
The following is the simplest form for starting a worker:
```
celery -A tasks worker -l info
```
- -A stands for app, which should be the name of the celery python file. in this example it.s tasks.py, therefore tasks.
- **worker** is just a type, you can start your celery in other ways, for example if you want to do a scheduled jobb, you should use **beat**.
- -l stands for logging-type, for this example we just want log info. Other levels are DEBUG, INFO, WARNING, ERROR, CRITICAL, or FATAL

## To start the scheduler
To start the scheduler is as simple as starting the worker:
```
celery -A beat -l info
```
An important note: the scheduler just add tasks to the workers. Which makes it important to launch the scheduler and the worker.