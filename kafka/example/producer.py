#!/usr/bin/env python
""" Producer test. """

# pylint: disable=consider-using-f-string
import time
import logging
import json
import msgpack
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Asynchronous by default
future = producer.send('my-topic', b'raw_bytes')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError as earg:
    logging.exception(earg)

# Successful result returns assigned partition and offset
print("topic:", record_metadata.topic)
print("partition:", record_metadata.partition)
print("offset:", record_metadata.offset)

# produce keyed messages to enable hashed partitioning
producer.send('my-topic', key=b'foo', value=b'bar')

# encode objects via msgpack
producer = KafkaProducer(value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key': 'value'})

# produce json messages
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'))
producer.send('json-topic', {'key': 'value'})

# produce asynchronously
for item in range(100):
    producer.send('my-topic', 'msg %d' % item)

time.sleep(10)

def on_send_success(rmetadata):
    """ Send on success. """

    print(rmetadata.topic)
    print(rmetadata.partition)
    print(rmetadata.offset)


def on_send_error(excp):
    """ On send error. """

    logging.error('I am an errback', exc_info=excp)


# produce asynchronously with callbacks
producer.send('my-topic', 'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)

# block until all async messages are sent
producer.flush()

# configure multiple retries
producer = KafkaProducer(retries=5)
