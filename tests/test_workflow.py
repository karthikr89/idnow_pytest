import os
import pytest
from utils.util_api import BaseAPI
from utils.testData_loader import load_json_data

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

@pytest.fixture(scope="module") #define scope of the function
def initiate_url():
    return BaseAPI(base_url=BASE_URL)

def test_create_employee(initiate_url):
    payload_data = load_json_data("data_post.json") #load data from data directory
    post_response = initiate_url.post_request("/posts", json=payload_data)
    assert post_response.status_code == 201
    response_body = post_response.json()
    assert response_body["username"] == payload_data["username"]

def test_get_employee(initiate_url):
    get_response = initiate_url.get_request("/posts", "userId=1")
    assert get_response.status_code == 200
    response_body = get_response.json()
    assert response_body[0]["userId"] == 1

def test_delete_employee(initiate_url):
    delete_response = initiate_url.delete_request("/posts/1")
    assert delete_response.status_code == 200

#validation for negative assertion in POST
def test_create_employee_invalid(initiate_url):
    payload_data = load_json_data("invalid_data.json") #load data from data directory
    post_response = initiate_url.post_request("/posts", json=payload_data)
    assert post_response.status_code == 201
    response_body = post_response.json()
    assert response_body["username"] == payload_data["username"]

#to test invalid path
def test_invalid_get_employee(initiate_url):
    invalid_get_response = initiate_url.get_request("/post", "user=999999999")
    assert invalid_get_response.status_code == 404

#to test invalid assertions
def test_invalid_delete_employee(initiate_url):
    delete_response = initiate_url.delete_request("/posts/KAR")
    assert delete_response.status_code == 202