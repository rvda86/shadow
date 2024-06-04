import re

from app.constants.ExceptionMessages import ExceptionMessages


def validate_id(id):
    if not isinstance(id, str):
        raise ValueError("not a string")
    if not re.search("^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$", id):
        raise ValueError(ExceptionMessages.ID_NOT_VALID)

    return id
