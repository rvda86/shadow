import unittest

from app.constants.ControllerMessages import ControllerMessages
from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /api/users DELETE
class TestDeleteUser(unittest.TestCase):

    db = db_pool.acquire()
    requester = UserRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.email = "user1@example.com"
        self.username = "user1"
        self.password = "passwSf2@ord"

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        token, data = create_user(self.requester, self.email, self.password, self.username)

        data, status_code = self.requester.delete_user(self.password, token)
        self.assertEqual(200, status_code)
        self.assertEqual(ControllerMessages.ACCOUNT_DELETED, data["msg"])

    def test_password_missing(self):
        token, _ = create_user(self.requester, self.email, self.password, self.username)
        data = {}

        data, status_code = self.requester.post_request(data, "user", token)
        self.assertEqual(422, status_code)

    def test_too_many_fields(self):
        token, _ = create_user(self.requester, self.email, self.password, self.username)
        data = {"email": self.email, "password": self.password}

        data, status_code = self.requester.post_request(data, "user", token)
        self.assertEqual(422, status_code)

    def test_wrong_field(self):
        token, data = create_user(self.requester, self.email, self.password, self.username)
        data = {"wrong_field": self.password}

        data, status_code = self.requester.post_request(data, "user", token)
        self.assertEqual(422, status_code)

    def test_unknown_user(self):
        token, data = create_user(self.requester, self.email, self.password, self.username)
        self.requester.delete_user(self.password, token)

        data, status_code = self.requester.delete_user(self.password, token)
        self.assertEqual(404, status_code)
        self.assertEqual(ExceptionMessages.USER_NOT_FOUND, data["msg"])

    def test_wrong_password(self):
        token, data = create_user(self.requester, self.email, self.password, self.username)
        wrong_password = "wrong_password"

        data, status_code = self.requester.delete_user(wrong_password, token)
        self.assertEqual(401, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_WRONG, data["msg"])


if __name__ == "__main__":
    unittest.main()
