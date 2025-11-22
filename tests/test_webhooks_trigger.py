import os
import pytest
from datetime import datetime, timezone
from utils.util_webhooks import Webhook

webhook_post_url = os.getenv("WEBHOOK_POST_URL", "https://cf67281d84e8b56f9ca65564b4a7b7b2.m.pipedream.net")
webhook_api_url  = os.getenv("WEBHOOK_API_URL", "https://api.pipedream.com/v1/sources/dc_v3u2VYA/events")

@pytest.fixture(scope="module")
def webhook_initiate():
    return Webhook(
        webhook_post_url=webhook_post_url,
        webhook_api_url=webhook_api_url
    )

def test_webhook_timestamp(webhook_initiate):
    current_time = datetime.now(timezone.utc).isoformat()
    payload = {
        "event": "qa.test",
        "payload": {"hello": "world"},
        "x-request-time": current_time
    }

    resp = webhook_initiate.send_webhook(payload)
    assert resp.status_code in (200, 201, 202)

    result = webhook_initiate.wait_for_event_with_field("x-request-time")
    body = result["body"]

    # timestamp validations
    assert webhook_initiate.validate_x_request_time_timestamp(body["x-request-time"])