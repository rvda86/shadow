import bleach
import re

from app.error_handling import InvalidDataError


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
                    "POST": ["type", "task", "topic_id"], 
                    "PUT": ["type", "task", "completed", "id"], 
                    "DELETE": ["type", "id"]},
        "habit": {  "GET": ["type", "id"],
                    "POST": ["type", "name", "topic_id"],
                    "PUT": ["type", "name", "days", "id"],
                    "DELETE": ["type", "id"]},
        "tag": {    "GET": ["type", "id"],
                    "POST": ["type", "name"], 
                    "PUT": ["type", "name", "id"], 
                    "DELETE": ["type", "id"]},
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
    check_keys(data, method)
    return data

def validate_title(title):
    if not isinstance(title, str):
        raise InvalidDataError("invalid title")
    if len(title) == 0:
        raise InvalidDataError("title is required")
    if not re.search("^[-a-zA-Z0-9!@#$&()`.+,/\" ]*$", title):
        raise InvalidDataError("invalid title")


def validate_name(name):
    if not isinstance(name, str):
        raise InvalidDataError("invalid name")
    if len(name) == 0:
        raise InvalidDataError("oops, no input")
    if not re.search("^[-a-zA-Z0-9!/_@#$&()`.+,/\" ]*$", name):
        raise InvalidDataError("invalid name")


def validate_id(id):
    if not isinstance(id, str):
        raise InvalidDataError("invalid id")
    if not re.search("^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$", id): 
        raise InvalidDataError("invalid id")


def validate_date(date):
    if not isinstance(date, str):
        raise InvalidDataError("invalid date")
    if not re.search("([a-zA-Z]{3}-\d{2}\/\d{2}\/\d{4})", date):
        print(date)
        raise InvalidDataError("invalid date")
