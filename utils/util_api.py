import os
import requests

class BaseAPI:
    def __init__(self, base_url: str | None = None):
            self.base_url = base_url or os.getenv("BASE_URL")
            if not self.base_url:
                raise ValueError("Missing base url")
            self.session = requests.Session() #gives persistent connection

    def _join_url(self, path):
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get_request(self, path, params=None):
        return self.session.get(self._join_url(path), params=params)

    def post_request(self, path, json=None):
        return self.session.post(self._join_url(path), json=json)

    def delete_request(self, path):
        return self.session.delete(self._join_url(path))