import unittest

from app.config import Config
from app.constants.ControllerMessages import ControllerMessages
from app.constants.ExceptionMessages import ExceptionMessages
from app.db_mysql import db_pool
from app.tests.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester


# /users/reset_password_send_link POST
class TestPasswordResetRequest(unittest.TestCase):

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

    def test_success_send_password_reset_link(self):
        self.requester.verify_email(self.token_based_on_email)

        data, status_code = self.requester.send_password_reset_link(self.email)
        self.assertEqual(200, status_code)
        if Config.MAIL_ENABLED:
            self.assertEqual(ControllerMessages.PASSWORD_RESET_MAIL_SENT, data["msg"])
        else:
            self.assertEqual(ControllerMessages.PASSWORD_RESET_MAIL_DISABLED, data["msg"])

    def test_email_missing(self):
        data = {}
        data, status_code = self.requester.post_request(data, "password_reset_request")

        self.assertEqual(422, status_code)

    def test_too_many_fields(self):
        data = {"email": self.email, "username": self.username}
        data, status_code = self.requester.post_request(data, "password_reset_request")

        self.assertEqual(422, status_code)

    def test_wrong_field(self):
        data = {"color": self.email}
        data, status_code = self.requester.post_request(data, "password_reset_request")

        self.assertEqual(422, status_code)

    def test_send_password_reset_link_email_not_verified(self):
        data, status_code = self.requester.send_password_reset_link(self.email)

        self.assertEqual(403, status_code)
        self.assertEqual(ExceptionMessages.PASSWORD_RESET_NOT_POSSIBLE, data["msg"])


if __name__ == "__main__":
    unittest.main()
