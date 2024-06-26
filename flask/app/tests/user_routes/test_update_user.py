import unittest

from app.constants.ControllerMessages import ControllerMessages
from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /api/users PUT
# update username or email
class TestUpdateUser(unittest.TestCase):
    db = db_pool.acquire()
    requester = UserRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.email = "user1@example.com"
        self.username = "user1"
        self.email2 = "user2@example.com"
        self.username2 = "user2"
        self.password = "passwSf2@ord"

    def tearDown(self):
        self.db.reset_database()

    def test_success(self):
        token, data = create_user(self.requester, self.email, self.password, self.username)

        username = "mynewusername"
        email = "new@example.com"

        data, status_code = self.requester.update_user(self.password, email, self.password, username, token)
        self.assertEqual(200, status_code)
        self.assertEqual(username, data["data"]["username"])
        self.assertEqual(email, data["data"]["email"])
        self.assertEqual(data["msg"], ControllerMessages.ACCOUNT_UPDATED)

    def test_too_few_fields(self):
        token, _ = create_user(self.requester, self.email, self.password, self.username)
        data = {"email": self.email, "password": self.password, "username": self.username}
        data, status_code = self.requester.put_request(data, "user", token)

        self.assertEqual(422, status_code)

    def test_too_many_fields(self):
        token, _ = create_user(self.requester, self.email, self.password, self.username)
        data = {"currentPassword": self.password, "email": self.email, "password": self.password,
                "username": self.username, "phone": "0612345678"}
        data, status_code = self.requester.put_request(data, "user", token)

        self.assertEqual(422, status_code)

    def test_wrong_fields(self):
        token, data = create_user(self.requester, self.email, self.password, self.username)
        data = {"shape": self.password, "animal": self.email, "phone": self.password, "location": self.username}
        data, status_code = self.requester.put_request(data, "user", token)

        self.assertEqual(422, status_code)

    def test_username_not_available(self):
        create_user(self.requester, self.email, self.password, self.username)
        token, data = create_user(self.requester, self.email2, self.password, self.username2)

        data, status_code = self.requester.update_user(self.password, self.email2, self.password, self.username, token)
        self.assertEqual(409, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.USERNAME_NOT_AVAILABLE)

    def test_email_not_available(self):
        create_user(self.requester, self.email, self.password, self.username)
        token, data = create_user(self.requester, self.email2, self.password, self.username2)

        data, status_code = self.requester.update_user(self.password, self.email, self.password, self.username2, token)
        self.assertEqual(409, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.EMAIL_NOT_AVAILABLE)

    def test_username_too_long(self):
        token, data = create_user(self.requester, self.email2, self.password, self.username2)

        username = "a" * 31
        data, status_code = self.requester.update_user(self.password, self.email2, self.password, username, token)

        self.assertEqual(422, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.USERNAME_TOO_LONG)

    def test_username_too_short(self):
        token, data = create_user(self.requester, self.email2, self.password, self.username2)

        username = "a"
        data, status_code = self.requester.update_user(self.password, self.email2, self.password, username, token)
        self.assertEqual(422, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.USERNAME_TOO_SHORT)

    def test_invalid_email(self):
        token, data = create_user(self.requester, self.email2, self.password, self.username2)

        email = "user4example.com"

        data, status_code = self.requester.update_user(self.password, email, self.password, self.username2, token)
        self.assertEqual(422, status_code)
        self.assertEqual(data["msg"], ExceptionMessages.EMAIL_NOT_VALID)


if __name__ == "__main__":
    unittest.main()
