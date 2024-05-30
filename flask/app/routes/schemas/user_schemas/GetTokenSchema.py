from app.validators.password import validate_password
from app.validators.username import validate_username


class GetTokenSchema:

    def __init__(self, username: str, password: str):
        self.username = validate_username(username)
        self.password = validate_password(password)
