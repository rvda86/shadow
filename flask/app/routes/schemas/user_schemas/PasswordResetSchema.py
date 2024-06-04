from app.validators.password import validate_password


class PasswordResetSchema:

    def __init__(self, password: str):
        self.password = validate_password(password)
