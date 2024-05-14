def string_is_not_alphanumeric(string: str) -> bool:
    for char in string:
        if not char.isalnum():
            return True
    return False


def string_is_too_long(max_length: int, string: str) -> bool:
    return len(string) > max_length


def string_is_too_short(min_length: int, string: str) -> bool:
    return len(string) < min_length
