import unittest

from app.config import Config
from app.constants.ControllerMessages import ControllerMessages
from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.user_routes.UserRequester import UserRequester


# /api/users POST
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
        data, status_code = self.requester.create_user(self.email, self.password, self.username)

        self.assertEqual(200, status_code)
        self.assertEqual(ControllerMessages.ACCOUNT_CREATED, data["msg"])
        self.assertEqual(self.username, data["data"]["username"])
        self.assertEqual(self.email, data["data"]["email"])

    def test_password_entirely_numeric(self):
        password = "1234567891234"
        data, status_code = self.requester.create_user(self.email, password, self.username)
        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_NUMERIC, data["msg"])

    def test_password_too_common(self):
        password = "password"
        data, status_code = self.requester.create_user(self.email, password, self.username)

        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_TOO_COMMON, data["msg"])

    def test_password_too_long(self):
        password = "a"*129
        data, status_code = self.requester.create_user(self.email, password, self.username)

        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_TOO_LONG, data["msg"])

    def test_password_too_short(self):
        password = "shortpw"
        data, status_code = self.requester.create_user(self.email, password, self.username)

        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_TOO_SHORT, data["msg"])

    def test_username_already_exists(self):
        self.requester.create_user(self.email, self.password, self.username)
        email = "user2@example.com"
        data, status_code = self.requester.create_user(email, self.password, self.username)

        self.assertEqual(409, status_code)
        self.assertEqual(ExceptionMessages.USERNAME_NOT_AVAILABLE, data["msg"])


if __name__ == "__main__":
    unittest.main()
