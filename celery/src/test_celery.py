import pytest
import time
import logging
import celery
import celery.result
import proj.tasks


def test_chain():
    """ Learn how to chain celery. """

    ##
    # First call add tasks 10 times.
    ##
    assert proj.tasks.add.delay(4, 4).get() == 8
    assert proj.tasks.mul.delay(8, 8).get() == 64
    # mul.s is a curry function.
    result = celery.chain(proj.tasks.add.s(4, 4) | proj.tasks.mul.s(8))
    result.delay().get() == 64


def test_sleep():
    """ chain celery. """

    assert proj.tasks.sleep.delay(100)


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

    app = celery.Celery('tasks', backend="redis://localhost",
                         broker='pyamqp://guest@localhost//')

    inspection = app.control.inspect()
    print("registered", inspection.registered())
    print("active", inspection.active())
    print("scheduled", inspection.scheduled())
    print("reserved", inspection.reserved())

    active = inspection.active()
    for worker, jobs in active.items():
        for job in jobs:
            print("id", job["id"])
            job = celery.result.AsyncResult(job["id"])
            job.forget()
