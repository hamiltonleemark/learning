import time
from .celery import app
import celery.utils.log

logger = celery.utils.log.get_task_logger(__name__)


@app.task(acks_late=True)
def add(x, y):
    logger.info(f"Adding {x} + {y}")
    return x + y


@app.task(acks_late=True)
def mul(x, y):
    logger.info(f"Adding {x} x {y}")
    return x * y


@app.task(acks_late=True)
def xsum(numbers):
    logger.info(f"sum {numbers}")
    return sum(numbers)

@app.task(acks_late=True)
def sleep(seconds):
    logger.info(f"sleep {seconds} seconds")
    time.sleep(seconds)
    return seconds
