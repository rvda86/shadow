import unittest

from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.entry_routes.EntryRequester import EntryRequester
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester
from app.utils.utils import uuid_generator


# /api/entry/category GET
class TestGetCategory(unittest.TestCase):

    db = db_pool.acquire()
    user_requester = UserRequester()
    requester = EntryRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.token_1, _ = create_user(self.user_requester, "user1@example.com", "passwSf2@ord", "user1")
        self.token_2, _ = create_user(self.user_requester, "user2@example.com", "passwSf2@ord", "user2")
        self.category, _ = self.requester.create_entry({"name": "category1"}, "category", self.token_1)

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        data, status_code = self.requester.get_entry("category", self.category["entry"]["id"], self.token_1)
        self.assertEqual(200, status_code)

    def test_combination_category_author_unknown(self):
        data, status_code = self.requester.get_entry("category", self.category["entry"]["id"], self.token_2)
        self.assertEqual(404, status_code)

    def test_category_does_not_exist(self):
        category_id = uuid_generator()
        data, status_code = self.requester.get_entry("category", category_id, self.token_1)
        self.assertEqual(404, status_code)

    def test_invalid_id(self):
        invalid_id = "invalidID"
        data, status_code = self.requester.get_entry("category", invalid_id, self.token_1)
        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.ID_NOT_VALID, data["msg"])


if __name__ == "__main__":
    unittest.main()
