IDnow Case Study – API & Webhook Automation

This project contains a realistically small automation setup that covering -
	1.	REST API testing (CRUD flow + negative cases)
	2.	Webhook delivery validation using a live Pipedream endpoint

Everything is written in Python using pytest, with a simple structure that keeps the tests readable, maintainable, and easy to extend.

API Testing

For the API portion, I used jsonplaceholder.typicode.com, mainly because:
	•	it behaves like a real REST API
	•	supports GET/POST/DELETE
	•	returns consistent mock responses
	•	requires no authentication

I added a small API wrapper (BaseAPI) to keep the request logic in a single place and make the tests easier to read.

The workflow tests include:
	•	Creating a “user” (POST)
	•	Fetching users (GET)
	•	Deleting a user (DELETE)
	•	Negative checks (invalid payloads, wrong paths, etc.)

Payloads used in POST tests are stored as JSON in a small data folder to keep the tests clean.

Webhook Testing

For webhook validation I used Pipedream, because it:
	•	Provides a stable public URL for receiving webhook traffic
	•	Offers an API for fetching captured events
	•	Is free to use and does not require hosting anything myself

The webhook tests do the following:
	1.	Send a webhook event to the Pipedream URL
	2.	Poll the Pipedream API until the event is captured
	3.	Extract the payload
	4.	Validate that:
	•	the event contains the custom x-request-time field
	•	the timestamp is in UTC
	•	and it’s not older than 2 minutes

The utility class (Webhook) handles all of this and hides the complexity inside a small set of methods.

Running the Tests

Install dependencies:
`pip install -r requirements.txt`

Run Test:
`pytest`

Generate allure reports:
`pytest --alluredir=allure-results`

View report:
`allure serve allure-results`

Design Choices:

I kept the framework intentionally simple:
	•	Requests + pytest are enough for this level of testing
	•	A thin API client avoids duplicating URLs and makes the tests readable
	•	Test data is externalized so payloads can be changed without touching test logic
	•	Webhook polling is wrapped into a single reusable method
	•	Allure reports were added to make the execution trace easier to follow

This structure leaves room to grow into something larger without being over-engineered for a case study.

Trade-offs
	•	JsonPlaceholder always returns 201 for POST requests, even with invalid data. I adjusted the tests to expect the platform’s behavior, not valid REST semantics.
	•	Webhook polling uses a simple loop. In a real environment I’d switch to a more robust event-based solution or message queue.
	•	The framework is intentionally lightweight. For a real product, I would add logging, type validation, schema checks, and CI-quality test grouping.


One Test Design Decision Based on Risk

I added timestamp validation on the webhook payload because timing-related issues tend to be high-risk in distributed systems.
If the webhook arrives late or has the wrong timezone, downstream systems can behave unpredictably.
By validating freshness (≤ 2 minutes) and format, the test ensures the producer and consumer are aligned in terms of event timing.