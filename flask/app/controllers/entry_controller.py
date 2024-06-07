from flask import jsonify

from app.models.entry.Habit import Habit
from app.models.entry.Entry import to_dict
from app.routes.schemas.habit_schemas.CreateHabitSchema import CreateHabitSchema
from app.routes.schemas.category_schemas.UpdateCategorySchema import UpdateCategorySchema


class CategoryController:

    @staticmethod
    def create(user_id: str, data: CreateCategorySchema):
        habit = Habit()
        habit, msg = habit.create(user_id, data)
        return jsonify({"entry": to_dict(habit), "msg": msg})

    @staticmethod
    def delete(user_id: str, category_id: str):
        habit = Habit()
        habit.load_by_id(category_id, user_id)
        msg = habit.delete(user_id)
        return jsonify({"msg": msg})

    @staticmethod
    def get(user_id: str, category_id: str):
        category = Habit()
        category.load_by_id(category_id, user_id)
        return jsonify({"data": to_dict(category)})

    @staticmethod
    def update(user_id: str, data: UpdateCategorySchema):
        category = Habit()
        category.load_by_id(data.id, user_id)
        created_entry, msg = category.update(user_id, data)
        return jsonify({"entry": to_dict(created_entry), "msg": msg})
