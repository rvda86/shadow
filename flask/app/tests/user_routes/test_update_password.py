import unittest

from app.config import Config
from app.constants.ControllerMessages import ControllerMessages
from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /api/users PUT
# update password
class TestUpdatePassword(unittest.TestCase):

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
        self.token, self.user_data = create_user(self.requester, self.email, self.password, self.username)

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        new_password = "passwSf2@ord_new"
        data, status_code = self.requester.update_user(self.password, self.email, new_password, self.username, self.token)
        self.assertEqual(200, status_code)
        self.assertEqual(data["msg"], ControllerMessages.ACCOUNT_UPDATED)

    def test_password_entirely_numeric(self):
        new_password = "1234567891234"
        data, status_code = self.requester.update_user(self.password, self.email, new_password, self.username, self.token)
        self.assertEqual(422, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.PASSWORD_NUMERIC)

    def test_password_too_common(self):
        new_password = "password"
        data, status_code = self.requester.update_user(self.password, self.email, new_password, self.username, self.token)
        self.assertEqual(422, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.PASSWORD_TOO_COMMON)

    def test_password_too_long(self):
        new_password = "a" * 129
        data, status_code = self.requester.update_user(self.password, self.email, new_password, self.username, self.token)
        self.assertEqual(422, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.PASSWORD_TOO_LONG)

    def test_password_too_short(self):
        new_password = "shortpw"
        data, status_code = self.requester.update_user(self.password, self.email, new_password, self.username, self.token)
        self.assertEqual(422, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.PASSWORD_TOO_SHORT)


if __name__ == "__main__":
    unittest.main()
