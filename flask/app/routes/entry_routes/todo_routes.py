from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.main import app
from app.error_handling import error_handler
from app.controllers.entry_controller import EntryController
from app.routes.schemas.journal_schemas.CreateJournalSchema import CreateJournalSchema
from app.routes.schemas.journal_schemas.UpdateJournalSchema import UpdateJournalSchema
from app.validators.id import validate_id


@app.route("/api/entry/journal", methods=["POST"])
@error_handler
@jwt_required()
def create_journal():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = CreateJournalSchema(**data)
    return EntryController.create(user_id, data, "journal")


@app.route("/api/entry/journal", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_journal():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.delete(user_id, category_id, "journal")


@app.route("/api/entry/journal", methods=["GET"])
@error_handler
@jwt_required()
def get_journal():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return EntryController.get(user_id, category_id, "journal")


@app.route("/api/entry/journal", methods=["PUT"])
@error_handler
@jwt_required()
def update_journal():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = UpdateJournalSchema(**data)
    return EntryController.update(user_id, data, "journal")
