import os
import requests
import allure

class BaseAPI:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv("BASE_URL")
        if not self.base_url:
            raise ValueError("Missing base url")

        self.session = requests.Session()

    def _join_url(self, path):
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    @allure.step("GET request to: {path}")
    def get_request(self, path, params=None, header=None):
        url = self._join_url(path)
        return self.session.get(url, params=params, headers=header)

    @allure.step("POST request to: {path}")
    def post_request(self, path, json=None):
        url = self._join_url(path)
        return self.session.post(url, json=json)

    @allure.step("DELETE request to: {path}")
    def delete_request(self, path):
        url = self._join_url(path)
        return self.session.delete(url)