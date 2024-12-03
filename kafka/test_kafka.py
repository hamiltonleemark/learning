#!/usr/bin/env python
import logging
import msgpack
import json
import time
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError



def test_default_producer_consumer():
    """  Test basic producer consumer. """

    topic = "topic-default"
    consumer = KafkaConsumer(topic, group_id='my-group',
                             consumer_timeout_ms=1000,
                             bootstrap_servers=['localhost:9092'])
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    print(consumer.assignment())
    time.sleep(10)
    print(consumer.assignment())
    return

    future = producer.send(topic, b'raw_bytes')
    count = 0
    for msg in consumer:
        assert msg.topic == "my-topic"
        assert msg.partition == 0
        ##
        # offset keeps going up. Seems to be a persistent value.
        assert msg.offset > 0
        ##
        assert msg.key is None
        assert msg.value == b'raw_bytes'
        count += 1
    assert count > 0


def test_default_auto_offset_reset():
    """  Test basic auto offset consumer. """

    topic = "topic-auto-reset"
    consumer = KafkaConsumer(topic, group_id='my-group',
                             consumer_timeout_ms=1000,
                             bootstrap_servers=['localhost:9092'])
    future = producer.send(topic, b'data-auto-reset')
    count = 0
    for msg in consumer:
        print("MARK: 2")
        assert msg.topic == topic
        assert msg.partition == 0
        ##
        # offset keeps going up. Seems to be a persistent value.
        assert msg.offset > 0
        logging.info("offset %d", msg.offset)
        ##
        assert msg.key is None
        assert msg.value == b'data-auto-reset'
        count += 1
    assert count > 0
