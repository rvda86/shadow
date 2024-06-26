import datetime

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from app.config import Config
from app.logging import get_main_logger


def create_app():
    app = Flask(__name__)
    app.config['MAIL_SERVER']= Config.MAIL_SERVER
    app.config['MAIL_PORT'] = Config.MAIL_PORT
    app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=7200)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    mail = Mail(app)
    CORS(app)

    get_main_logger()

    return app, bcrypt, jwt, mail


app, bcrypt, jwt, mail = create_app()

from app.routes import user_routes, frontend_routes
from app.routes.entry_routes import category_routes, habit_routes, journal_routes, todo_routes, topic_routes
