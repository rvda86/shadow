from app.constants.ExceptionMessages import ExceptionMessages
from app.validators.string import string_is_too_short, string_is_too_long

common_passwords = ["password", "12345678", "123456789", "baseball", "football", "qwertyuiop", "1234567890",
                    "superman", "1qaz2wsx", "trustno1", "jennifer", "sunshine", "iloveyou", "starwars",
                    "computer", "michelle", "11111111", "princess", "987654321", "qwerty123", "aa12345678",
                    "password1", "password123"]
max_password_length = 128
min_password_length = 8


def validate_password(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("not a string")
    if string_is_too_short(min_password_length, password):
        raise ValueError(ExceptionMessages.PASSWORD_TOO_SHORT)
    if string_is_too_long(max_password_length, password):
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
    return password in common_passwords
