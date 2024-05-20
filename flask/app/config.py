import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_LINK = os.getenv("API_LINK")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PRODUCTION = os.getenv("DB_PRODUCTION")
    DB_TESTING = os.getenv("DB_TESTING")
    DB_USER = os.getenv("DB_USER")
    EMAIL_VERIFICATION_LINK = os.getenv("EMAIL_VERIFICATION_LINK")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_ENABLED = bool(int(os.getenv("MAIL_ENABLED")))
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_USE_SSL = bool(int(os.getenv("MAIL_USE_SSL")))
    MAIL_USE_TLS = bool(int(os.getenv("MAIL_USE_TLS")))
    PASSWORD_RESET_LINK = os.getenv("PASSWORD_RESET_LINK")
    SECRET_KEY = os.getenv("SECRET_KEY")
    TEST_ENVIRONMENT = bool(int(os.getenv("TEST_ENVIRONMENT")))
    TEST_CLIENT = os.getenv("TEST_CLIENT")
