import httpx

from app.config import Config
from app.main import app
from app.tests.utils import get_json_and_response_code_from_response


class Requester:

    def __init__(self):
        if Config.TEST_CLIENT == "httpx":
            self.client = httpx.Client()
        elif Config.TEST_CLIENT == "flask":
            self.client = app.test_client()
        else:
            raise Exception()

        self.endpoint_password_reset = f"{Config.API_LINK}/users/reset_password"
        self.endpoint_password_reset_request = f"{Config.API_LINK}/users/reset_password_send_link"
        self.endpoint_user = f"{Config.API_LINK}/users"
        self.endpoint_token = f"{Config.API_LINK}/users/token"

        self.endpoints = {"password_reset": self.endpoint_password_reset,
                          "password_reset_request": self.endpoint_password_reset_request,
                          "user": self.endpoint_user,
                          "token": self.endpoint_token}

    def post_request(self, data: dict, endpoint: str, token: str = None) -> tuple[dict, int]:
        headers = {'Content-type': 'application/json'} if token is None else {"Content-type": "application/json",
                                                                              'Authorization': "Bearer " + token}
        response = self.client.post(self.endpoints[endpoint], json=data, headers=headers)
        return get_json_and_response_code_from_response(response)

    def put_request(self, data: dict, endpoint: str, token: str = None) -> tuple[dict, int]:
        headers = {'Content-type': 'application/json'} if token is None else {"Content-type": "application/json",
                                                                              'Authorization': "Bearer " + token}
        response = self.client.put(self.endpoints[endpoint], json=data, headers=headers)
        return get_json_and_response_code_from_response(response)
