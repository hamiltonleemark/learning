#!/usr/bin/env python
import msgpack
import json
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError


def test_basic():
    """ Try consumer and producer.

    Assume server is running locally.
    """
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    consumer = KafkaConsumer('my-topic', group_id='my-group',
                             bootstrap_servers=['localhost:9092'])
