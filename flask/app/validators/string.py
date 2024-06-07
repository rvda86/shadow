from app.constants.ExceptionMessages import ExceptionMessages


def validate_string(string, min_length, max_length):
    if not isinstance(string, str):
        raise ValueError("not a string")
    if string_is_too_short(min_length, string):
        raise ValueError(ExceptionMessages.NAME_TOO_SHORT)
    if string_is_too_long(max_length, string):
        raise ValueError(ExceptionMessages.NAME_TOO_LONG)

    return string


def string_is_not_alphanumeric(string: str) -> bool:
    for char in string:
        if not char.isalnum():
            return True
    return False


def string_is_too_long(max_length: int, string: str) -> bool:
    return len(string) > max_length


def string_is_too_short(min_length: int, string: str) -> bool:
    return len(string) < min_length
