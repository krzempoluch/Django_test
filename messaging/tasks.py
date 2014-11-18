from celery import Celery
import logging, time, datetime, os
from messaging.queue import PublishQueue

app = Celery('tasks', backend='amqp', broker='amqp://iypkanhf:f7W5aI8SOzDje6BM-e-JSPcR4k7V7VFh@turtle.rmq.cloudamqp.com/iypkanhf')
logger = logging.getLogger(__name__+'Task')
producer = PublishQueue('reportReturnQueue', 'amqp://iypkanhf:f7W5aI8SOzDje6BM-e-JSPcR4k7V7VFh@turtle.rmq.cloudamqp.com:5672/iypkanhf')

@app.task
def gen_report(id):
    now = datetime.datetime.now()
    time.sleep(5)
    raport = now.strftime("%Y-%m-%d %H:%M")+' ID: '+id+' Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris         isi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla         pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa         qui officia deserunt mollit anim id est laborum.'
    logger.error('-------------------generowanie raportu dla projektu: '+id+' zakonczone---------------')
    producer.publish(str(raport))
    return raport