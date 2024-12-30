import datetime
import json
import os
import random

from dotenv import load_dotenv
from flask import Flask
from google.cloud import pubsub_v1
from google.oauth2 import service_account


load_dotenv(override=True)
PROJECT_ID = os.environ.get("PROJECT_ID")
TOPIC_ID = os.environ.get("TOPIC_ID")
PRIVATE_KEY_ID = os.environ.get("PRIVATE_KEY_ID")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY").replace("\\n", "\n")
CLIENT_EMAIL = os.environ.get("CLIENT_EMAIL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_X509_CERT_URL = os.environ.get("CLIENT_X509_CERT_URL")

app = Flask(__name__)

credentials = service_account.Credentials.from_service_account_info(
    {
        "type": "service_account",
        "project_id": PROJECT_ID,
        "private_key_id": PRIVATE_KEY_ID,
        "private_key": PRIVATE_KEY,
        "client_email": CLIENT_EMAIL,
        "client_id": CLIENT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": CLIENT_X509_CERT_URL,
        "universe_domain": "googleapis.com"
    }
)
publisher = pubsub_v1.PublisherClient(credentials=credentials)


@app.route("/")
def publish():
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
