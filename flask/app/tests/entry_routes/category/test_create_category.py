import unittest

from app.db_mysql import db_pool
from app.tests.entry_routes.EntryRequester import EntryRequester
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /api/entries POST
class TestCreateCategory(unittest.TestCase):

    db = db_pool.acquire()
    user_requester = UserRequester()
    requester = EntryRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.token_1, _ = create_user(self.user_requester, "user1@example.com", "passwSf2@ord", "user1")
        self.token_2, _ = create_user(self.user_requester, "user2@example.com", "passwSf2@ord", "user2")

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        data = {"type": "category", "name": "category1"}
        data, status_code = self.requester.create_entry(data, self.token_1)

        self.assertEqual(200, status_code)


if __name__ == "__main__":
    unittest.main()
