import sys

from flask import jsonify
from flask_jwt_extended import create_access_token

from app.config import Config
from app.constants.ControllerMessages import ControllerMessages
from app.constants.ExceptionMessages import ExceptionMessages
from app.error_handling import PasswordResetNotPossible
from app.models.entry.entries import get_all_categories_by_user, to_dict
from app.models.user.User import User
from app.utils.utils import send_email_verification_mail, send_password_reset_mail
from app.validation import preprocess_incoming_data


class UserController:

    @staticmethod
    def create_user(data):
        if isinstance(data, dict):
            data["type"] = "user"
        data = preprocess_incoming_data(data, "POST")
        user = User()
        user = user.create(data)
        response = {"data": user.as_dict_private_profile(), "msg": ControllerMessages.ACCOUNT_CREATED}
        if Config.MAIL_ENABLED:
            send_email_verification_mail(user)
        return jsonify(response)

    @staticmethod
    def delete_user(user_id, data):
        if isinstance(data, dict):
            data["type"] = "user"
        data = preprocess_incoming_data(data, "DELETE")
        user = User()
        user.load_by_id(user_id)
        user.authenticate(data["password"])
        response = user.delete(user_id)
        return jsonify(response)

    @staticmethod
    def email_verification(email):
        user = User()
        user.load_by_email(email)
        user.set_email_verified(True)
        response = user.update_email_verification_status()
        return jsonify(response)

    @staticmethod
    def email_verification_send_link(user_id):
        user = User()
        user.load_by_id(user_id)
        if Config.MAIL_ENABLED:
            response = send_email_verification_mail(user)
        else:
            response = ControllerMessages.EMAIL_VERIFICATION_DISABLED
        return jsonify({"msg": response})

    @staticmethod
    def get_all_data_by_user(user_id: str):
        user = User()
        user.load_by_id(user_id)
        user_data = {"username": user.get_username(), "email": user.get_email(),
                     "email_verified": user.get_email_verified()}
        user_categories = [to_dict(category) for category in get_all_categories_by_user(user_id)]
        return jsonify({"user_data": user_data, "user_categories": user_categories})

    @staticmethod
    def get_user(user_id):
        user = User()
        user.load_by_id(user_id)
        return jsonify({"username": user.get_username(), "email": user.get_email(),
                        "email_verified": user.get_email_verified()})

    @staticmethod
    def get_token(data):
        if isinstance(data, dict):
            data["type"] = "token"
        data = preprocess_incoming_data(data, "POST")
        user = User()
        user.load_by_username(data["username"])
        user.authenticate(data["password"])
        response = user.get_token()
        return jsonify(response)

    @staticmethod
    def get_token_email(user_id):
        user = User()
        user.load_by_id(user_id)
        access_token = {"access_token": create_access_token(identity=user.get_email())}
        return jsonify(access_token)

    @staticmethod
    def password_reset_send_link(data):
        user = User()
        user.load_by_email(data["email"])
        if not user.email_verified:
            raise PasswordResetNotPossible()
        if Config.MAIL_ENABLED:
            response = send_password_reset_mail(user)
        else:
            response = ControllerMessages.PASSWORD_RESET_MAIL_DISABLED
        return jsonify({"msg": response})

    @staticmethod 
    def reset_password(data):
        user = User()
        user.load_by_email(data["email"])
        user.set_password(data["password"])
        response = user.update_password_password_reset()
        return jsonify(response)
    
    @staticmethod
    def update_user(user_id, data):
        if isinstance(data, dict): 
            data["type"] = "user"
        data = preprocess_incoming_data(data, "PUT")
        user = User()
        user.load_by_id(user_id)
        user.authenticate(data["currentPassword"])
        response = user.update(user_id, data)
        if data["email"] != user.get_email():
            user.set_email_verified(False)
            user.update_email_verification_status()
            send_email_verification_mail(user)
        return jsonify(response)
