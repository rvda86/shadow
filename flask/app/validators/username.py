from app.constants.ExceptionMessages import ExceptionMessages
from app.constants.ValidationConstants import ValidationConstants
from app.validators.string import string_is_too_short, string_is_too_long, string_is_not_alphanumeric


def validate_username(username: str) -> str:
    if not isinstance(username, str):
        raise ValueError("not a string")
    if string_is_not_alphanumeric(username):
        raise ValueError(ExceptionMessages.USERNAME_ILLEGAL_CHARACTERS)
    if string_is_too_short(ValidationConstants.MIN_USERNAME_LENGTH, username):
        raise ValueError(ExceptionMessages.USERNAME_TOO_SHORT)
    if string_is_too_long(ValidationConstants.MAX_USERNAME_LENGTH, username):
        raise ValueError(ExceptionMessages.USERNAME_TOO_LONG)
    return username
