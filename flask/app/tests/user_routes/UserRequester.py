import httpx

from app.config import Config
from app.main import app
from app.tests.utils import get_response_json_status_code


class UserRequester:

    def __init__(self):
        if Config.TEST_CLIENT == "httpx":
            self.client = httpx.Client()
        elif Config.TEST_CLIENT == "flask":
            self.client = app.test_client()
        else:
            raise Exception()

        self.endpoint_user = f"{Config.API_LINK}/users"
        self.endpoint_token = f"{Config.API_LINK}/users/token"

    def create_user(self, email: str, password: str, username: str) -> tuple[dict, int]:
        data = {"email": email, "password": password, "username": username}
        response = self.client.post(self.endpoint_user, json=data,
                                    headers={'Content-type': 'application/json'})
        return get_response_json_status_code(response)

    def delete_user(self, password, token) -> tuple[dict, int]:
        data = {"password": password}
        response = self.client.post(f"{self.endpoint_user}/delete", json=data,
                                    headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def get_token(self, username: str, password: str) -> tuple[dict, int]:
        data = {"username": username, "password": password}
        response = self.client.post(self.endpoint_token, json=data,
                                    headers={"Content-type": "application/json"})
        return get_response_json_status_code(response)

    def get_token_email(self, token: str):
        response = self.client.get(f"{self.endpoint_user}/token-email", headers={'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def get_user(self, token: str):
        response = self.client.get(self.endpoint_user, headers={'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def password_reset(self, new_password: str, token: str) -> tuple[dict, int]:
        data = {"password": new_password}
        response = self.client.post(f"{self.endpoint_user}/reset_password",
                                    json=data,
                                    headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def resend_email_verification_link(self, token: str) -> tuple[dict, int]:
        response = self.client.get(f"{self.endpoint_user}/verify_email_send_link",
                                   headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def send_password_reset_link(self, email: str) -> tuple[dict, int]:
        data = {"email": email}
        response = self.client.post(f"{self.endpoint_user}/reset_password_send_link", json=data,
                                    headers={"Content-type": "application/json"})
        return get_response_json_status_code(response)

    def update_user(self, currentPassword: str, email: str, password: str, username: str, token: str) -> tuple[
        dict, int]:
        data = {"currentPassword": currentPassword, "email": email, "password": password, "username": username}
        response = self.client.put(self.endpoint_user, json=data,
                                   headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def verify_email(self, token: str) -> tuple[dict, int]:
        response = self.client.post(f"{self.endpoint_user}/verify_email",
                                    headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)
