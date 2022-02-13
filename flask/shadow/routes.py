from shadow import app
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from shadow.error_handling import error_handler
from shadow.controllers import Controller

@app.route("/api/users", methods=["GET"])
@error_handler
@jwt_required()
def get_user(): 
    user_id = get_jwt_identity()
    return Controller.get_user(user_id)

@app.route("/api/users", methods=["POST"])
@error_handler
def create_user():
    data = request.get_json()
    return Controller.create_user(data)

@app.route("/api/users", methods=["PUT"])
@error_handler
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    return Controller.update_user(user_id, data)

@app.route("/api/users", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    return Controller.delete_user(user_id, data)

@app.route("/api/users/token", methods=["POST"])
@error_handler
def get_token():
    data = request.get_json()
    return Controller.get_token(data)

@app.route("/api/users/check_availability", methods=["POST"])
@error_handler
def check_available_username_email():
    data = request.get_json()
    return Controller.check_available_username_email(data)

@app.route("/api/data", methods=["GET"])
@error_handler
@jwt_required()
def get_all_data_by_user():
    user_id = get_jwt_identity()
    return Controller.get_all_data_by_user(user_id)

@app.route("/api/entries", methods=["GET"])
@error_handler
@jwt_required()
def get_entry():
    user_id = get_jwt_identity()
    data = {"type": request.args.get('type'), "id": request.args.get('id')}
    return Controller.get_entry(user_id, data)
    
@app.route("/api/entries", methods=["POST"])
@error_handler
@jwt_required()
def create_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    return Controller.create_entry(user_id, data)

@app.route("/api/entries", methods=["PUT"])
@error_handler
@jwt_required()
def update_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    return Controller.update_entry(user_id, data)
 
@app.route("/api/entries", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    return Controller.delete_entry(user_id, data)    