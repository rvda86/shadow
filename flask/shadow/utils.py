import uuid
from flask_mail import Message
from shadow import mail
from shadow.config import Config
from flask_jwt_extended import create_access_token

def uuid_generator():
    return str(uuid.uuid4())

def send_email_verification_mail(user):
    access_token = create_access_token(identity=user.get_email())
    html = f"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
	        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
	        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
        <h2>Welcome to Shadow</h2>
        <p>Please verify your email address by clicking on this link: <a href="{Config.EMAIL_VERIFICATION_LINK}?token={access_token}">Verify my email</a>
        </body>
        </html>
    """
    msg = Message(subject="Welcome to Shadow", 
            html=html, 
            sender=Config.MAIL_DEFAULT_SENDER,
            recipients=[user.get_email()])
    try:
        mail.send(msg)
        return "Verification email send"
    except ConnectionRefusedError:
        return "Failed to send verification email"

def send_password_reset_mail(user):
    if user.get_email_verified():
        access_token = create_access_token(identity=user.get_email())
        html = f"""
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>
            <h2>Password Reset</h2>
            <p>Please click the following link to reset your password: <a href="{Config.PASSWORD_RESET_LINK}?token={access_token}">Reset password</a>
            </body>
            </html>
        """
        try:
            msg = Message(f"Password reset for Shadow", 
                    html=html,
                    sender=Config.MAIL_DEFAULT_SENDER,
                    recipients=[user.get_email()])
            mail.send(msg)
            return "Password reset email sent, please check your email to reset your password"
        except ConnectionRefusedError:
            return "Failed to send reset password email"
    return "Cannot send password reset email, email not verified"