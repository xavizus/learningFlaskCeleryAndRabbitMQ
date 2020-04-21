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

## Some example code snippets
I will list some code snippet examples in this section

### Only allow 1 job to be processed at a time with RabbitMQ
It's quite simple to make sure celery only do one job in a queue at a time. One important key is that you need too import Queue from kombu.
```Python
from kombu import Queue
celery.conf.task_queues = (
            Queue('getinvoice', routing_key="getinvoice", queue_arguments={'x-max-length': 1}),
        )
```
The first row just tells celery that we will be chaning how an Queue will behave.

At the queue function, we send three params:
1. The queue name
2. The routing key (in this example the queue name and route key are the same)
3. *queue_arguments* is an dictaroy with settings which is sent to RabbitMQ. In this example, we are sending `x-max-length:1` which basically says that the queue should only processes one message at a time.

### To predefine tasks routes
You can predifine tasks routes to make sure each task uses specific route.
```Python
celery.conf.task_routes = {
        'tasks.getActiveInvoices': {'queue': 'getinvoice'},
        'tasks.sendInvoice': {'queue': 'jobs'},
        'tasks.processCallback': {'queue': 'callback'},
        'tasks.createdStatus': {'queue': 'invoicestatus'},
    }
```
1. The key is the name of the task
2. The key takes a dictionary which requires a key named `queue` and a queue name.

### To schedule tasks
To schedule taks, you take advantage of the built-in config beat_schedule in Celery.
The simplest form to make a schedule is to use the seconds:
```python
celery.conf.beat_schedule = {
        # Run every 5 min
        'get-all-ready-to-send-invoices': {
            'task': 'tasks.getActiveInvoices',
            'schedule': 300.0,
            'options': {'queue': 'getinvoice'}
        },
}
```
You can include multiple schedules in the same beat:
```python
celery.conf.beat_schedule = {
        # Run every 5 min
        'get-all-ready-to-send-invoices': {
            'task': 'tasks.getActiveInvoices',
            'schedule': 300.0,
            'options': {'queue': 'getinvoice'}
        },

        # Run every 15 min
        'get-failed-callbacks-emails': {
            'task': 'tasks.checkEmailInbox',
            'schedule': 900.0,
            'options': {'queue': 'getemail'}
        },
    }
```

#### Crontab
You can even perform advanced schedules with crontab in Celery. It requires to import the crontab from the library celery.schedules
```Python
from celery.schedules import crontab
```
This chrontab resembles the syntax of crontab in linux, though it uses keywords such as, `minute`,`hour`,`day_of_week`, `day_of_month`,`month_of_year`.
Each of the key word arguments above can accept integer values as arguments. The range of these values is restricted e.g. `0–59` for `minute` , `0–23` for hour, `1–31` for day_of_month etc.
Each of the key word arguments above can also accept crontab patterns.
I would recommend to use [crontab-generator](https://crontab-generator.org/)
For an example, if you want job to run 23:00 every monday the syntax would be like following: `0 23 * * 1`.
If you would type it out with celery crontab you would need to use the following syntax
`crontab(minute=0, hour=23, day_of_month='*', month_of_year='*', day_of_week=1)`.

To use this code practically:
```python
from celery.schedules import crontab
celery.conf.beat_schedule = {
        # Run every 5 min
        'get-all-ready-to-send-invoices': {
            'task': 'tasks.getActiveInvoices',
            'schedule': 300.0,
            'options': {'queue': 'getinvoice'}
        },

        # Run every 15 min
        'get-failed-callbacks-emails': {
            'task': 'tasks.checkEmailInbox',
            'schedule': 900.0,
            'options': {'queue': 'getemail'}
        },
        # Run every monday 23:00
        'get-total-invoices': {
            'task': 'tasks.getTotalInvoices'
            'schedule': crontab(minute=0, hour=23, day_of_month='*', month_of_year='*', day_of_week=1),
            'options': {
                'queue': 'gettotalinvoices'
            }
        },
    }
```

# Logging
In this project I am going to use logstash (ELK-stack) and the console as loghandlers. All logging code are in the file flaskLogger.
In Flask, there is already an [logger](https://flask.palletsprojects.com/en/1.1.x/logging/), which I will use and append with `logstash.TCPLogstashHandler(host, port, version=1, message_type=appName)`.
In Flask, there are two events called "after_request" and "before_request" that I could use, and I find after_request most usefull. This mean I don't need to write a log entry in every route. Though I could still do normal logging by using `app.logger.debug/info/warning/error/critical`.

# Supervisors
There are mutilple supervisors in the wild, the most common one is systemd which is standard in most Linux distros.
Therefore I need some information on how to deploy an / multiple app(s) with systemd in mind.

## Systemd
To create a process, you need to create a unit-file in the folder /etc/systemd/system/*filename*.service
```
[Unit]
Description="Flask, celery and RabbitMQ learning app"
After=network.target

[Service]
User=someUser
Group=someGroup
ExecStart=/path/tp/start
[Install]
WantedBy=multi-user.target
```
If I would like to controll two services at once, but still independent of each other, you can use the "wants" command:
`apps.service`
```
[Unit]
After=network.target
Wants=first.service second.service
[Install]
WantedBy=multi-user.target
```
In order to use above code, you need to change your target on your Unit, by adding PartOf:
```
[Unit]
Description="Flask, celery and RabbitMQ learning app"
After=network.target
PartOf=first.target

[Service]
User=someUser
Group=someGroup
ExecStart=/path/tp/start
[Install]
WantedBy=multi-user.target
```

To use the service, you use the command: `systemctl status/stop/start/restart apps.service`

## Supervisord
There is also another common supervisor, called supervisord.
It's quite easy to add a service to supervisord.
In the file supervisord.conf, you can add the following:
```
[program:firstApp]
command=/path/to/your/startFile/
user=yourUser
```
To controll multiple apps at the same time (independent of eachother)
```
[program:firstApp]
command=/path/to/your/startFile/
user=yourUser

[program:secondApp]
command=/path/to/your/startFile/
user=yourUser

[group:apps]
programs=firstApp,secondApp
```
To start the apps, you just use: `supervisorctl status/stop/start/restart apps:*`

# Python factory
In the file /dbFactory/dbFactory.py, I am not using \__init__() function, because when you call init, the object dbFactory has already been created. Instead we call \__new__() this is called before \__init__(). Which make it possible to create another class than the one we call. 
The negative part of doing it this way, pylint can't resolve the actually class that's been loaded in runtime. Therefore you get the error "No-member".