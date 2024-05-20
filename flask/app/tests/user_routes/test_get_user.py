import unittest

from app.config import Config
from app.db_mysql import db_pool
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /api/users GET
class TestGetUser(unittest.TestCase):
    db = db_pool.acquire()
    api = Config.API_LINK
    endpoint_user = f"{api}/users"
    endpoint_token = f"{api}/users/token"
    requester = UserRequester(endpoint_user, endpoint_token)

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.email = "user1@example.com"
        self.username = "user1"
        self.password = "passwSf2@ord"
        self.token, self.user_data = create_user(self.requester, self.email, self.password, self.username)

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        data, status_code = self.requester.get_user(self.token)

        self.assertEqual(200, status_code)
        self.assertEqual(self.username, data["username"])
        self.assertEqual(self.email, data["email"])

    def test_invalid_token(self):
        token = "i_am_an_invalid_token"
        data, status_code = self.requester.get_user(token)
        self.assertEqual(422, status_code)


if __name__ == "__main__":
    unittest.main()
