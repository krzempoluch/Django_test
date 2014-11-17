from celery import Celery
import logging, time, datetime
from celery.canvas import subtask
from projekty.queue import PublishQueue

app = Celery('tasks', backend='amqp', broker='amqp://')
logger = logging.getLogger(__name__+'Task')
producer = PublishQueue('reportReturnQueue')

@app.task(ignore_result=True)
def print_hello():
    logger.error('-------------------Task hello------------------')
    
@app.task
def gen_prime(x, callback=None):
    multiples = []
    results = []
    for i in range(x+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i):
                multiples.append(j)
    logger.error('-------------------liczenie zakończone---------------')
    producer.publish(str(results))
    return results

@app.task
def gen_report(id):
    now = datetime.datetime.now()
    time.sleep(5)
    raport = now.strftime("%Y-%m-%d %H:%M")+' ID: '+id+' Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris         isi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla         pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa         qui officia deserunt mollit anim id est laborum.'
    logger.error('-------------------generowanie raportu dla projektu: '+id+' zakonczone---------------')
    producer.publish(str(raport))
    return raport