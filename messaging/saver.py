from celery import Celery
from django.conf import settings
import logging, time, datetime, os, json

from messaging.queue import PublishQueue
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_test.settings')
app = Celery('saver')
app.config_from_object('django.conf:settings')

logger = logging.getLogger(__name__+'Task')
producer = PublishQueue('eventReturnQueue', 'amqp://localhost:5672//')

@app.task
def saveReport(report):
        now = datetime.datetime.now()
        reportFolder = 'reports/'
        fileName = reportFolder+'raport_'+now.strftime("%Y-%m-%d_%H%M%S")+'.txt'
        handle1=open(fileName,'w+')
        handle1.write(str(report))
        handle1.close()
        producer.publish('Wygenerowano nowy raport')
        logger.error("Zapisano plik raportu: "+fileName);