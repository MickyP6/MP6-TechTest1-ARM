import os
import json

APP_SECRETS = json.loads(os.environ["PRODUCER_SECRETS"])

KAFKA_PRODUCER_SERVER = APP_SECRETS["KAFKA_PRODUCER_SERVER"]
KAFKA_CLIENT_APP_ID = APP_SECRETS["KAFKA_CLIENT_APP_ID"]

