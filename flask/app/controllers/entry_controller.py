from flask import jsonify
from app.validation import preprocess_incoming_data
from app.factory import get_entry
from app.models.entry.entries import to_dict

class EntryController:

    @staticmethod
    def get_entry(user_id: str, data: dict):
        data = preprocess_incoming_data(data, "GET")        
        entry = get_entry(data["type"])
        entry.load_by_id(data["id"], user_id)       
        entry = to_dict(entry)
        return jsonify({"data": entry})  
    
    @staticmethod
    def create_entry(user_id: str, data: dict):
        data = preprocess_incoming_data(data, "POST")
        entry = get_entry(data["type"])
        created_entry, msg = entry.create(user_id, data)  
        created_entry = to_dict(created_entry)
        return jsonify({"entry": created_entry, "msg": msg})

    @staticmethod
    def update_entry(user_id: str, data: dict):
        data = preprocess_incoming_data(data, "PUT")      
        entry = get_entry(data["type"])
        entry.load_by_id(data["id"], user_id)
        created_entry, msg = entry.update(user_id, data)
        created_entry = to_dict(created_entry)
        return jsonify({"entry": created_entry, "msg": msg})

    @staticmethod
    def delete_entry(user_id: str, data: dict):
        data = preprocess_incoming_data(data, "DELETE")
        entry = get_entry(data["type"])
        entry.load_by_id(data["id"], user_id)
        msg = entry.delete(user_id)
        return jsonify({"msg": msg})
    