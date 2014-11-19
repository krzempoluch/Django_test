from django_sse.views import BaseSseView
import logging, os, time
from messaging.queue import ConsumerQueue
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__+'sse')
sendQueue = ['one']

class EventConsumerQueue(ConsumerQueue):
    def callback(self, ch, method, properties, body):
        global sendQueue
        self.logger.error("Odebrano wiadomosc z kolejki: "+self.name+" wiadomosc: "+str(body))
        sendQueue.append(str(body))
    
   
def loop():
    global sendQueue
    mygenerator = (x*x for x in range(10))
    while True:
        for val in sendQueue:
            yield val
        time.sleep(5)
        
@method_decorator(csrf_exempt)
def iterator(request):
    response = HttpResponse(loop(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response

            