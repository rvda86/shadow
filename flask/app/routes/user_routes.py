from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.user_controller import UserController
from app.error_handling import error_handler
from app.main import app
from app.routes.schemas.user_schemas.CreateUserSchema import CreateUserSchema
from app.routes.schemas.user_schemas.DeleteUserSchema import DeleteUserSchema
from app.routes.schemas.user_schemas.GetTokenSchema import GetTokenSchema
from app.routes.schemas.user_schemas.PasswordResetRequestSchema import PasswordResetRequestSchema
from app.routes.schemas.user_schemas.PasswordResetSchema import PasswordResetSchema
from app.routes.schemas.user_schemas.UpdateUserSchema import UpdateUserSchema


@app.route("/api/users", methods=["POST"])
@error_handler
def create_user():
    data = request.get_json()
    data = CreateUserSchema(**data)
    return UserController.create_user(data)


@app.route("/api/users/delete", methods=["POST"])
@error_handler
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = DeleteUserSchema(**data)
    return UserController.delete_user(user_id, data)


@app.route("/api/data", methods=["GET"])
@error_handler
@jwt_required()
def get_all_data_by_user():
    user_id = get_jwt_identity()
    return UserController.get_all_data_by_user(user_id)


@app.route("/api/users/token", methods=["POST"])
@error_handler
def get_token():
    data = request.get_json()
    data = GetTokenSchema(**data)
    return UserController.get_token(data)


# temp route for testing purposes
@app.route("/api/users/token-email", methods=["GET"])
@error_handler
@jwt_required()
def get_token_email():
    user_id = get_jwt_identity()
    return UserController.get_token_email(user_id)


@app.route("/api/users", methods=["GET"])
@error_handler
@jwt_required()
def get_user(): 
    user_id = get_jwt_identity()
    return UserController.get_user(user_id)


@app.route("/api/users/reset_password", methods=["POST"])
@error_handler
@jwt_required()
def reset_password():
    email = get_jwt_identity()
    data = request.get_json()
    data = PasswordResetSchema(**data)
    return UserController.reset_password(data, email)


@app.route("/api/users/reset_password_send_link", methods=["POST"])
@error_handler
def reset_password_send_link():
    data = request.get_json()
    data = PasswordResetRequestSchema(**data)
    return UserController.password_reset_send_link(data)


@app.route("/api/users", methods=["PUT"])
@error_handler
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = UpdateUserSchema(**data)
    return UserController.update_user(user_id, data)


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
