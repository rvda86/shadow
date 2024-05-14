import unittest

from shadow.db_mysql import db_pool
from shadow.config import Config
from shadow.tests.user_routes.UserRequester import UserRequester


# /api/user POST
class TestCreateUser(unittest.TestCase):

    db = db_pool.acquire()
    api = Config.API_LINK
    endpoint_user = f"{api}/users"
    endpoint_token = f"{api}/users/token"
    requester = UserRequester(endpoint_user, endpoint_token)

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.username = "user1"
        self.email = "user1@example.com"
        self.password = "passwSf2@ord"

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        data = {"username": self.username, "email": self.email, "password": self.password}
        data, status_code = self.requester.create_user(data)

        self.assertEqual(200, status_code)

        # self.assertEqual(self.username, data["data"]["username"])
        # self.assertEqual(self.email, data["data"]["email"])


if __name__ == "__main__":
    unittest.main()
