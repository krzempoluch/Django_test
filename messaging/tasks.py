from celery import Celery
import logging, time, datetime, os, json
# from messaging.queue import PublishQueue
app = Celery('tasks', backend='amqp', broker=json.loads(os.environ['cloudamqp_56497'])['uri'])
logger = logging.getLogger(__name__+'Task')
# producer = PublishQueue('reportReturnQueue', 'amqp://iypkanhf:f7W5aI8SOzDje6BM-e-JSPcR4k7V7VFh@turtle.rmq.cloudamqp.com:5672/iypkanhf')

@app.task
def gen_report(id):
    now = datetime.datetime.now()
    time.sleep(5)
    raport = now.strftime("%Y-%m-%d %H:%M")+' ID: '+id+' Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris         isi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla         pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa         qui officia deserunt mollit anim id est laborum.'
    logger.error('-------------------generowanie raportu dla projektu: '+id+' zakonczone---------------')
#     producer.publish(str(raport))
    saveReport(str(raport), id)
    return raport

def saveReport(report, id):
        now = datetime.datetime.now()
        reportFolder = '/var/lib/openshift/54646c675973ca5701000018/app-root/runtime/repo/reports/'
        fileName = reportFolder+'raport_'+now.strftime("%Y-%m-%d_%H%M")+'_'+id+'.txt'
        handle1=open(fileName,'w+')
        handle1.write(str(report))
        handle1.close()
        logger.error("Zapisano plik raportu: "+fileName);