from confluent_kafka import Consumer
import logging
import boto3
import time
import os


class S3Connection:
    
    @staticmethod
    def s3_client():
        return boto3.Session().client(
                region_name="us-east-1",
                service_name="s3",
            )

    def check_bucket(self) -> bool:
        buckets = [bucket.get("Name") for bucket in self.s3_client().list_buckets().get("Buckets")] 
        return "sample-bucket" in buckets

    def create_bucket(self):
        self.s3_client().create_bucket(Bucket="sample-bucket")

    def load_data(self, msg):
        logging.info(msg)
        logging.info(msg.value())
        self.s3_client().put_object(
            Body=msg.value(),
            Bucket="sample-bucket",
            Key=f"{int(time.time())}.json"
            )

def consume_messages():
    conf = {
        'bootstrap.servers': os.getenv("KAFKA_PRODUCER_SERVER"),
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'group.id': 'my-group',
        'api.version.request': True,
        'api.version.fallback.ms': 0,
    }
    
    consumer = Consumer(conf)
    consumer.subscribe(["google-data"])
    while True:
        try:
            msg = consumer.poll(1.0)
            logging.info("Consumer polling")
            if msg:
                logging.info("Loading Message.")
                S3Connection().load_data(msg)
                logging.info("Loaded Message")
            else:
                logging.info("No Message")
        except Exception as e:
            logging.info(e)


if __name__ == "__main__":
    if not S3Connection().check_bucket():
        S3Connection().create_bucket()
    consume_messages()
    