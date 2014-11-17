#!/usr/bin/env python
import logging, pika, threading, datetime, os
from random import randrange
from urllib.parse import urlparse

class MessageQueue(object):
    u"Klasa do laczenia sie z kolejkami"
    logger = logging.getLogger(__name__+'Q')
    def __init__(self, queueName=None, queueAddress='localhost'):
        self.logger.error("Inicjalizacja kolejki: "+queueName+' adres: '+ queueAddress)
        self.name=queueName
        self.address=queueAddress
        
    def connect(self):
        url = urlparse(self.address)
        params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
                                           credentials=pika.PlainCredentials(url.username, url.password))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(params))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.name)
        
    def disconnect(self):
        self.connection.close()
        
class PublishQueue(MessageQueue):
    def publish(self, message):
        self.connect()
        self.channel.basic_publish(exchange='',
                      routing_key=self.name,
                      body=message)
        self.logger.error("Wyslano wiadomosc na kolejke: "+self.name+" wiadomosc: "+message);
        self.disconnect()
        
class ConsumerQueue(MessageQueue):
    consumer_thread=None
    def consume(self):
        self.consumer_thread = threading.Thread(target=self.setAsConsumer)
        self.logger.error("Start watku");
        self.consumer_thread.start()
        
    def setAsConsumer(self):
        self.logger.error("Ustawiono konsumera dla kolejki: "+self.name);
        self.connect()
        self.channel.basic_consume(self.callback,
                      queue=self.name,
                      no_ack=True)
        self.channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
       raise NotImplementedError("Please Implement this method")
        
class ReportConsumerQueue(ConsumerQueue):
    def callback(self, ch, method, properties, body):
        self.logger.error("--------Zamkniecie kolejki--------");
        self.channel.stop_consuming()
        self.disconnect()
        self.consumer_thread._stop()
        self.logger.error("Odebrano wiadomosc z kolejki: "+self.name+" wiadomosc: "+str(body))
        self.saveReport(body)
        
    def saveReport(self, report):
        now = datetime.datetime.now()
        reportFolder = 'reports/'
        fileName = reportFolder+'raport_'+now.strftime("%Y-%m-%d_%H%M")+str(randrange(10))+'.txt'
        handle1=open(fileName,'w+')
        handle1.write(str(report))
        handle1.close()
        self.logger.error("Zapisano plik raportu: "+fileName);
        