from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_TESTING = os.getenv("DB_TESTING")
    DB_PRODUCTION = os.getenv("DB_PRODUCTION")
    TEST_ENVIRONMENT = "True" in os.getenv("TEST_ENVIRONMENT")
    API_LINK = os.getenv("API_LINK")
    PASSWORD_RESET_LINK = os.getenv("PASSWORD_RESET_LINK")
    EMAIL_VERIFICATION_LINK = os.getenv("EMAIL_VERIFICATION_LINK")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_USE_TLS = "True" in os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = "True" in os.getenv("MAIL_USE_SSL")