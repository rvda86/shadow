from app.validators.email import validate_email


class PasswordResetRequestSchema:

    def __init__(self, email: str):
        self.email = validate_email(email)
