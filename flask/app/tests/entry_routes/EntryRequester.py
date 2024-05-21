import httpx

from app.config import Config
from app.main import app
from app.tests.utils import get_response_json_status_code


class EntryRequester:

    def __init__(self):
        if Config.TEST_CLIENT == "httpx":
            self.client = httpx.Client()
        elif Config.TEST_CLIENT == "flask":
            self.client = app.test_client()
        else:
            raise Exception()

        self.endpoint_entry = f"{Config.API_LINK}/entries"

    def create_entry(self, data, token):
        response = self.client.post(self.endpoint_entry, json=data, headers={'Content-type': 'application/json',
                                                                             'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def delete_entry(self, data, token):
        response = self.client.delete(self.endpoint_entry, json=data, headers={'Content-type': 'application/json',
                                                                               'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def get_entry(self, entry_type, entry_id, token):
        response = self.client.get(f'{self.endpoint_entry}?type={entry_type}&id={entry_id}',
                                   headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)

    def update_entry(self, data, token):
        response = self.client.put(self.endpoint_entry, json=data, headers={'Content-type': 'application/json',
                                                                            'Authorization': "Bearer " + token})
        return get_response_json_status_code(response)