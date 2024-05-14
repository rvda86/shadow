import httpx
import json


class UserRequester:

    def __init__(self, endpoint_user: str, endpoint_token: str):
        self.client = httpx.Client()
        self.endpoint_user = endpoint_user
        self.endpoint_token = endpoint_token

    def create_user(self, email: str, password: str, username: str) -> tuple[dict, int]:
        data = {"email": email, "password": password, "username": username}
        response = self.client.post(self.endpoint_user, content=json.dumps(data),
                                    headers={'Content-type': 'application/json'})
        return response.json(), response.status_code
