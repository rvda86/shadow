import unittest

from app.config import Config
from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.user_routes.UserRequester import UserRequester


# /api/users/token POST
class TestGetToken(unittest.TestCase):

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
        self.requester.create_user(self.email, self.password, self.username)

        data, status_code = self.requester.get_token(self.username, self.password)
        self.assertEqual(200, status_code)

    def test_no_user_found(self):
        username = "idontexist"
        data, status_code = self.requester.get_token(username, self.password)

        self.assertEqual(404, status_code)
        self.assertEqual(ExceptionMessages.USER_NOT_FOUND, data["msg"])

    def test_wrong_password(self):
        self.requester.create_user(self.email, self.password, self.username)

        password = "wrong_password"
        data, status_code = self.requester.get_token(self.username, password)

        self.assertEqual(401, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_WRONG, data["msg"])


if __name__ == "__main__":
    unittest.main()
