from app.constants.ExceptionMessages import ExceptionMessages
from app.error_handling import InvalidDataError
from app.validators.string import string_is_too_short, string_is_too_long, string_is_not_alphanumeric

max_username_length = 30
min_username_length = 2


def is_valid_username(username: str) -> bool:
    if not isinstance(username, str):
        raise InvalidDataError("not a string")
    if string_is_not_alphanumeric(username):
        raise InvalidDataError(ExceptionMessages.USERNAME_ILLEGAL_CHARACTERS)
    if string_is_too_short(min_username_length, username):
        raise InvalidDataError(ExceptionMessages.USERNAME_TOO_SHORT)
    if string_is_too_long(max_username_length, username):
        raise InvalidDataError(ExceptionMessages.USERNAME_TOO_LONG)
    username_is_valid = True
    return username_is_valid
