import os

from celery import Celery
from django.conf import settings
import environ

env = environ.Env()
environ.Env.read_env()
REDIS_URL = env("REDIS_URL")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VacciNate.settings')
app = Celery('VacciNate', broker=REDIS_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')