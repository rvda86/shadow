from flask import jsonify
from shadow.models.user.users import User, get_all_usernames_emails
from shadow.validation import preprocess_incoming_data
from shadow.models.entry.entries import get_all_categories_by_user, to_dict
from shadow.utils import send_email_verification_mail, send_password_reset_mail

class UserController:

    @staticmethod
    def get_user(user_id):
        user = User()
        user.load_by_id(user_id)
        return jsonify({"username": user.get_username(), "email": user.get_email()})

    @staticmethod
    def email_verification_send_link(user_id):
        user = User()
        user.load_by_id(user_id)
        send_email_verification_mail(user)

    @staticmethod
    def password_reset_send_link(data):
        user = User()
        user.load_by_email(data["email"])
        response = send_password_reset_mail(user)
        return jsonify({"msg": response})

    @staticmethod
    def email_verification(email):
        user = User()
        user.load_by_email(email)
        user.set_email_verified(True)
        response = user.update_email_verification_status()
        return jsonify(response)

    @staticmethod 
    def reset_password(data):
        user = User()
        user.load_by_email(data["email"])
        user.set_password(data["password"])
        response = user.update_password_password_reset()
        return jsonify(response)

    @staticmethod
    def create_user(data):
        if isinstance(data, dict): 
            data["type"] = "user"
        data = preprocess_incoming_data(data, "POST")
        user = User()
        response = user.create(data)
        send_email_verification_mail(user)
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
    def check_available_username_email(data: dict):
        existing_usernames, existing_emails = get_all_usernames_emails()
        username_available = True
        email_available = True
        if data["username"] in existing_usernames:
            username_available = False
        if data["email"] in existing_emails:
            email_available = False
        return jsonify({"username": username_available, "email": email_available})

    @staticmethod
    def get_all_data_by_user(user_id: str):
        user = User()
        user.load_by_id(user_id)
        user_data = {"username": user.get_username(), "email": user.get_email()}
        user_categories = [to_dict(category) for category in get_all_categories_by_user(user_id)]
        return jsonify({"user_data": user_data, "user_categories": user_categories})

  