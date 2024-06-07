import unittest

from app.db_mysql import db_pool
from app.tests.entry_routes.EntryRequester import EntryRequester
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /api/entry/journal POST
class TestCreateJournal(unittest.TestCase):

    db = db_pool.acquire()
    user_requester = UserRequester()
    requester = EntryRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.token_1, _ = create_user(self.user_requester, "user1@example.com", "passwSf2@ord", "user1")
        self.category, _ = self.requester.create_entry({"name": "category1"}, "category", self.token_1)
        self.topic, _ = self.requester.create_entry({"topic_type": "journal", "name": "topic_1",
                                                     "category_id": self.category["entry"]["id"]}, "topic", self.token_1)

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        data = {"title": "My First Post", "content": "This is my first post",
                "topic_id": self.topic["entry"]["id"]}

        data, status_code = self.requester.create_entry(data, "journal", self.token_1)
        self.assertEqual(200, status_code)

    def test_missing_field(self):
        data = {"title": "My First Post", "topic_id": self.topic["entry"]["id"]}

        data, status_code = self.requester.create_entry(data, "journal", self.token_1)
        self.assertEqual(422, status_code)

    def test_extra_field(self):
        data = {"title": "My First Post", "content": "This is my first post",
                "topic_id": self.topic["entry"]["id"], "city": "oslo"}

        data, status_code = self.requester.create_entry(data, "journal", self.token_1)
        self.assertEqual(422, status_code)

    def test_unexpected_field(self):
        data = {"title": "My First Post", "text": "This is my first post",
                "topic_id": self.topic["entry"]["id"]}

        data, status_code = self.requester.create_entry(data, "journal", self.token_1)
        self.assertEqual(422, status_code)


if __name__ == "__main__":
    unittest.main()
