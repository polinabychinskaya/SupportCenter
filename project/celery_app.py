import os
from celery import Celery
from project import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-every-twenty-secs': {
        'task': 'user_auth.api.tasks.delete_by_completion',
        'schedule': 20.0,
    },
    'check-to-remind-every-minute': {
        'task': 'user_auth.api.tasks.email_reminder',
        'schedule': 60.0,
    },
}


@app.task()
def debug_task():
    print('Hello from debug_task')