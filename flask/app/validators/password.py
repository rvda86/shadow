import re

from app.constants.ExceptionMessages import ExceptionMessages
from app.error_handling import InvalidDataError

common_passwords = ["password", "12345678", "123456789", "baseball", "football", "qwertyuiop", "1234567890",
                    "superman", "1qaz2wsx", "trustno1", "jennifer", "sunshine", "iloveyou", "starwars",
                    "computer", "michelle", "11111111", "princess", "987654321", "qwerty123", "aa12345678",
                    "password1", "password123"]
max_password_length = 128
min_password_length = 8


def validate_password(password: str) -> bool:
    if not isinstance(password, str):
        raise InvalidDataError("invalid password")
    if len(password) < min_password_length:
        raise InvalidDataError(ExceptionMessages.PASSWORD_TOO_SHORT)
    if len(password) > max_password_length:
        raise InvalidDataError(ExceptionMessages.PASSWORD_TOO_LONG)
    if password_is_too_common(password):
        raise InvalidDataError(ExceptionMessages.PASSWORD_TOO_COMMON)
    if password_is_entirely_numeric(password):
        raise InvalidDataError(ExceptionMessages.PASSWORD_NUMERIC)

    if re.search("^(.{0,7}|[^0-9]*|[^A-Za-z]*)$", password):
        raise InvalidDataError("invalid password")
    password_valid = True
    return password_valid


def password_is_entirely_numeric(password: str) -> bool:
    if len(password) == 0:
        return False
    for char in password:
        if char not in "1234567890":
            return False
    return True


def password_is_too_common(password: str) -> bool:
    return password in common_passwords