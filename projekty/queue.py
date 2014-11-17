#!/usr/bin/env python
import logging, pika, threading

class MessageQueue(object):
    u"Klasa do laczenia sie z kolejkami"
    logger = logging.getLogger(__name__+'Q')
    def __init__(self, queueName=None, queueAddress='localhost'):
        self.logger.error("Inicjalizacja kolejki: "+queueName)
        self.name=queueName
        self.address=queueAddress
        
    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.address))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.name)
        
    def disconnect(self):
        self.connection.close()
        
    def publish(self, message):
        self.connect()
        self.channel.basic_publish(exchange='',
                      routing_key=self.name,
                      body=message)
        self.logger.error("Wyslano wiadomosc na kolejke: "+self.name+" wiadomosc: "+message);
        self.disconnect()
        
    def consume(self, callback=None):
        if callback is None:
            self.consumer_thread = threading.Thread(target=self.setAsConsumer)
        else:
            self.consumer_thread = threading.Thread(target=setAsConsumer(callback))
        self.logger.error("Start watku");
        self.consumer_thread.start()
        
    def setAsConsumer(self, callback):
        self.logger.error("Ustawiono konsumera dla kolejki: "+self.name);
        self.connect()
        self.channel.basic_consume(self.callback,
                      queue=self.name,
                      no_ack=True)
        self.channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        self.consumer_thread._stop()
        self.logger.error("Odebrano wiadomosc z kolejki: "+self.name+" wiadomosc: "+str(body));

        