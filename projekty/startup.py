import logging, threading

logger = logging.getLogger(__name__+'Startup')

def run():
    logger.error('--------Start aplikacji projekty--------')
    subscriber = ReportConsumerQueue('reportReturnQueue', 'amqp://iypkanhf:f7W5aI8SOzDje6BM-e-JSPcR4k7V7VFh@turtle.rmq.cloudamqp.com:5672/iypkanhf')
    subscriber.consume()