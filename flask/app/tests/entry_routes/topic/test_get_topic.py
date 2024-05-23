import unittest

from app.db_mysql import db_pool
from app.tests.entry_routes.EntryRequester import EntryRequester
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester
from app.utils.utils import uuid_generator


# /api/entries GET
class TestGetTopic(unittest.TestCase):

    db = db_pool.acquire()
    user_requester = UserRequester()
    requester = EntryRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.token_1, _ = create_user(self.user_requester, "user1@example.com", "passwSf2@ord", "user1")
        self.token_2, _ = create_user(self.user_requester, "user2@example.com", "passwSf2@ord", "user2")
        self.category, _ = self.requester.create_entry({"type": "category", "name": "category1"}, self.token_1)
        self.topic, _ = self.requester.create_entry({"type": "topic", "topic_type": "journal", "name": "topic_1",
                                                     "category_id": self.category["entry"]["id"]}, self.token_1)

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        data, status_code = self.requester.get_entry("topic", self.topic["entry"]["id"], self.token_1)
        self.assertEqual(200, status_code)

    def test_combination_category_author_unknown(self):
        data, status_code = self.requester.get_entry("topic", self.category["entry"]["id"], self.token_2)
        self.assertEqual(404, status_code)

    def test_category_does_not_exist(self):
        topic_id = uuid_generator()
        data, status_code = self.requester.get_entry("topic", topic_id, self.token_1)
        self.assertEqual(404, status_code)


if __name__ == "__main__":
    unittest.main()
