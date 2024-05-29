from app.validators.email import validate_email
from app.validators.password import validate_password
from app.validators.username import validate_username


class UpdateUserSchema:

    def __init__(self, currentPassword, email, password, username):
        self.currentPassword = validate_password(currentPassword)
        self.email = validate_email(email)
        self.password = validate_password(password)
        self.username = validate_username(username)
