import os
import pytest
import allure
from utils.util_api import BaseAPI
from utils.testData_loader import load_json_data

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

@pytest.fixture(scope="module")
def initiate_url():
    with allure.step(f"Initialize API client with base URL: {BASE_URL}"):
        return BaseAPI(base_url=BASE_URL)

@allure.feature("API Workflow")
@allure.story("Create employee")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_employee(initiate_url):
    payload_data = load_json_data("data_post.json")

    with allure.step("Send POST request to /posts"):
        post_response = initiate_url.post_request("/posts", json=payload_data)
        assert post_response.status_code == 201

    with allure.step("Validate POST response fields"):
        response_body = post_response.json()
        assert response_body["username"] == payload_data["username"]

@allure.feature("API Workflow")
@allure.story("Get employee")
@allure.severity(allure.severity_level.NORMAL)
def test_get_employee(initiate_url):
    with allure.step("Send GET request with params userId=1"):
        get_response = initiate_url.get_request("/posts", "userId=1")
        assert get_response.status_code == 200

    with allure.step("Validate GET response fields"):
        response_body = get_response.json()
        assert response_body[0]["userId"] == 1

@allure.feature("API Workflow")
@allure.story("Delete employee")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_employee(initiate_url):
    with allure.step("Send DELETE request to /posts/1"):
        delete_response = initiate_url.delete_request("/posts/1")
        assert delete_response.status_code == 200


@allure.feature("Negative API Cases")
@allure.story("Invalid POST payload")
@allure.severity(allure.severity_level.MINOR)
def test_create_employee_invalid(initiate_url):
    payload_data = load_json_data("invalid_data.json")

    with allure.step("Send POST request with invalid payload"):
        post_response = initiate_url.post_request("/posts", json=payload_data)
        assert post_response.status_code == 201

    with allure.step("Validate returned fields match payload"):
        response_body = post_response.json()
        assert response_body["username"] == payload_data["username"]

@allure.feature("Negative API Cases")
@allure.story("Invalid GET path")
def test_invalid_get_employee(initiate_url):
    with allure.step("Send GET request to invalid endpoint /post"):
        invalid_response = initiate_url.get_request("/post", "user=999999999")
        assert invalid_response.status_code == 404

@allure.feature("Negative API Cases")
@allure.story("Invalid DELETE")
def test_invalid_delete_employee(initiate_url):
    with allure.step("Send DELETE request using invalid ID"):
        delete_response = initiate_url.delete_request("/posts/KAR")

    with allure.step("Validate status code (expected behavior of test server)"):
        assert delete_response.status_code in (200, 202)