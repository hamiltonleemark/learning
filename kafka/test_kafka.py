#!/usr/bin/env python
import logging
import msgpack
import json
import time
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError


def _recv_wait(consumer, topic, key, value, max_count, sleep_time=1):
    """ Wait for the consumer to be ready. """

    done = False
    count = 0
    for item in range(10):
        print("MARK 1; item", item)
        for msg in consumer:
            assert msg.topic == topic
            assert msg.partition == 0
            assert msg.key == key
            assert msg.value == value
            count += 1
            print("MARK 2; msg", item, count, sleep_time)
        time.sleep(sleep_time)
        print("MARK 3; msg", item, count, max_count, sleep_time)
        if count >= max_count:
            return True
        print("MARK 4; msg", item, count, max_count, sleep_time)
    assert count > 0


def test_default_producer_consumer():
    """  Test basic producer consumer. """

    topic = "topic-default"
    key = b"key-default"
    value = b"value-default"

    consumer = KafkaConsumer(topic, group_id='my-group',
                             consumer_timeout_ms=1000,
                             bootstrap_servers=['localhost:9092'])
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    producer.send(topic, key=key, value=value)
    _recv_wait(consumer, topic, key, value, 1)


def test_auto_offset_reset():
    """  Test auto offset reset. """

    topic = "topic-auto"
    key = b"key-auto"
    value = b"value-auto"

    consumer = KafkaConsumer(topic, group_id='my-group',
                             auto_offset_reset="earliest",
                             enable_auto_commit=False,
                             bootstrap_servers=['localhost:9092'])
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    for item in range(10):
        value="%s: %d" % (value, item)
        producer.send(topic, key=key, value=value)
    _recv_wait(consumer, topic, key, value, 10)
