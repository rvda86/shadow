import re
from shadow.error_handling import InvalidDataError

def strip_whitespace_dict(data: dict):
    for k in data:
        if isinstance(data[k], str):
            data[k] = data[k].strip()
    return data

required_keys = {
        "category":{"GET": ["type", "id"],
                    "POST": ["type", "name"], 
                    "PUT": ["type", "name", "id"], 
                    "DELETE": ["type", "id"]},
        "topic": {  "GET": ["type", "id"],
                    "POST": ["type", "topic_type", "name", "category_id"], 
                    "PUT": ["type", "name", "id"], 
                    "DELETE": ["type", "id"]},
        "journal": {"GET": ["type", "id"],
                    "POST": ["type", "title", "content", "topic_id"], 
                    "PUT": ["type", "title", "content", "id"],
                    "DELETE": ["type", "id"]},
        "todo": {   "GET": ["type", "id"],
                    "POST": ["type", "task", "due_date", "topic_id"], 
                    "PUT": ["type", "task", "due_date", "completed", "id"], 
                    "DELETE": ["type", "id"]},
        "habit": {  "GET": ["type", "id"],
                    "POST": ["type", "name", "topic_id"],
                    "PUT": ["type", "name", "days_completed", "id"],
                    "DELETE": ["type", "id"]},
        "user": {   "GET": ["type", "id"],
                    "POST": ["type", "username", "email", "password"], 
                    "PUT": ["type", "username", "email", "password", "currentPassword"], 
                    "DELETE": ["type", "password"]},
        "token": {  "POST": ["type", "username", "password"]}             
        }

def validate_data(data, method):
    if not isinstance(data, dict):
        raise InvalidDataError("1")
    data = strip_whitespace_dict(data)
    if "type" not in data: 
        raise InvalidDataError("2")
    if data["type"] not in ["category", "topic", "journal", "habit", "todo", "user", "token"]:
        raise InvalidDataError("3")
    return validate_values(data, required_keys[data["type"]][method])

def validate_values(data, required_keys):

    for k in required_keys:
        if k not in data:
            raise InvalidDataError("4")

    for k in data:
        if k not in required_keys:
            raise InvalidDataError("5")
        elif k in ["type", "days_completed"]:
            pass
        elif k in ["name", "title", "task"]:
            if len(data[k]) < 1 or len(data[k]) > 100: 
                raise InvalidDataError("6")
        elif k in ["id", "category_id", "topic_id"]:
            if len(data[k]) != 36: 
                raise InvalidDataError("7")
        elif k == "topic_type":
            if data[k] not in ["journal", "todo", "habit"]:
                raise InvalidDataError("8")
        elif k == "content":
            if len(data[k]) > 65535:
                raise InvalidDataError
        elif k == "due_date":
            if not re.search("(\d{4}-\d{2}-\d{2})", data[k]):
                raise InvalidDataError
        elif k == "completed":
            if data[k] not in ["0", "1"]:
                raise InvalidDataError
        elif k == "username":
            if not re.search("([a-zA-Z0-9._])", data[k]) and (len(data[k]) < 5 or len(data[k]) > 32):
                raise InvalidDataError
        elif k == "email":
            if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data[k]):
                raise InvalidDataError("9")
        elif k == "password" or k == "currentPassword":
            if len(data[k]) < 8:
                raise InvalidDataError("10")
        else:
            raise InvalidDataError

    return data