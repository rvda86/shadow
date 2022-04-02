from shadow.utils import uuid_generator
from shadow.error_handling import UsernameOrEmailTakenError, InvalidPasswordError, NotFoundError
from shadow.validation import validate_email, validate_password, validate_username
from shadow.logging import get_user_logger
from shadow import bcrypt
from flask_jwt_extended import create_access_token
from shadow.db_mysql import db_pool

logger = get_user_logger()

db = db_pool.acquire()

def get_all_usernames_emails():
    existing_usernames = [record[0] for record in db.retrieve_all(db.retrieve_all_usernames_sql)]
    existing_emails = [record[0] for record in db.retrieve_all(db.retrieve_all_emails_sql)]
    return existing_usernames, existing_emails

class User:    

    id: str
    username: str
    email: str
    password: str
    authenticated: bool
    email_verified: bool

    def __init__(self):
        self.id = None
        self.username = None
        self.email = None
        self.password = None
        self.email_verified = False
        self.authenticated = False

    def load_by_email(self, email: str):
        result = db.retrieve(db.retrieve_user_by_email_sql, (email, ))
        if result is None:
            raise NotFoundError
        self.id, self.username, self.email, self.password, self.email_verified = result
        if self.email_verified == "1":
            self.email_verified = True

    def load_by_username(self, username: str):
        result = db.retrieve(db.retrieve_user_by_username_sql, (username, ))
        if result is None:
            raise NotFoundError
        self.id, self.username, self.email, self.password, self.email_verified = result
        if self.email_verified == "1":
            self.email_verified = True

    def load_by_id(self, user_id: str):
        result = db.retrieve(db.retrieve_user_by_id_sql, (user_id, ))
        if result is None:
            raise NotFoundError
        self.id, self.username, self.email, self.password, self.email_verified = result
        if self.email_verified == "1":
            self.email_verified = True

    def create(self, data: dict):
        self.set_username(data["username"])
        self.set_email(data["email"])
        self.set_password(data["password"])    
        self.id = uuid_generator()   
        db.create_update_delete(db.create_user_sql, (self.id, self.username, self.email, self.password))
        logger.info(f'USER CREATED: {self.id} Username: {self.get_username()} Email: {self.get_email()}')
        return {"msg": "account successfully created"}

    def update(self, user_id: str, data: dict):
        if self.authenticated:
            self.set_username(data["username"])
            self.set_email(data["email"])
            self.set_password(data["password"])  
            db.create_update_delete(db.update_user_sql, (self.username, self.email, self.password, user_id))
            logger.info(f'USER UPDATED: {self.id} Username: {self.get_username()} Email: {self.get_email()}')
            return {"msg": "account successfully updated"}
        return {"msg": "not authenticated"}

    def delete(self, user_id: str):      
        if self.authenticated: 
            queries = [db.delete_all_journal_entries_user_sql, 
                        db.delete_all_todo_entries_user_sql, 
                        db.delete_all_habit_entries_user_sql,
                        db.delete_all_topics_user_sql,
                        db.delete_all_categories_user_sql,
                        db.delete_user_by_id_sql]
            db.create_update_delete(queries, (user_id, ))
            logger.info(f'USER DELETED: {self.id} Username: {self.get_username()} Email: {self.get_email()}')
            return {"msg": "account successfully deleted"}
        return {"msg": "not authenticated"}

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_id(self):
        return self.id

    def set_username(self, username: str):
        validate_username(username)
        username = username.lower()
        existing_usernames = [record[0] for record in db.retrieve_all(db.retrieve_all_usernames_sql)]
        if username in existing_usernames:
            if self.username is None:
                raise UsernameOrEmailTakenError("username")
            else: 
                if username != self.username:
                    raise UsernameOrEmailTakenError("username")
        self.username = username

    def set_email(self, email: str):
        validate_email(email)
        existing_emails = [record[0] for record in db.retrieve_all(db.retrieve_all_emails_sql)]
        if email in existing_emails:
            if self.email is None:
                raise UsernameOrEmailTakenError("email")
            else: 
                if email != self.email:
                    raise UsernameOrEmailTakenError("email")
        self.email = email

    def set_password(self, password: str):
        validate_password(password)
        self.password = bcrypt.generate_password_hash(password)

    def set_email_verified(self, verified: bool):
        self.email_verified = verified

    def get_email_verified(self):
        return self.email_verified

    def update_email_verification_status(self):
        if self.email_verified:
            email_verified = "1"
        if not self.email_verified:
            email_verified = "0"
        db.create_update_delete(db.update_email_verification_status_sql, (email_verified, self.get_id()))
        logger.info(f'USER EMAIL VERIFICATION UPDATED: {self.id} Username: {self.get_username()} Email: {self.get_email()} Email-verified {self.get_email_verified()}')
        return {"msg": "email verification status has been updated"}

    def update_password_password_reset(self):
        db.create_update_delete(db.update_password_sql, (self.password, self.get_id()))
        logger.info(f'USER PASSWORD RESET: {self.id} Username: {self.get_username()} Email: {self.get_email()}')
        return {"msg": "password has been updated"}

    def authenticate(self, password: str):
        if not bcrypt.check_password_hash(self.password, password):
            raise InvalidPasswordError
        self.authenticated = True

    def get_token(self):
        if self.authenticated:
            access_token = create_access_token(identity=self.id)
            return {"access_token":access_token}