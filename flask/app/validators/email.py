import re

from app.constants.ExceptionMessages import ExceptionMessages


def is_valid_email(email):
    if not isinstance(email, str):
        raise ValueError("not a string")
    if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        raise ValueError(ExceptionMessages.EMAIL_NOT_VALID)
    email_valid = True
    return email_valid
