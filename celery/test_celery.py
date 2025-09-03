import pytest
import tasks
import time
import logging
import celery

def test_add():
    result = tasks.add.delay(4, 6)
    while not result.ready():
        time.sleep(1)
        assert 10 == result.get()

def test_mimic_a_breakdown():
    for i in range(10):
        result = tasks.add.delay(4, 6)

    # Yes only the last one.
    while not result.ready():
        time.sleep(1)
        assert 10 == result.get()

    #app = celery.Celery("tasks", broker="redis://localhost:6379/0")
    app = celery.Celery('tasks', backend="redis://localhost")

    inspection = app.control.inspect()
    print("stats", inspection.stats())
    print("registered", inspection.registered())
    print("active", inspection.active())
    print("scheduled", inspection.scheduled())
    print("reserved", inspection.reserved())
