import re
import bleach
from shadow.error_handling import InvalidDataError

def sanitize_strings(data: dict):
    for k in data:
        if isinstance(data[k], str):
            data[k] = bleach.clean(data[k].strip())
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
        "tag": {    "GET": ["type", "id"],
                    "POST": ["type", "name"], 
                    "PUT": ["type", "name", "id"], 
                    "DELETE": ["type", "id"]},
        "token": {  "POST": ["type", "username", "password"]},       
        }

def check_keys(data, method):
    if "type" not in data: 
        raise InvalidDataError("key 'type' is mandatory")
    if data["type"] not in list(required_keys.keys()):
        raise InvalidDataError("wrong value for key 'type'")
 
    for k in required_keys[data["type"]][method]:
        if k not in data:
            raise InvalidDataError("missing required key(s)")  
    for k in data:
        if k not in required_keys[data["type"]][method]:
            raise InvalidDataError("key(s) not allowed")

def preprocess_incoming_data(data, method):
    if not isinstance(data, dict):
        raise InvalidDataError("not a dictionary")
    data = sanitize_strings(data)
    check_keys(data, method)
    return data

def validate_email(email):
    if not isinstance(email, str):
        raise InvalidDataError("invalid email")
    if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        raise InvalidDataError("invalid email")

def validate_password(password):
    if not isinstance(password, str):
        raise InvalidDataError("invalid password")
    if not re.search("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,100}$", password):
        raise InvalidDataError("invalid password")

def validate_username(username):
    if not isinstance(username, str):
        raise InvalidDataError("invalid username")
    if not re.search("^[A-Za-z][A-Za-z0-9_]{4,30}$", username):
        raise InvalidDataError("invalid username")

def validate_title(title):
    if not isinstance(title, str):
        raise InvalidDataError("invalid input")
    if not re.search("^[A-Za-z0-9_ ]{1,100}$", title):
        raise InvalidDataError("invalid input")

def validate_id(id):
    if not isinstance(id, str):
        raise InvalidDataError("invalid id")
    if not re.search("^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$", id): 
        raise InvalidDataError("invalid id")

def validate_date(date):
    if not isinstance(date, str):
        raise InvalidDataError("invalid date")
    if not re.search("(\d{4}-\d{2}-\d{2})", date):
        raise InvalidDataError("invalid date")