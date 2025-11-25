import os
import time
import json
import allure
from datetime import datetime, timezone
import requests
from dateutil import parser as dateparser


class Webhook:
    def __init__(self, webhook_post_url=None, webhook_api_url=None, poll_interval=3, timeout=120):
        self.webhook_post_url = webhook_post_url or os.getenv("WEBHOOK_POST_URL")
        self.webhook_api_url = webhook_api_url or os.getenv("WEBHOOK_API_URL")
        self.api_key = os.getenv("WEBHOOK_API_KEY") or os.getenv("PIPEDREAM_API_KEY")

        if not self.webhook_post_url:
            raise ValueError("Missing WEBHOOK_POST_URL")
        if not self.webhook_api_url:
            raise ValueError("Missing WEBHOOK_API_URL")
        if not self.api_key:
            raise ValueError("Missing WEBHOOK_API_KEY or PIPEDREAM_API_KEY")

        self.poll_interval = poll_interval
        self.timeout = timeout
        self.session = requests.Session()

    @allure.step("Send webhook payload")
    def send_webhook(self, body, headers=None):
        headers = headers or {"Content-Type": "application/json"}
        return self.session.post(self.webhook_post_url, json=body)

    @allure.step("Fetch latest events from Pipedream source")
    def fetch_events(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = self.session.get(self.webhook_api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Pipedream events reside under "data"
        if isinstance(data, dict) and "data" in data:
            return data["data"]

        return data

    @allure.step("Wait for event containing field: {field_name}")
    def wait_for_event_with_field(self, field_name, correlation_id):
        deadline = time.time() + self.timeout

        while time.time() <= deadline:
            events = self.fetch_events()

            for e in events:
                body = e.get("e", {}).get("body")


                if not body:
                    body = e.get("json") or e.get("body") or e

                if isinstance(body, str):
                    try:
                        body = json.loads(body)
                    except Exception:
                        continue

                if isinstance(body, dict) and field_name in body and body.get("correlation") == correlation_id:
                    return {"event": e, "body": body}

            time.sleep(self.poll_interval)

        raise TimeoutError(f"Event with field '{field_name} and {correlation_id}' not found.")

    @staticmethod
    @allure.step("Validate x-request-time timestamp")
    def validate_x_request_time_timestamp(value, allowed_age_seconds=120):
        try:
            dt = dateparser.parse(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)
            return 0 <= (now - dt).total_seconds() <= allowed_age_seconds

        except Exception:
            return False