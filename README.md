**IDnow Case Study – API & Webhook Automation**

This repository contains a compact backend automation suite created for the IDnow technical case study.
The main areas covered are:  
	1.	API testing (CRUD flow, basic validations, negative checks)  
	2.	Webhook validation against a live endpoint (Pipedream)  
	3.	A maintainable structure without over-engineering anything  

The code is in Python (Pytest), with a couple of small utilities to avoid repeating logic.

GitHub repository (main code — easiest to browse):
https://github.com/karthikr89/idnow_pytest

GitLab repository (CI/CD pipeline runs + artifacts):
https://gitlab.com/karthikr89-group/IDNow

**<i>Why GitHub + GitLab?</i>**

I put the code on GitHub simply because it’s easier to share during reviews — no permissions needed and it’s familiar to most people.

For the CI/CD part, I used GitLab instead of GitHub Actions because:  
	•	GitLab’s pipeline syntax is straightforward  
	•	Allure reports integrate nicely as artifacts  
	•	I already had a runner setup there  

It also reflects something that happens in real environments: sometimes code and CI don’t live on the same platform. It keeps the project clean while still showing a working pipeline.

**<i>What the Project Covers?</i>**

**<i>API Testing</i>**

I used jsonplaceholder (https://jsonplaceholder.typicode.com) because:  
	•	It behaves like a real REST service  
	•	Supports GET / POST / DELETE  
	•	Returns predictable mock responses  
	•	No auth or token handling needed  

There’s a small API client (BaseAPI) so the tests don’t need to worry about URLs or request boilerplate.

The API workflow includes:  
	•	Creating a resource (POST)  
	•	Reading data (GET)  
	•	Deleting a resource (DELETE)  
	•	A few negative paths just to show error handling (invalid IDs, wrong endpoints)  

Payloads for POST tests live in a tiny data folder so they can be edited without touching test logic.

**<i>Webhook Testing</i>**

For webhooks, I chose Pipedream because:  
	•	It gives you a public URL immediately  
	•	The event retrieval API is simple  
	•	It’s free and doesn’t require hosting anything  

The webhook test flow is:  
	1.	Send an event to the Pipedream endpoint  
	2.	Poll the API until the event shows up  
	3.	Parse the payload  
	4.	Validate:  
	•	x-request-time exists  
	•	Timestamp is in UTC  
	•	Not older than ~2 minutes  

A Webhook helper takes care of sending, polling, parsing JSON, and checking timestamps.

**Running the Tests**

Install dependencies:
`pip install -r requirements.txt`

Run Test:
`pytest`

Generate allure reports:
`pytest --alluredir=allure-results`

View report:
`allure serve allure-results`

Environment variables you’ll need:  
`BASE_URL=<>`  
`WEBHOOK_POST_URL=<>`  
`WEBHOOK_API_URL=<>`  
`WEBHOOK_API_KEY=<>`  

**Design Choices:**

A few of the decisions behind the setup:  
	•	Using requests.Session keeps HTTP calls lightweight  
	•	A thin API client helps keep test files readable  
	•	External JSON payloads make the tests easier to maintain  
	•	Polling for webhook events keeps the logic simple for this exercise  
	•	Allure reports help visualize the flow, especially for webhooks  

The structure is intentionally minimal so it’s easy to follow, but it can grow if needed.

**Trade-offs**
    •	jsonplaceholder returns 201 even when passing “invalid” data, so I had to write tests based on how their API behaves, not strict REST rules  
	•	The webhook polling is a straightforward loop — in a real system I’d probably use something more robust  
	•	The framework doesn’t include heavy logging or schema validation to keep things simple  

**One Test Design Decision Based on Risk**

The timestamp validation on the webhook is there because timing issues can break distributed systems quickly.
If an event arrives late or isn’t in UTC, downstream services can go out of sync.

The test checks both the presence of x-request-time and that it’s reasonably recent (within ~2 minutes).

