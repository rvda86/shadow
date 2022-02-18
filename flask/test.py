import unittest
import requests
import json
from shadow.db_mysql import db_pool
from shadow import API_LINK

db = db_pool.acquire()

class TestApi(unittest.TestCase):

    api = API_LINK
    users_endpoint = f"{api}/users"
    token_endpoint = f"{api}/users/token"
    check_availability_endpoint = f"{api}/users/check_availability"

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
        
    def test_users(self):

        username = "user_1"
        new_username = "donald"
        password = "password"
        email = "user_1@email.com"
        new_email = "user_1@hotmail.com"
        wrong_password = "pa$$w0rd"
        invalid_email = "user_1email.com"
        invalid_password = "passwor"
        new_password = "password2"

        self.success_create_user({"username": username, "email": email, "password": password})
        self.fail_create_user_duplicate({"username": username, "email": email, "password": password})
        self.fail_create_user_invalid_data({"username": username, "email": invalid_email, "password": password})
        self.fail_create_user_invalid_data({"username": username, "email": email, "password": invalid_password})
        self.success_get_token({"username": username, "password": password})
        self.fail_get_token_unknown_user({"username": "user_2", "password": "password"})
        self.fail_get_token_wrong_password({"username": username, "password": wrong_password} )
        token = self.get_token({"username": username, "password": password}).json()["access_token"]
        self.success_get_user(token)
        self.success_update_user(token, {"username": username, "email": email, "password": new_password, "currentPassword": password})
        self.success_update_user(token, {"username": username, "email": new_email, "password": new_password, "currentPassword": new_password})
        self.success_update_user(token, {"username": new_username, "email": new_email, "password": new_password, "currentPassword": new_password})
        self.confirm_success_update_username_email(token, {"username": new_username, "email": new_email})
        self.success_check_username_available({"username": "user_2", "email": "new@email.com"})
        self.fail_check_username_available({"username": new_username, "email": new_email})
        self.success_check_email_available({"username": "user_2", "email": "new@email.com"})
        self.fail_check_email_available({"username": new_username, "email": new_email})
        self.success_get_token({"username": new_username, "password": new_password})
        self.fail_delete_user_wrong_password(token, {"password": wrong_password})
        self.success_delete_user(token, {"password": new_password} )
        self.fail_delete_user_unknown_user(token, {"password": new_password} )

    def success_create_user(self, data):
        response = self.create_user(data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("account successfully created", response.json()["msg"])

    def fail_create_user_duplicate(self, data):
        response = self.create_user(data)
        self.assertEqual(409, response.status_code)
    
    def fail_create_user_invalid_data(self, data):
        response = self.create_user(data)
        self.assertEqual(422, response.status_code)

    def success_get_token(self, data):
        response = self.get_token(data)
        self.assertEqual(200, response.status_code)

    def fail_get_token_unknown_user(self, data):
        response = self.get_token(data)
        self.assertEqual(404, response.status_code)

    def fail_get_token_wrong_password(self, data):
        response = self.get_token(data)
        self.assertEqual(401, response.status_code)

    def success_get_user(self, token):
        response = self.get_user(token)
        self.assertEqual(200, response.status_code)
    
    def success_update_user(self, token, data):
        response = self.update_user(data, token)
        self.assertEqual(200, response.status_code)
        self.assertEqual("account successfully updated", response.json()["msg"])

    def confirm_success_update_username_email(self, token, data):
        response = self.get_user(token).json()
        self.assertEqual(data, response)

    def success_delete_user(self, token, data):
        response = self.delete_user(data, token)
        self.assertEqual(200, response.status_code)
        self.assertEqual("account successfully deleted", response.json()["msg"])

    def fail_delete_user_unknown_user(self, token, data):
        response = self.delete_user(data, token)
        self.assertEqual(404, response.status_code)

    def fail_delete_user_wrong_password(self, token, data):
        response = self.delete_user(data, token)
        self.assertEqual(401, response.status_code)

    def success_check_username_available(self, data):
        response = self.check_availability(data)
        self.assertEqual(True, response.json()["username"])

    def fail_check_username_available(self, data):
        response = self.check_availability(data)
        self.assertEqual(False, response.json()["username"])

    def success_check_email_available(self, data):
        response = self.check_availability(data)
        self.assertEqual(True, response.json()["email"])

    def fail_check_email_available(self, data):
        response = self.check_availability(data)
        self.assertEqual(False, response.json()["email"])

    def check_availability(self, data):
        return requests.post(self.check_availability_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json'})

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
        id = self.success_create_entry({"type": "todo", "task": "My First Task", "due_date": "2021-12-01", "topic_id": topic_id}, token1)
        
        data = { 
            "entry_type": "todo",
            "update": {"type": "todo", "task": "My First Updated Task", "due_date": "2021-12-01", "completed": "0", "id": id},
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
            "update": {"type": "habit", "name": "My First Updated Habit", "days_completed": ["2022-03-12", "2022-03-13"], "id": id},
            "delete": {"type": "habit", "id": id}
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
        self.create_user({"username": "user_1", "email": "user_1@email.com", "password": "password"})
        token1 = self.get_token({"username": "user_1", "password": "password"}).json()["access_token"]
        self.create_user({"username": "user_2", "email": "user_2@email.com", "password": "password"})
        token2 = self.get_token({"username": "user_2", "password": "password"}).json()["access_token"]
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
        self.assertEqual("Resource not found", response.json()["msg"])    

    def fail_get_entry_unknown_entry(self, entry_type, id, token):
        response = self.get_entry(entry_type, id, token)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Resource not found", response.json()["msg"])

    def success_update_entry(self, data, token):
        response = self.update_entry(data, token)
        self.assertEqual(200, response.status_code)

    def fail_update_entry_wrong_user(self, data, token):
        response = self.update_entry(data, token)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Resource not found", response.json()["msg"])

    def fail_delete_entry_wrong_user(self, data, token):
        response = self.delete_entry(data, token)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Resource not found", response.json()["msg"])

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
