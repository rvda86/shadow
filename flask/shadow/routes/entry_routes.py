from shadow import app
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from shadow.error_handling import error_handler
from shadow.controllers.entry_controller import EntryController

@app.route("/api/entries", methods=["GET"])
@error_handler
@jwt_required()
def get_entry():
    user_id = get_jwt_identity()
    data = {"type": request.args.get('type'), "id": request.args.get('id')}
    return EntryController.get_entry(user_id, data)
    
@app.route("/api/entries", methods=["POST"])
@error_handler
@jwt_required()
def create_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    return EntryController.create_entry(user_id, data)

@app.route("/api/entries", methods=["PUT"])
@error_handler
@jwt_required()
def update_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    return EntryController.update_entry(user_id, data)
 
@app.route("/api/entries", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    return EntryController.delete_entry(user_id, data)    