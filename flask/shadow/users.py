from shadow.utils import uuid_generator
from shadow.error_handling import UsernameOrEmailTakenError, InvalidPasswordError, NotFoundError
from shadow import bcrypt
from flask_jwt_extended import create_access_token
from shadow.db_mysql import db_pool

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

    def __init__(self):
        self.id = None
        self.username = None
        self.email = None
        self.password = None

    # load_tags?

    def load_by_username(self, username: str):
        result = db.retrieve(db.retrieve_user_by_username_sql, (username, ))
        if result is None:
            raise NotFoundError
        self.id, self.username, self.email, self.password = result

    def load_by_id(self, user_id: str):
        result = db.retrieve(db.retrieve_user_by_id_sql, (user_id, ))
        if result is None:
            raise NotFoundError
        self.id, self.username, self.email, self.password = result

    def create(self, data: dict):
        self.set_username(data["username"])
        self.set_email(data["email"])
        self.set_password(data["password"])    
        self.id = uuid_generator()   
        db.create_update_delete(db.create_user_sql, (self.id, self.username, self.email, self.password))
        return {"msg": "account successfully created"}

    def update(self, user_id: str, data: dict):
        self.set_username(data["username"])
        self.set_email(data["email"])
        self.set_password(data["password"])  
        db.create_update_delete(db.update_user_sql, (self.username, self.email, self.password, user_id))
        return {"msg": "account successfully updated"}

    def delete(self, user_id: str):       
        queries = [db.delete_all_journal_entries_user_sql, 
                    db.delete_all_todo_entries_user_sql, 
                    db.delete_all_habit_entries_user_sql,
                    db.delete_all_topics_user_sql,
                    db.delete_all_categories_user_sql,
                    db.delete_user_by_id_sql]
        db.create_update_delete(queries, (user_id, ))
        return {"msg": "account successfully deleted"}

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def set_username(self, username):
        username = username.lower()
        existing_usernames = [record[0] for record in db.retrieve_all(db.retrieve_all_usernames_sql)]
        if username in existing_usernames:
            if self.username is None:
                raise UsernameOrEmailTakenError("username")
            else: 
                if username != self.username:
                    raise UsernameOrEmailTakenError("username")
        self.username = username

    def set_email(self, email):
        existing_emails = [record[0] for record in db.retrieve_all(db.retrieve_all_emails_sql)]
        if email in existing_emails:
            if self.email is None:
                raise UsernameOrEmailTakenError("email")
            else: 
                if email != self.email:
                    raise UsernameOrEmailTakenError("email")
        self.email = email

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def authenticate(self, password):
        if not bcrypt.check_password_hash(self.password, password):
            raise InvalidPasswordError
        self.authenticated = True

    def get_token(self):
        if self.authenticated:
            access_token = create_access_token(identity=self.id)
            return {"access_token":access_token}