import datetime
import json
import os
import random

from dotenv import load_dotenv
from flask import Flask
from google.cloud import pubsub_v1
from google.oauth2 import service_account


load_dotenv(override=True)
PROJECT_ID = os.environ.get("PROJECT_ID", "oshin-laboratry")
TOPIC_ID = os.environ.get("TOPIC_ID", "terraform-test-app-log-v2")
SERVICE_ACCOUNT_FILE_PATH = os.environ.get("SERVICE_ACCOUNT_FILE_PATH", "oshin-laboratry.json")
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE_PATH)

app = Flask(__name__)


@app.route("/")
def publish():
    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    log_data = _get_log_data()
    publisher.publish(topic_path, json.dumps(log_data).encode('utf-8'))

    return "OK"


def _get_log_data():
    user_id = random.randint(1, 1000000)
    message = f"test_{user_id}"
    logged_at = int(datetime.datetime.now().timestamp() * 1_000_000)
    return {
        "user_id": user_id,
        "message": message,
        "logged_at": logged_at
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
