import os
import time
import json
from datetime import datetime, timezone
import requests
from dateutil import parser as dateparser


class Webhook:
    def __init__(self, webhook_post_url=None, webhook_api_url=None, poll_interval=3, timeout=120):
        self.webhook_post_url = webhook_post_url or os.getenv("WEBHOOK_POST_URL")
        self.webhook_api_url = webhook_api_url or os.getenv("WEBHOOK_API_URL")
        self.api_key = os.getenv("WEBHOOK_API_KEY")
        self.poll_interval = poll_interval
        self.timeout = timeout
        self.session = requests.Session()
    def send_webhook(self, body, headers=None):
        headers = headers or {"Content-Type": "application/json"}
        return self.session.post(self.webhook_post_url, json=body, headers=headers)

    def fetch_events(self):
        print("API KEY USED:", self.api_key)
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = self.session.get(self.webhook_api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ("data", "items", "requests"):
                if key in data and isinstance(data[key], list):
                    return data[key]

        return [data]

    def wait_for_event_with_field(self, field_name):
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

                if isinstance(body, dict) and field_name in body:
                    return {"event": e, "body": body}

            time.sleep(self.poll_interval)

        raise TimeoutError(f"Event with field '{field_name}' not found.")

    @staticmethod
    def validate_x_request_time_timestamp(value, allowed_age_seconds=120):
        try:
            dt = dateparser.parse(value)

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)
            return 0 <= (now - dt).total_seconds() <= allowed_age_seconds

        except Exception:
            return False