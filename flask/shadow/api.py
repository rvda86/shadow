from shadow import app
from flask import request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from shadow.factory import get_entry_factory
from shadow.serialize import get_serializer
from shadow.users import User, get_all_usernames_emails
from shadow.validator import validate_data
from shadow.error_handling import api_error_handler

@app.route("/api/users/create", methods=["POST"])
@api_error_handler
def api_users_create():
    data = request.get_json()
    if isinstance(data, dict): 
        data["type"] = "user"
    data = validate_data(data, request.method)

    user = User()
    user.set_values(data)
    response = user.create()
    return jsonify(response)

@app.route("/api/users/token", methods=["POST"])
@api_error_handler
def api_users_token():
    data = request.get_json()
    if isinstance(data, dict): 
        data["type"] = "token"
    data = validate_data(data, request.method)
    user = User()
    user.load_data_by_username(data["username"])
    user.authenticate(data["password"])
    response = user.get_token()
    return jsonify(response)

@app.route("/api/users/check_availability", methods=["POST"])
@api_error_handler
def api_users_check_available():
    data = request.get_json()
    # validation ??
    existing_usernames, existing_emails = get_all_usernames_emails()
    username_available = True
    email_available = True
    if data["username"] in existing_usernames:
        username_available = False
    if data["email"] in existing_emails:
        email_available = False
    return jsonify({"username": username_available, "email": email_available})

@app.route("/api/users", methods=["GET", "PUT", "DELETE"])
@api_error_handler
@jwt_required()
def api_users():

    user_id = get_jwt_identity()
    user = User()
    user.load_data_by_id(user_id)

    if request.method == "GET":
        response = user.fetchUserData()
        return jsonify(response)

    data = request.get_json()
    if isinstance(data, dict): 
        data["type"] = "user"
    data = validate_data(data, request.method)

    if request.method == "DELETE":
        user.authenticate(data["password"])
        response = user.delete()
        return jsonify(response)

    else: # request.method == "PUT":
        user.authenticate(data["currentPassword"])
        user.set_values(data)
        response = user.update()
        return jsonify(response)

@app.route("/api/data", methods=["GET"])
@api_error_handler
@jwt_required()
def api_data():
    user_id = get_jwt_identity()
    user = User()
    user.load_data_by_id(user_id)
    user_data = user.fetchUserData()

    serializer = get_serializer("categories")
    user_categories = serializer(user_id)

    return jsonify({"user_data": user_data, "user_categories": user_categories})
        
@app.route("/api/entries", methods=["GET", "POST", "DELETE", "PUT"])
@api_error_handler
@jwt_required()
def api_entries():
    user_id = get_jwt_identity()

    if request.method == "GET": 
        data = {"type": request.args.get('type'), "id": request.args.get('id')}
    else: 
        data = request.get_json()
    
    data = validate_data(data, request.method)

    entry_type = data["type"]
    entry_factory = get_entry_factory(entry_type)
    entry = entry_factory.get_entry()
    
    if request.method == "GET":
        serializer = get_serializer(entry_type)
        response = serializer(entry, data["id"], user_id)
        return jsonify({"data": response})

    elif request.method == "POST":
        entry.set_values(data, user_id)
        response = entry.create(user_id)      
        return jsonify({"msg": response})

    elif request.method == 'DELETE':
        entry.load_data(data["id"], user_id)
        response = entry.delete(user_id)
        return jsonify({"msg": response})

    else: # request.method == "PUT":
        entry.load_data(data["id"], user_id)
        entry.set_values(data, user_id)
        response = entry.update(user_id)
        return jsonify({"msg": response})