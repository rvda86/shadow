from shadow.utils import uuid_generator
from shadow.error_handling import UsernameOrEmailTakenError, InvalidPasswordError, NotFoundError
from shadow import bcrypt
from flask_jwt_extended import create_access_token
from shadow.db_mysql import db_pool

db = db_pool.acquire()

def get_all_usernames_emails():
    existing_usernames = [record[0] for record in db.retrieve_all_records(db.retrieve_all_usernames_sql)]
    existing_emails = [record[0] for record in db.retrieve_all_records(db.retrieve_all_user_emails_sql)]
    return existing_usernames, existing_emails

class User:    

    def __init__(self):
        pass

    def set_values(self, data):
        self.username = data["username"].lower()
        self.email = data["email"]
        self.password = data["password"]

    def load_data_by_username(self, username):
        result = db.retrieve_record(db.retrieve_user_by_username_sql, (username, ))
        if result is None:
            raise NotFoundError
        self.id, self.username, self.email, self.password = result

    def load_data_by_id(self, id):
        result = db.retrieve_record(db.retrieve_user_by_id_sql, (id, ))
        if result is None:
            raise NotFoundError
        self.id, self.username, self.email, self.password = result

    def create(self):
        existing_usernames = [record[0] for record in db.retrieve_all_records(db.retrieve_all_usernames_sql)]
        existing_emails = [record[0] for record in db.retrieve_all_records(db.retrieve_all_user_emails_sql)]
        if self.username in existing_usernames or self.email in existing_emails:
            raise UsernameOrEmailTakenError
        self.id = uuid_generator()
        self.password = bcrypt.generate_password_hash(self.password)
        db.create_update_delete_record(db.create_user_sql, (self.id, self.username, self.email, self.password))
        return {"msg": "account successfully created"}

    def update(self):
        self.password = bcrypt.generate_password_hash(self.password)
        db.create_update_delete_record(db.update_user_sql, (self.username, self.email, self.password, self.id))
        return {"msg": "account successfully updated"}

    def delete(self):
        db.create_update_delete_record(db.delete_all_journal_entries_user_sql, (self.id, ))
        db.create_update_delete_record(db.delete_all_todo_entries_user_sql, (self.id, ))
        db.create_update_delete_record(db.delete_all_topics_user_sql, (self.id, ))
        db.create_update_delete_record(db.delete_all_categories_user_sql, (self.id, ))
        db.create_update_delete_record(db.delete_user_by_id_sql, (self.id, ))
        return {"msg": "account successfully deleted"}

    def fetchUserData(self):
        return {"username": self.username, "email": self.email}

    def authenticate(self, password):
        if not bcrypt.check_password_hash(self.password, password):
            raise InvalidPasswordError
        self.authenticated = True

    def get_token(self):
        if self.authenticated:
            access_token = create_access_token(identity=self.id)
            return {"access_token":access_token}

