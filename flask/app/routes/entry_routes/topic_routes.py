from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.main import app
from app.error_handling import error_handler
from app.controllers.entry_controller import EntryController
from app.routes.schemas.topic_schemas.CreateTopicSchema import CreateTopicSchema
from app.routes.schemas.topic_schemas.UpdateTopicSchema import UpdateTopicSchema
from app.validators.id import validate_id


@app.route("/api/entry/topic", methods=["POST"])
@error_handler
@jwt_required()
def create_topic():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = CreateTopicSchema(**data)
    return EntryController.create(user_id, data, "topic")


@app.route("/api/entry/topic", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_topic():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.delete(user_id, category_id, "topic")


@app.route("/api/entry/topic", methods=["GET"])
@error_handler
@jwt_required()
def get_topic():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.get(user_id, category_id, "topic")


@app.route("/api/entry/topic", methods=["PUT"])
@error_handler
@jwt_required()
def update_topic():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = UpdateTopicSchema(**data)
    return EntryController.update(user_id, data, "topic")
