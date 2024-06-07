import httpx

from app.config import Config
from app.main import app
from app.tests.utils import get_json_and_response_code_from_response


class EntryRequester:

    def __init__(self):
        if Config.TEST_CLIENT == "httpx":
            self.client = httpx.Client()
        elif Config.TEST_CLIENT == "flask":
            self.client = app.test_client()
        else:
            raise Exception()

        self.endpoint_category = f"{Config.API_LINK}/entry/category"
        self.endpoint_habit = f"{Config.API_LINK}/entry/habit"
        self.endpoint_journal = f"{Config.API_LINK}/entry/journal"
        self.endpoint_todo = f"{Config.API_LINK}/entry/todo"
        self.endpoint_topic = f"{Config.API_LINK}/entry/topic"

        self.endpoints = {"category": self.endpoint_category,
                          "habit": self.endpoint_habit,
                          "journal": self.endpoint_journal,
                          "todo": self.endpoint_todo,
                          "topic": self.endpoint_topic}

    def create_entry(self, data, endpoint, token):
        response = self.client.post(self.endpoints[endpoint], json=data, headers={'Content-type': 'application/json',
                                                                                  'Authorization': "Bearer " + token})
        return get_json_and_response_code_from_response(response)

    def delete_entry(self, endpoint, entry_id, token):
        response = self.client.delete(f'{self.endpoints[endpoint]}?id={entry_id}',
                                      headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})
        return get_json_and_response_code_from_response(response)

    def get_entry(self, endpoint, entry_id, token):
        response = self.client.get(f'{self.endpoints[endpoint]}?id={entry_id}',
                                   headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})
        return get_json_and_response_code_from_response(response)

    def update_entry(self, data, endpoint, token):
        response = self.client.put(self.endpoints[endpoint], json=data, headers={'Content-type': 'application/json',
                                                                                 'Authorization': "Bearer " + token})
        return get_json_and_response_code_from_response(response)
