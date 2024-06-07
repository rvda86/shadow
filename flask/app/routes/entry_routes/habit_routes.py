from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.main import app
from app.error_handling import error_handler
from app.controllers.entry_controller import EntryController
from app.routes.schemas.habit_schemas.CreateHabitSchema import CreateHabitSchema
from app.routes.schemas.habit_schemas.UpdateHabitSchema import UpdateHabitSchema
from app.validators.id import validate_id


@app.route("/api/entry/habit", methods=["POST"])
@error_handler
@jwt_required()
def create_habit():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = CreateHabitSchema(**data)
    return EntryController.create(user_id, data, "habit")


@app.route("/api/entry/habit", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_habit():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.delete(user_id, category_id, "habit")


@app.route("/api/entry/habit", methods=["GET"])
@error_handler
@jwt_required()
def get_habit():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.get(user_id, category_id, "habit")


@app.route("/api/entry/habit", methods=["PUT"])
@error_handler
@jwt_required()
def update_habit():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = UpdateHabitSchema(**data)
    return EntryController.update(user_id, data, "habit")
