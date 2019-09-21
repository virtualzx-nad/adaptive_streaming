"""Print messages from a topic to stdout"""
import logging
import sys
import time

import pulsar
import yaml

from pipeline_utils.schema_model import model_class_factory


if len(sys.argv) < 1:
    raise ArgumentError('Did not suppy settings through yaml file')
with open(sys.argv[1]) as f:
    settings = yaml.safe_load(f)
logging.basicConfig(level=settings.get('log_level', 'INFO'))
logger = logging.getLogger(__name__)

client = pulsar.Client(settings['broker'])

Model = model_class_factory(**settings['schema'])
consumer = client.subscribe(settings['topic'], subscription_name=settings['name'],
                            schema=pulsar.schema.AvroSchema(Model))

i = 0
max_records = settings['max_records']
while i != max_records: 
    message = consumer.receive()
    data = message.value()
    print("Message: %s" % str(data))
    consumer.acknowledge(message)
client.close()
