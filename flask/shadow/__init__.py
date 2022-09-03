from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv
import os
import datetime
import logging

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_TESTING = os.getenv("DB_TESTING")
DB_DEVELOPMENT = os.getenv("DB_DEVELOPMENT")
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

app = Flask(__name__)
app.config['MAIL_SERVER']= MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=7200)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
CORS(app)

logging.basicConfig(filename='./shadow/logs/logs.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

from shadow.routes import entry_routes, user_routes, frontend_routes