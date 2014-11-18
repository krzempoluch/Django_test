import logging, threading
from projekty.queue import ReportConsumerQueue

logger = logging.getLogger(__name__+'Startup')

def run():
    logger.error('--------Start aplikacji projekty--------')