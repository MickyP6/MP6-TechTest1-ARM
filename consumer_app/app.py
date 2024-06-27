from confluent_kafka import Consumer

import logging


logging.basicConfig(level=logging.DEBUG)

conf = {
    'bootstrap.servers': 'localhost:9092',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
    'group.id': 'my-group',
    'api.version.request': True,
    'api.version.fallback.ms': 0
}

def consume_messages():
    consumer = Consumer(conf)
    consumer.subscribe(["google-data"])
    while True:
        try:
            msg = consumer.poll(1.0)
            logging.info("Consumer polling")
            if msg:
                logging.info(msg.value().decode('utf-8'))
            else:
                logging.info("No Message")
        except Exception as e:
            logging.info(e)


if __name__ == "__main__":
    consume_messages()