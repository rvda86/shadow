from app.validators.password import validate_password


class PasswordResetSchema:

    def __init__(self, password: str):
        self.email = validate_password(password)
