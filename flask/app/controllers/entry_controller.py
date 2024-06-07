from flask import jsonify

from app.factory import get_entry
from app.models.entry.Entry import to_dict
from app.routes.schemas.EntrySchema import EntrySchema


class EntryController:

    @staticmethod
    def create(user_id: str, data: EntrySchema, entry_type: str):
        entry = get_entry(entry_type)
        entry, msg = entry.create(user_id, data)
        return jsonify({"entry": to_dict(entry), "msg": msg})

    @staticmethod
    def delete(user_id: str, entry_id: str, entry_type: str):
        entry = get_entry(entry_type)
        entry.load_by_id(entry_id, user_id)
        msg = entry.delete(user_id)
        return jsonify({"msg": msg})

    @staticmethod
    def get(user_id: str, entry_id: str, entry_type: str):
        entry = get_entry(entry_type)
        entry.load_by_id(entry_id, user_id)
        return jsonify({"data": to_dict(entry)})

    @staticmethod
    def update(user_id: str, data: EntrySchema, entry_type: str):
        entry = get_entry(entry_type)
        entry.load_by_id(data.id, user_id)
        entry, msg = entry.update(user_id, data)
        return jsonify({"entry": to_dict(entry), "msg": msg})
