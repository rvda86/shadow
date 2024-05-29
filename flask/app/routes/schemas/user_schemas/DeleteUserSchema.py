from app.validators.password import validate_password


class DeleteUserSchema:

    def __init__(self, password):
        self.password = validate_password(password)
