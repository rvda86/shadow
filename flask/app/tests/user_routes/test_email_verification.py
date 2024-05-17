import unittest

from app.config import Config
from app.constants.ControllerMessages import ControllerMessages
from app.db_mysql import db_pool
from app.main import app
from app.tests.user_routes.helpers import create_user
from app.tests.user_routes.UserRequester import UserRequester

# /users/verify_email POST
# /users/verify_email_send_link GET


class TestEmailVerification(unittest.TestCase):

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

    def tearDown(self):
        self.db.reset_database()

    def test_success_resend_verification_link(self):
        token, data = create_user(self.requester, self.email, self.password, self.username)

        data, status_code = self.requester.resend_email_verification_link(token)

        self.assertEqual(200, status_code)
        if Config.MAIL_ENABLED:
            self.assertEqual(ControllerMessages.EMAIL_VERIFICATION_MAIL_SENT, data["msg"])
        else:
            self.assertEqual(ControllerMessages.EMAIL_VERIFICATION_DISABLED, data["msg"])

    def test_success_verify_email(self):
        create_user(self.requester, self.email, self.password, self.username)

        data, status_code = self.requester.verify_email(token)
        self.assertEqual(200, status_code)
        self.assertEqual(ControllerMessages.EMAIL_VERIFIED, data["msg"])


if __name__ == "__main__":
    unittest.main()
