from flask import jsonify
from shadow.users import User, get_all_usernames_emails
from shadow.validator import validate_data
from shadow.serialize import get_serializer
from shadow.factory import get_entry

class Controller:

    @staticmethod
    def get_user(user_id):
        user = User()
        user.load_data_by_id(user_id)
        response = user.fetchUserData()
        return jsonify(response)

    @staticmethod
    def create_user(data):
        if isinstance(data, dict): 
            data["type"] = "user"
        data = validate_data(data, "POST")

        user = User()
        user.set_values(data)
        response = user.create()
        return jsonify(response)
    
    @staticmethod
    def update_user(user_id, data):
        user = User()
        user.load_data_by_id(user_id)
        if isinstance(data, dict): 
            data["type"] = "user"
        data = validate_data(data, "PUT")
        user.authenticate(data["currentPassword"])
        user.set_values(data)
        response = user.update()
        return jsonify(response)

    @staticmethod
    def delete_user(user_id, data):
        user = User()
        user.load_data_by_id(user_id)
        if isinstance(data, dict): 
            data["type"] = "user"
        data = validate_data(data, "DELETE")
        user.authenticate(data["password"])
        response = user.delete()
        return jsonify(response)

    @staticmethod 
    def get_token(data):
        if isinstance(data, dict): 
            data["type"] = "token"
        data = validate_data(data, "POST")
        user = User()
        user.load_data_by_username(data["username"])
        user.authenticate(data["password"])
        response = user.get_token()
        return jsonify(response)

    @staticmethod
    def check_available_username_email(data):
        existing_usernames, existing_emails = get_all_usernames_emails()
        username_available = True
        email_available = True
        if data["username"] in existing_usernames:
            username_available = False
        if data["email"] in existing_emails:
            email_available = False
        return jsonify({"username": username_available, "email": email_available})

    @staticmethod
    def get_all_data_by_user(user_id):
        user = User()
        user.load_data_by_id(user_id)
        user_data = user.fetchUserData()

        serializer = get_serializer("categories")
        user_categories = serializer(user_id)

        return jsonify({"user_data": user_data, "user_categories": user_categories})

    @staticmethod
    def get_entry(user_id, data):
        data = validate_data(data, "GET")
        
        entry = get_entry(data["type"])
        
        serializer = get_serializer(data["type"])
        response = serializer(entry, data["id"], user_id)
        return jsonify({"data": response})  
    
    @staticmethod
    def create_entry(user_id, data):
        data = validate_data(data, "POST")
        
        entry = get_entry(data["type"])
        
        entry.set_values(data, user_id)
        response = entry.create(user_id)      
        return jsonify({"msg": response})

    @staticmethod
    def update_entry(user_id, data):
        data = validate_data(data, "PUT")
      
        entry = get_entry(data["type"])

        entry.load_data(data["id"], user_id)
        entry.set_values(data, user_id)
        response = entry.update(user_id)
        return jsonify({"msg": response})

    @staticmethod
    def delete_entry(user_id, data):
        data = validate_data(data, "DELETE")

        entry = get_entry(data["type"])

        entry.load_data(data["id"], user_id)
        response = entry.delete(user_id)
        return jsonify({"msg": response})
    