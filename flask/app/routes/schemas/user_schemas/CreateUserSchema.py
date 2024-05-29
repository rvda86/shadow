from app.validators.email import validated_email
from app.validators.password import validated_password
from app.validators.username import validated_username


class CreateUserSchema:

    def __init__(self, email, password, username):
        self.email = validated_email(email)
        self.password = validated_password(password)
        self.username = validated_username(username)
