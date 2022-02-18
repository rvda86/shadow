from flask import jsonify
from shadow.users import User, get_all_usernames_emails
from shadow.validator import validate_data
from shadow.factory import get_entry
from shadow.entries import get_all_categories_by_user, to_dict

class Controller:

    @staticmethod
    def get_user(user_id):
        user = User()
        user.load_by_id(user_id)
        return jsonify({"username": user.get_username(), "email": user.get_email()})

    @staticmethod
    def create_user(data):
        if isinstance(data, dict): 
            data["type"] = "user"
        data = validate_data(data, "POST")
        user = User()
        response = user.create(data)
        return jsonify(response)
    
    @staticmethod
    def update_user(user_id, data):
        if isinstance(data, dict): 
            data["type"] = "user"
        data = validate_data(data, "PUT")
        user = User()
        user.load_by_id(user_id)
        user.authenticate(data["currentPassword"])
        response = user.update(user_id, data)
        return jsonify(response)

    @staticmethod
    def delete_user(user_id, data):
        if isinstance(data, dict): 
            data["type"] = "user"
        data = validate_data(data, "DELETE")
        user = User()
        user.load_by_id(user_id)        
        user.authenticate(data["password"])
        response = user.delete(user_id)
        return jsonify(response)

    @staticmethod 
    def get_token(data):
        if isinstance(data, dict): 
            data["type"] = "token"
        data = validate_data(data, "POST")
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

    @staticmethod
    def get_entry(user_id: str, data: dict):
        data = validate_data(data, "GET")        
        entry = get_entry(data["type"])
        entry.load_by_id(data["id"], user_id)       
        entry = to_dict(entry)
        return jsonify({"data": entry})  
    
    @staticmethod
    def create_entry(user_id: str, data: dict):
        data = validate_data(data, "POST")
        entry = get_entry(data["type"])
        created_entry, msg = entry.create(user_id, data)  
        created_entry = to_dict(created_entry)   
        return jsonify({"entry": created_entry, "msg": msg})

    @staticmethod
    def update_entry(user_id: str, data: dict):
        data = validate_data(data, "PUT")      
        entry = get_entry(data["type"])
        entry.load_by_id(data["id"], user_id)
        msg = entry.update(user_id, data)
        return jsonify({"msg": msg})

    @staticmethod
    def delete_entry(user_id: str, data: dict):
        data = validate_data(data, "DELETE")
        entry = get_entry(data["type"])
        entry.load_by_id(data["id"], user_id)
        msg = entry.delete(user_id)
        return jsonify({"msg": msg})
    