from app.constants.ExceptionMessages import ExceptionMessages
from app.constants.ValidationConstants import ValidationConstants
from app.validators.string import string_is_too_short, string_is_too_long


def validate_password(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("not a string")
    if string_is_too_short(ValidationConstants.MIN_PASSWORD_LENGTH, password):
        raise ValueError(ExceptionMessages.PASSWORD_TOO_SHORT)
    if string_is_too_long(ValidationConstants.MAX_PASSWORD_LENGTH, password):
        raise ValueError(ExceptionMessages.PASSWORD_TOO_LONG)
    if password_is_too_common(password):
        raise ValueError(ExceptionMessages.PASSWORD_TOO_COMMON)
    if password_is_entirely_numeric(password):
        raise ValueError(ExceptionMessages.PASSWORD_NUMERIC)
    return password


def password_is_entirely_numeric(password: str) -> bool:
    if len(password) == 0:
        return False
    for char in password:
        if char not in "1234567890":
            return False
    return True


def password_is_too_common(password: str) -> bool:
    return password in ValidationConstants.COMMON_PASSWORDS
