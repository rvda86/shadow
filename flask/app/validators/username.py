from app.constants.ExceptionMessages import ExceptionMessages
from app.validators.string import string_is_too_short, string_is_too_long, string_is_not_alphanumeric

max_username_length = 30
min_username_length = 2


def validated_username(username: str) -> str:
    if not isinstance(username, str):
        raise ValueError("not a string")
    if string_is_not_alphanumeric(username):
        raise ValueError(ExceptionMessages.USERNAME_ILLEGAL_CHARACTERS)
    if string_is_too_short(min_username_length, username):
        raise ValueError(ExceptionMessages.USERNAME_TOO_SHORT)
    if string_is_too_long(max_username_length, username):
        raise ValueError(ExceptionMessages.USERNAME_TOO_LONG)
    return username

