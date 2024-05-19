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

    def delete_user(self, password, token) -> tuple[dict, int]:
        data = {"password": password}
        response = self.client.request("DELETE", self.endpoint_user, content=json.dumps(data),
                                       headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return response.json(), response.status_code

    def get_token(self, username: str, password: str) -> tuple[dict, int]:
        data = {"username": username, "password": password}
        response = self.client.post(self.endpoint_token, content=json.dumps(data),
                                    headers={"Content-type": "application/json"})
        return response.json(), response.status_code

    def get_token_email(self, token: str):
        response = self.client.get(f"{self.endpoint_user}/token-email", headers={'Authorization': "Bearer " + token})
        return response.json(), response.status_code

    def get_user(self, token: str):
        response = self.client.get(self.endpoint_user, headers={'Authorization': "Bearer " + token})
        return response.json(), response.status_code

    def password_reset(self, new_password: str, token: str) -> tuple[dict, int]:
        data = {"password": new_password}
        response = self.client.post(f"{self.endpoint_user}/reset_password",
                                    content=json.dumps(data),
                                    headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return response.json(), response.status_code

    def resend_email_verification_link(self, token: str) -> tuple[dict, int]:
        response = self.client.get(f"{self.endpoint_user}/verify_email_send_link",
                                   headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return response.json(), response.status_code

    def send_password_reset_link(self, email: str) -> tuple[dict, int]:
        data = {"email": email}
        response = self.client.post(f"{self.endpoint_user}/reset_password_send_link", content=json.dumps(data),
                                    headers={"Content-type": "application/json"})
        return response.json(), response.status_code

    def update_user(self, currentPassword: str, email: str, password: str, username: str, token: str) -> tuple[
        dict, int]:
        data = {"currentPassword": currentPassword, "email": email, "password": password, "username": username}
        response = self.client.put(self.endpoint_user, content=json.dumps(data),
                                   headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})
        return response.json(), response.status_code

    def verify_email(self, token: str) -> tuple[dict, int]:
        response = self.client.post(f"{self.endpoint_user}/verify_email",
                                    headers={"Content-type": "application/json", 'Authorization': "Bearer " + token})
        return response.json(), response.status_code
