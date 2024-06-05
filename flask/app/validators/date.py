import re

from app.constants.ExceptionMessages import ExceptionMessages


def validate_date(date: str):
    if not isinstance(date, str):
        raise ValueError("not a string")
    if not re.search("([a-zA-Z]{3}-\d{2}\/\d{2}\/\d{4})", date):
        raise ValueError(ExceptionMessages.DATE_NOT_VALID)
