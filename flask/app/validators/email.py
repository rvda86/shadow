import re

from app.constants.ExceptionMessages import ExceptionMessages


def validate_email(email) -> str:
    if not isinstance(email, str):
        raise ValueError("not a string")
    if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        raise ValueError(ExceptionMessages.EMAIL_NOT_VALID)
    return email
