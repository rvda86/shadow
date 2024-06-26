import unittest

from app.config import Config
from app.constants.ControllerMessages import ControllerMessages
from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /users/reset_password POST

class TestPasswordReset(unittest.TestCase):

    db = db_pool.acquire()
    requester = UserRequester()

    def setUp(self):
        if self.db.name != "shadow_testing":
            raise Exception
        self.email = "user1@example.com"
        self.password = "passwSf2@ord"
        self.username = "user1"
        self.token, self.user_data = create_user(self.requester, self.email, self.password, self.username)
        self.token_based_on_email, status_code = self.requester.get_token_email(self.token)
        self.token_based_on_email = self.token_based_on_email["access_token"]

    def tearDown(self):
        self.db.reset_database()

    def test_success_reset_password(self):
        new_password = "passwSf2@ord"
        self.requester.verify_email(self.token_based_on_email)

        data, status_code = self.requester.password_reset(new_password, self.token_based_on_email)

        self.assertEqual(200, status_code)
        self.assertEqual(ControllerMessages.PASSWORD_RESET, data["msg"])

    def test_password_missing(self):
        data = {}
        data, status_code = self.requester.post_request(data, "password_reset", self.token_based_on_email)

        self.assertEqual(422, status_code)

    def test_too_many_fields(self):
        data = {"email": self.email, "password": self.password}
        data, status_code = self.requester.post_request(data, "password_reset", self.token_based_on_email)

        self.assertEqual(422, status_code)

    def test_wrong_field(self):
        data = {"color": self.password}
        data, status_code = self.requester.post_request(data, "password_reset", self.token_based_on_email)

        self.assertEqual(422, status_code)

    def test_reset_password_email_not_verified(self):
        new_password = "passwSf2@ord"

        data, status_code = self.requester.password_reset(new_password, self.token_based_on_email)

        self.assertEqual(403, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_RESET_NOT_POSSIBLE, data["msg"])

    def test_password_entirely_numeric(self):
        new_password = "1234567891234"
        self.requester.verify_email(self.token_based_on_email)

        data, status_code = self.requester.password_reset(new_password, self.token_based_on_email)

        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_NUMERIC, data["msg"])

    def test_password_too_common(self):
        new_password = "password"
        self.requester.verify_email(self.token_based_on_email)

        data, status_code = self.requester.password_reset(new_password, self.token_based_on_email)

        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_TOO_COMMON, data["msg"])

    def test_password_too_long(self):
        new_password = "a" * 129
        self.requester.verify_email(self.token_based_on_email)

        data, status_code = self.requester.password_reset(new_password, self.token_based_on_email)

        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_TOO_LONG, data["msg"])

    def test_password_too_short(self):
        new_password = "shortpw"
        self.requester.verify_email(self.token_based_on_email)

        data, status_code = self.requester.password_reset(new_password, self.token_based_on_email)

        self.assertEqual(422, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_TOO_SHORT, data["msg"])


if __name__ == "__main__":
    unittest.main()
