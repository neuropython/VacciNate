import os
import logging

from celery import Celery
from django.conf import settings
import environ

env = environ.Env()
environ.Env.read_env()
REDIS_URL = env("REDIS_URL")

logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VacciNate.settings')
app = Celery('VacciNate', broker=REDIS_URL, backend=REDIS_URL, broker_heartbeat=2)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_connection_retry_on_startup = True

def on_redis_connect(sender=None, **kwargs):
    logger.info("Connected to Redis broker!")

app.on_configure.connect(on_redis_connect)  # Register the callback function
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')