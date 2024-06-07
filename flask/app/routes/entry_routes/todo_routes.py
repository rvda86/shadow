from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.main import app
from app.error_handling import error_handler
from app.controllers.entry_controller import EntryController
from app.routes.schemas.todo_schemas.CreateToDoSchema import CreateToDoSchema
from app.routes.schemas.todo_schemas.UpdateToDoSchema import UpdateToDoSchema
from app.validators.id import validate_id


@app.route("/api/entry/todo", methods=["POST"])
@error_handler
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = CreateToDoSchema(**data)
    return EntryController.create(user_id, data, "todo")


@app.route("/api/entry/todo", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_todo():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.delete(user_id, category_id, "todo")


@app.route("/api/entry/todo", methods=["GET"])
@error_handler
@jwt_required()
def get_todo():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.get(user_id, category_id, "todo")


@app.route("/api/entry/todo", methods=["PUT"])
@error_handler
@jwt_required()
def update_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = UpdateToDoSchema(**data)
    return EntryController.update(user_id, data, "todo")
