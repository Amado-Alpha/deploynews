from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsAggregator.settings')

app = Celery('NewsAggregator')
app.conf.enable_utc = False

app.conf.update(timezone = 'UTC')

app.config_from_object('django.conf:settings', namespace='CELERY')


# Celery Beat Settings

target_names = ['politics', 'sports', 'latest']

app.conf.beat_schedule = {
    
    'scrape-every-minute': {
        'task': 'news.tasks.auto_scrape_news',  # Update the path accordingly
        'schedule': crontab(minute='*/1'),
        'args': (target_names,), 
    },
}



# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')