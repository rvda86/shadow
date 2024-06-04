from app.constants.ExceptionMessages import ExceptionMessages
from app.validators.string import string_is_not_alphanumeric, string_is_too_short, string_is_too_long


def validate_name(name, min_length, max_length):
    if not isinstance(name, str):
        raise ValueError("not a string")
    if string_is_not_alphanumeric(name):
        raise ValueError(ExceptionMessages.NAME_ILLEGAL_CHARACTERS)
    if string_is_too_short(min_length, name):
        raise ValueError(ExceptionMessages.NAME_TOO_SHORT)
    if string_is_too_long(max_length, name):
        raise ValueError(ExceptionMessages.NAME_TOO_LONG)

    return name
