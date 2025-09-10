import pytest
import tasks
import time
import logging
import celery

def test_add():
    """ Test adding a result. """

    result = tasks.add.delay(4, 6)
    while not result.ready():
        logging.debug("waiting for result")
        time.sleep(1)
    assert result.get() == 10

def get_celery_queue_items(app, queue_name):
    import base64
    import json

    with app.pool.acquire(block=True) as conn:
        tasks = conn.default_channel.client.lrange(queue_name, 0, -1)
        decoded_tasks = []

    for task in tasks:
        j = json.loads(task)
        body = json.loads(base64.b64decode(j['body']))
        decoded_tasks.append(body)

    return decoded_tasks


def get_queued_jobs(app, queue_name):
    connection = app.connection()

    try:
        channel = connection.channel()
        name, jobs, consumers = channel.queue_declare(queue=queue_name, passive=True)
        active_jobs = []

        def dump_message(message):
            active_jobs.append(message.properties['application_headers']['task'])

        channel.basic_consume(queue=queue_name, callback=dump_message)

        #for job in range(jobs):
        #    connection.drain_events()

        return active_jobs
    finally:
        connection.close()

def test_mimic_a_breakdown():
    """ mimic failure. """

    logging.info("starting test")

    ##
    # First call add tasks 10 times.
    ##
    results = []
    for i in range(10):
        results += [tasks.add.delay(4, 6)]

    # Yes only one.
    logging.info("waiting for result to be ready")
    for result in results:
        logging.info(f"result {result}")

    app = celery.Celery('tasks', backend="redis://localhost",
                         broker='pyamqp://guest@localhost//')

    inspection = app.control.inspect()
    print("stats", inspection.stats())
    print("registered", inspection.registered())
    print("active", inspection.active())
    print("scheduled", inspection.scheduled())
    print("reserved", inspection.reserved())

    jobs = get_queued_jobs(app, "celery")
    logging.info("number of jobs %s", len(jobs))
    for job in get_queued_jobs(app, "celery"):
        logging.info(f"job {job}")
        job.forget()
    return

    inspection = app.control.inspect()
    print("stats", inspection.stats())
