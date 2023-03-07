import time


from celery import Celery

# Wait for rabbitmq to be started
# time.sleep(20)

app = Celery(
    'crawler',
    broker='redis://localhost:6379',
    CELERYD_CONCURRENCY=1
)

app.send_task('crawl', args=['http://www.google.com'])
