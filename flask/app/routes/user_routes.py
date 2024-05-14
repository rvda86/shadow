from app import flask_app as app
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.error_handling import (error_handler)
from app.controllers.user_controller import UserController

@app.route("/api/users", methods=["GET"])
@error_handler
@jwt_required()
def get_user(): 
    user_id = get_jwt_identity()
    return UserController.get_user(user_id)

@app.route("/api/users", methods=["POST"])
@error_handler
def create_user():
    data = request.get_json()
    return UserController.create_user(data)

@app.route("/api/users", methods=["PUT"])
@error_handler
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    return UserController.update_user(user_id, data)

@app.route("/api/users", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    return UserController.delete_user(user_id, data)

@app.route("/api/users/token", methods=["POST"])
@error_handler
def get_token():
    data = request.get_json()
    return UserController.get_token(data)

@app.route("/api/data", methods=["GET"])
@error_handler
@jwt_required()
def get_all_data_by_user():
    user_id = get_jwt_identity()
    return UserController.get_all_data_by_user(user_id)

@app.route("/api/users/verify_email", methods=["POST"])
@error_handler
@jwt_required()
def verify_email():
    email = get_jwt_identity()
    return UserController.email_verification(email)

@app.route("/api/users/verify_email_send_link", methods=["GET"])
@error_handler
@jwt_required()
def verify_email_send_link():
    user_id = get_jwt_identity()
    return UserController.email_verification_send_link(user_id)

@app.route("/api/users/reset_password", methods=["POST"])
@error_handler
@jwt_required()
def reset_password_send_link():
    email = get_jwt_identity()
    data = request.get_json()
    data["email"] = email
    return UserController.reset_password(data)

@app.route("/api/users/reset_password_send_link", methods=["POST"])
@error_handler
def reset_password():
    data = request.get_json()
    return UserController.password_reset_send_link(data)
