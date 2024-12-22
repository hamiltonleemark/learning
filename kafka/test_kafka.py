#!/usr/bin/env python

""" Learning how to use Kafka. """

import logging
import msgpack
import json
import time
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError

def _consumer_wait(consumer, sleep_time=1, max_wait=10):
    """ Consumer only registers with the daemon when poll is called.

    @param sleep_time must be an integer in seconds.
    @param max_wait must be an integer greater than sleep_time.
    """

    assert sleep_time < max_wait

    consumer.poll(timeout_ms=0, max_records=1, update_offsets=False)
    for _ in range(max_wait):
        if consumer.assignment():
            return True
        time.sleep(sleep_time)
    raise ValueError("consumer is not ready")


def _recv_wait(consumer, topic, key, value, max_count, sleep_time=1):
    """ Wait for the consumer to be ready. """

    count = 0

    for _ in range(10):
        for msg in consumer:
            assert msg.topic == topic
            assert msg.partition == 0
            assert msg.key == key
            ##
            # msg.offset increases per message.
            print(f"MARK 2: recv {msg.offset} {msg.value} checking against {value}")
            assert msg.value.startswith(value)
            count += 1
            if count >= max_count:
                return True
        time.sleep(sleep_time)
        print(f"MARK: slept {sleep_time}")
        if count >= max_count:
            return True
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
    _consumer_wait(consumer)
    _recv_wait(consumer, topic, key, value, 1)


def test_auto_offset_reset():
    """  Test auto offset reset. """

    topic = "topic-auto"
    key = b"key-auto"
    prefix_value = b"value-auto"

    consumer = KafkaConsumer(topic, group_id='my-group',
                             auto_offset_reset="earliest",
                             enable_auto_commit=False,
                             bootstrap_servers=['localhost:9092'])
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    for item in range(10):
        value = b"%s: %d" % (prefix_value, item)
        print(f"MARK: send {key}:{value}")
        producer.send(topic, key=key, value=value)

    _consumer_wait(consumer)
    _recv_wait(consumer, topic, key, prefix_value, 10)
    consumer.commit()
