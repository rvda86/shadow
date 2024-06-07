from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.main import app
from app.error_handling import error_handler
from app.controllers.category_controller import CategoryController
from app.routes.schemas.category_schemas.CreateCategorySchema import CreateCategorySchema
from app.routes.schemas.category_schemas.UpdateCategorySchema import UpdateCategorySchema
from app.validators.id import validate_id


@app.route("/api/entry/category", methods=["POST"])
@error_handler
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = CreateCategorySchema(**data)
    return CategoryController.create(user_id, data)


@app.route("/api/entry/category", methods=["DELETE"])
@error_handler
@jwt_required()
def delete_category():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return CategoryController.delete(user_id, category_id)


@app.route("/api/entry/category", methods=["GET"])
@error_handler
@jwt_required()
def get_category():
    user_id = get_jwt_identity()
    category_id = validate_id(request.args.get('id'))
    return CategoryController.get(user_id, category_id)


@app.route("/api/entry/category", methods=["PUT"])
@error_handler
@jwt_required()
def update_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    data = UpdateCategorySchema(**data)
    return CategoryController.update(user_id, data)
