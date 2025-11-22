import os
import pytest
import allure
from datetime import datetime, timezone
from utils.util_webhooks import Webhook

@pytest.fixture(scope="module")
def webhook_initiate():
    return Webhook(
        webhook_post_url=os.getenv("WEBHOOK_POST_URL"),
        webhook_api_url=os.getenv("WEBHOOK_API_URL")
    )

@allure.feature("Webhook Validation")
@allure.story("Webhook timestamp validation")
@allure.severity(allure.severity_level.CRITICAL)
def test_webhook_timestamp(webhook_initiate):
    current_time = datetime.now(timezone.utc).isoformat()
    payload = {
        "event": "qa.test",
        "payload": {"hello": "world"},
        "x-request-time": current_time
    }

    with allure.step("Send webhook event to Pipedream endpoint"):
        resp = webhook_initiate.send_webhook(payload)
        assert resp.status_code in (200, 201, 202)

    with allure.step("Fetch event and validate timestamp"):
        result = webhook_initiate.wait_for_event_with_field("x-request-time")
        body = result["body"]
        assert webhook_initiate.validate_x_request_time_timestamp(body["x-request-time"])