import unittest

from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.entry_routes.EntryRequester import EntryRequester
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester
from app.utils.utils import uuid_generator


# /api/entry/topic GET
class TestGetTopic(unittest.TestCase):

    db = db_pool.acquire()
    user_requester = UserRequester()
    requester = EntryRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.token_1, _ = create_user(self.user_requester, "user1@example.com", "passwSf2@ord", "user1")
        self.token_2, _ = create_user(self.user_requester, "user2@example.com", "passwSf2@ord", "user2")
        self.category, _ = self.requester.create_entry({"name": "category1"}, "category", self.token_1)
        self.topic, _ = self.requester.create_entry({"topic_type": "journal", "name": "topic_1",
                                                     "category_id": self.category["entry"]["id"]}, "topic", self.token_1)

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        data, status_code = self.requester.get_entry("topic", self.topic["entry"]["id"], self.token_1)
        self.assertEqual(200, status_code)

    def test_combination_topic_author_unknown(self):
        data, status_code = self.requester.get_entry("topic", self.topic["entry"]["id"], self.token_2)
        self.assertEqual(404, status_code)

    def test_topic_does_not_exist(self):
        topic_id = uuid_generator()
        data, status_code = self.requester.get_entry("topic", topic_id, self.token_1)
        self.assertEqual(404, status_code)

    def test_invalid_id(self):
        invalid_id = "invalidID"
        data, status_code = self.requester.get_entry("topic", invalid_id, self.token_1)
        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.ID_NOT_VALID, data["msg"])


if __name__ == "__main__":
    unittest.main()
