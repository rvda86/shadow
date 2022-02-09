import unittest
import requests
import json
from shadow.db_mysql import db_pool
from shadow import API_LINK

db = db_pool.acquire()

class TestApi(unittest.TestCase):

    api = API_LINK
    users_endpoint = f"{api}/users"
    create_users_endpoint = f"{api}/users/create"
    token_endpoint = f"{api}/users/token"
    entries_endpoint = f"{api}/entries"

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
        
    def test_api_users(self):
        user_1 = {"username": "user_1", "email": "user_1@email.com", "password": "password"}

        #create user
        result = self.create_user(user_1)
        self.assertEqual(200, result.status_code)
        self.assertEqual("account successfully created", result.json()["msg"])

        # try creating a user with taken username and email
        result = self.create_user(user_1)
        self.assertEqual(409, result.status_code)

        # get token
        token = self.get_token({"username": "user_1", "password": "password"})

        # update user
        user_1_update = {"username": "user_2", "email": "user_2@email.com", "password": "password2", "currentPassword": "password"}
        result = self.update_user(user_1_update, token)
        self.assertEqual(200, result.status_code)
        self.assertEqual("account successfully updated", result.json()["msg"])

        # delete user
        result = self.delete_user({"password": "password2"}, token)
        self.assertEqual(200, result.status_code)
        self.assertEqual("account successfully deleted", result.json()["msg"])

        # assert user is deleted / update non-existant user
        result = self.update_user(user_1_update, token)
        self.assertEqual(404, result.status_code)

    def test_api_users_token(self):
        # test with valid credentials
        self.create_user({"username": "user_2", "email": "user_2@email.com", "password": "password"})
        result = self.token_request({"username": "user_2", "password": "password"})
        self.assertEqual(200, result.status_code)
 
        # test with non-existant username
        result = self.token_request({"username": "user_999", "password": "password"})
        self.assertEqual(404, result.status_code)

        # test with invalid password
        result = self.token_request({"username": "user_2", "password": "password999"})
        self.assertEqual(401, result.status_code)

    def test_api_entries(self):
        self.create_user({"username": "user_3", "email": "user_3@email.com", "password": "password"})
        token = self.get_token({"username": "user_3", "password": "password"})

        self.categories(token)
        self.topics(token)
        self.journal_entries(token)
        self.todo_entries(token)

    def categories(self, token):

        # create category
        result = self.create_entry({"type": "category", "name": "category1"}, token)
        self.assertEqual(200, result.status_code)

        # get category_id
        category_id = self.get_categories(token).json()["data"][0]["id"]
     
        # update category
        result = self.update_entry({"type": "category", "name": "cat_1", "id": category_id}, token)
        self.assertEqual(200, result.status_code)

        # delete category
        result = self.delete_entry({"type": "category", "id": category_id}, token)
        self.assertEqual(200, result.status_code)

        # assert category is deleted / update non-existant category
        result = self.update_entry({"type": "category", "name": "cat_1", "id": category_id}, token)
        self.assertEqual(404, result.status_code)

    def topics(self, token):
        self.create_entry({"type": "category", "name": "category1"}, token)
        category_id = self.get_categories(token).json()["data"][0]["id"]

        # create topic (journal)
        result = self.create_entry({"type": "topic", "topic_type": "journal", "name": "topic_1", "category_id": category_id}, token)
        self.assertEqual(200, result.status_code)

        # create topic (todo)
        result = self.create_entry({"type": "topic", "topic_type": "todo", "name": "topic_2", "category_id": category_id}, token)
        self.assertEqual(200, result.status_code)

        # get topic_ids
        categories = self.get_categories(token).json()["data"]
        topic_1_id = categories[0]["topics"][0]["id"]
        topic_2_id = categories[0]["topics"][1]["id"]

        # get a topic
        result = self.get_entry("topic", topic_1_id, token)
        self.assertEqual(200, result.status_code)

        # update topic (journal)
        result = self.update_entry({"type": "topic", "name": "topic_1_update", "id": topic_1_id}, token)
        self.assertEqual(200, result.status_code)

        # update topic (todo)
        result = self.update_entry({"type": "topic", "name": "topic_2_update", "id": topic_1_id}, token)
        self.assertEqual(200, result.status_code)

        # delete topics
        result = self.delete_entry({"type" : "topic", "id": topic_1_id,}, token)
        self.assertEqual(200, result.status_code)
        result = self.delete_entry({"type" : "topic", "id": topic_2_id}, token)
        self.assertEqual(200, result.status_code)

        # assert topics are deleted
        result = self.get_entry("topic", topic_1_id, token)
        self.assertEqual(404, result.status_code)
        result = self.get_entry("topic", topic_2_id, token)
        self.assertEqual(404, result.status_code)

        # delete category
        result = self.delete_entry({"type": "category", "id": category_id}, token)
        self.assertEqual(200, result.status_code)

    def journal_entries(self, token):
        self.create_entry({"type": "category", "name": "category1"}, token)
        category_id = self.get_categories(token).json()["data"][0]["id"]
        self.create_entry({"type": "topic", "topic_type": "journal", "name": "topic_1", "category_id": category_id}, token)
        for category in self.get_categories(token).json()["data"]:
            if category["id"] == category_id:
                topic_id = category["topics"][0]["id"]

        # create entry
        result = self.create_entry({"type": "journal", "title": "My First Post", "content": "This is my first post", "topic_id": topic_id}, token)
        self.assertEqual(200, result.status_code)
    
        # get entry_id
        journal_id = self.get_entry("topic", topic_id, token).json()["data"]["entries"][0]["id"]

        # get entry
        result = self.get_entry("journal", journal_id, token)
        self.assertEqual(200, result.status_code)

        # update entry
        result = self.update_entry({"type": "journal", "title": "My First Updated Post", "content": "This is my first updated content", "id": journal_id}, token)
        self.assertEqual(200, result.status_code)

        # delete entry
        result = self.delete_entry({"type": "journal", "id": journal_id}, token)
        self.assertEqual(200, result.status_code)

        # assert entry is deleted
        result = self.get_entry("journal", journal_id, token)
        self.assertEqual(404, result.status_code)


    def todo_entries(self, token):

        self.create_entry({"type": "category", "name": "category_todo"}, token)
        category_id = self.get_categories(token).json()["data"][1]["id"]
        self.create_entry({"type": "topic", "topic_type": "todo", "name": "topic_todo", "category_id": category_id}, token)
        for category in self.get_categories(token).json()["data"]:
            if category["name"] == "category_todo":
                topic_id = category["topics"][0]["id"]

        # create entry
        result = self.create_entry({"type": "todo", "title": "My First Task", "due_date": "2021-12-01", "topic_id": topic_id}, token)
        self.assertEqual(200, result.status_code)
                                   
        # get entry_id 
        todo_id = self.get_entry("topic", topic_id, token).json()["data"]["entries"][0]["id"]

        # get entry
        result = self.get_entry("todo", todo_id, token)
        self.assertEqual(200, result.status_code)

        # update entry
        result = self.update_entry({"type": "todo", "title": "My First Updated Task", "due_date": "2021-12-01", "completed": "0", "id": todo_id}, token)
        self.assertEqual(200, result.status_code)

        # delete entry 
        result = self.delete_entry({"type": "todo", "id": todo_id}, token)
        self.assertEqual(200, result.status_code)

        # assert entry is deleted
        result = self.get_entry("todo", todo_id, token)
        self.assertEqual(404, result.status_code)   

    def create_user(self, data):
        return requests.post(self.create_users_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json'})
    
    def update_user(self, data, token):
        return requests.put(self.users_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def delete_user(self, data, token):
        return requests.delete(self.users_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def get_token(self, data):
        return requests.post(self.token_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json'}).json()["access_token"]

    def token_request(self, data):
        return requests.post(self.token_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json'})

    def create_entry(self, data, token):
        return requests.post(self.entries_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def update_entry(self, data, token):
        return requests.put(self.entries_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def delete_entry(self, data, token):
        return requests.delete(self.entries_endpoint, data=json.dumps(data), headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def get_categories(self, token):
        return requests.get(f'{self.entries_endpoint}?type=category', headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def get_entry(self, entry_type, id, token):
        return requests.get(f'{self.entries_endpoint}?type={entry_type}&id={id}', headers={'Content-type': 'application/json', 'Authorization': "Bearer " + token})

    def test_validator(self):
        pass
        # user_1 = json.dumps({"username": "user_1", "email": "user_1#email.com", "password": "password"})
        # create_user = requests.post(self.create_users_endpoint, data=user_1, headers=self.json_header)
        # self.assertEqual(422, create_user.status_code)
  
if __name__ == '__main__':
    unittest.main()
