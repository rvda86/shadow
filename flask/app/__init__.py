from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import datetime
import logging
from app.config import Config

flask_app = Flask(__name__)
flask_app.config['MAIL_SERVER']= Config.MAIL_SERVER
flask_app.config['MAIL_PORT'] = Config.MAIL_PORT
flask_app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
flask_app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
flask_app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
flask_app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL
flask_app.config['SECRET_KEY'] = Config.SECRET_KEY
flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=7200)
bcrypt = Bcrypt(flask_app)
jwt = JWTManager(flask_app)
mail = Mail(flask_app)
CORS(flask_app)

logging.basicConfig(filename='./app/logs/main.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

from app.routes import entry_routes, user_routes, frontend_routes