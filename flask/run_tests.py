import json
import unittest
import requests

from app.db_mysql import db_pool
from app.config import Config

from app.tests.entry_routes.category.test_create_category import TestCreateCategory
from app.tests.entry_routes.category.test_get_category import TestGetCategory
from app.tests.entry_routes.habit.test_create_habit import TestCreateHabit
from app.tests.entry_routes.journal.test_create_journal import TestCreateJournal
from app.tests.entry_routes.todo.test_create_todo import TestCreateToDo
from app.tests.entry_routes.topic.test_create_topic import TestCreateTopic
# from app.tests.user_routes.test_create_user import TestCreateUser
# from app.tests.user_routes.test_delete_user import TestDeleteUser
# from app.tests.user_routes.test_email_verification import TestEmailVerification
# from app.tests.user_routes.test_get_token import TestGetToken
# from app.tests.user_routes.test_get_user import TestGetUser
# from app.tests.user_routes.test_password_reset import TestPasswordReset
# from app.tests.user_routes.test_update_password import TestUpdatePassword
# from app.tests.user_routes.test_update_user import TestUpdateUser

db = db_pool.acquire()


class TestApi(unittest.TestCase):

    api = Config.API_LINK
    users_endpoint = f"{api}/users"
    token_endpoint = f"{api}/users/token"

    entries_endpoint = f"{api}/entries"
    data_endpoint = f"{api}/data"

    @classmethod 
    def setUpClass(cls):
        if db.name != "shadow_testing":
            raise Exception

    @classmethod 
    def tearDownClass(cls):
        db.reset_database()

    def setUp(self):
        pass

    def tearDown(self):
        db.reset_database()

    def create_user(self, data):
        return requests.post(self.users_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json'})

    def update_user(self, data, token):
        return requests.put(self.users_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def get_user(self, token):
        return requests.get(self.users_endpoint, headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def delete_user(self, data, token):
        return requests.delete(self.users_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def get_token(self, data):
        return requests.post(self.token_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json'})

    def test_categories(self):
        token1, token2 = self.set_up_tokens()
        id = self.success_create_entry({"type": "category", "name": "category1"}, token1)

        data = {
            "entry_type": "category",
            "update": {"type": "category", "name": "cat_1", "id": id},
            "delete": {"type": "category", "id": id}
            }

        self.run_test_cases(data, id, token1, token2)

    def test_topics(self):
        token1, token2 = self.set_up_tokens()
        category_id = self.set_up_category_id(token1)
        id = self.success_create_entry({"type": "topic", "topic_type": "journal", "name": "topic_1", "category_id": category_id}, token1)
        self.success_create_entry({"type": "topic", "topic_type": "todo", "name": "topic_1", "category_id": category_id}, token1)
        self.success_create_entry({"type": "topic", "topic_type": "habit", "name": "topic_1", "category_id": category_id}, token1)

        data = {
            "entry_type": "topic",
            "update": {"type": "topic", "name": "top_1", "id": id},
            "delete": {"type": "topic", "id": id}
            }

        self.run_test_cases(data, id, token1, token2)

    def test_journal(self):
        token1, token2 = self.set_up_tokens()
        category_id = self.set_up_category_id(token1)
        topic_id = self.set_up_topic_id("journal", category_id, token1)
        id = self.success_create_entry({"type": "journal", "title": "My First Post", "content": "This is my first post", "topic_id": topic_id}, token1)

        data = {
            "entry_type": "journal",
            "update": {"type": "journal", "title": "My First Updated Post", "content": "This is my first updated content", "id": id},
            "delete": {"type": "journal", "id": id}
            }

        self.run_test_cases(data, id, token1, token2)

    def test_todo(self):
        token1, token2 = self.set_up_tokens()
        category_id = self.set_up_category_id(token1)
        topic_id = self.set_up_topic_id("todo", category_id, token1)
        id = self.success_create_entry({"type": "todo", "task": "My First Task", "topic_id": topic_id}, token1)

        data = {
            "entry_type": "todo",
            "update": {"type": "todo", "task": "My First Updated Task", "completed": "0", "id": id},
            "delete": {"type": "todo", "id": id}
            }

        self.run_test_cases(data, id, token1, token2)

    def test_habit(self):
        token1, token2 = self.set_up_tokens()
        category_id = self.set_up_category_id(token1)
        topic_id = self.set_up_topic_id("habit", category_id, token1)
        id = self.success_create_entry({"type": "habit", "name": "My First Habit", "topic_id": topic_id}, token1)
        data = {
            "entry_type": "habit",
            "update": {"type": "habit", \
                        "name": "My First Updated Habit",
                        "days": [ { "completed": 0, "date": "Mon-15/08/2022" },
                                { "completed": 1, "date": "Tue-16/08/2022" },
                                { "completed": 0, "date": "Wed-17/08/2022" },
                                { "completed": 1, "date": "Thu-18/08/2022" },
                                { "completed": 0, "date": "Fri-19/08/2022" },],
                        "id": id},
            "delete": {"type": "habit", "id": id}
            }

        self.run_test_cases(data, id, token1, token2)

    def test_tag(self):
        token1, token2 = self.set_up_tokens()
        id = self.success_create_entry({"type": "tag", "name": "tag1"}, token1)
        data = {
            "entry_type": "tag",
            "update": {"type": "tag", "name": "tag2", "id": id},
            "delete": {"type": "tag", "id": id}
            }

        self.run_test_cases(data, id, token1, token2)

    def run_test_cases(self, data, id, token1, token2):
        self.success_get_entry(data["entry_type"], id, token1)
        self.fail_get_entry_wrong_user(data["entry_type"], id, token2)
        self.success_update_entry(data["update"], token1)
        self.fail_update_entry_wrong_user(data["update"], token2)
        self.fail_delete_entry_wrong_user(data["delete"], token2)
        self.success_delete_entry(data["delete"], token1)
        self.fail_get_entry_unknown_entry(data["entry_type"], id, token1)

    def set_up_tokens(self):
        self.create_user({"username": "user1", "email": "user_1@email.com", "password": "password1234"})
        token1 = self.get_token({"username": "user1", "password": "password1234"}).json()["access_token"]
        self.create_user({"username": "user2", "email": "user_2@email.com", "password": "password1234"})
        token2 = self.get_token({"username": "user2", "password": "password1234"}).json()["access_token"]
        return token1, token2

    def set_up_category_id(self, token):
        response = self.create_entry({"type": "category", "name": "category1"}, token)
        return response.json()["entry"]["id"]

    def set_up_topic_id(self, type, category_id, token):
        response = self.create_entry({"type": "topic", "topic_type": type, "name": "topic_1", "category_id": category_id}, token)
        return response.json()["entry"]["id"]

    def success_create_entry(self, data, token):
        response = self.create_entry(data, token)
        self.assertEqual(200, response.status_code)
        return response.json()["entry"]["id"]

    def success_get_entry(self, entry_type, id, token):
        response = self.get_entry(entry_type, id, token)
        self.assertEqual(200, response.status_code)

    def fail_get_entry_wrong_user(self, entry_type, id, token):
        response = self.get_entry(entry_type, id, token)
        self.assertEqual(404, response.status_code)

    def fail_get_entry_unknown_entry(self, entry_type, id, token):
        response = self.get_entry(entry_type, id, token)
        self.assertEqual(404, response.status_code)

    def success_update_entry(self, data, token):
        response = self.update_entry(data, token)
        self.assertEqual(200, response.status_code)

    def fail_update_entry_wrong_user(self, data, token):
        response = self.update_entry(data, token)
        self.assertEqual(404, response.status_code)

    def fail_delete_entry_wrong_user(self, data, token):
        response = self.delete_entry(data, token)
        self.assertEqual(404, response.status_code)

    def success_delete_entry(self, data, token):
        response = self.delete_entry(data, token)
        self.assertEqual(200, response.status_code)

    def get_data(self, token):
        return requests.get(self.data_endpoint, headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def create_entry(self, data, token):
        return requests.post(self.entries_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def update_entry(self, data, token):
        return requests.put(self.entries_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def delete_entry(self, data, token):
        return requests.delete(self.entries_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def get_entry(self, entry_type, id, token):
        return requests.get(f'{self.entries_endpoint}?type={entry_type}&id={id}', headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})


if __name__ == '__main__':
    unittest.main()
