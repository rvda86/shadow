from app.db_mysql import db_pool
from app.error_handling import NotFoundException
from app.models.entry.Entry import Entry
from app.validation import validate_title
from app.utils.utils import uuid_generator

db = db_pool.acquire()


class Tag(Entry):
    id: str
    name: str

    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_tag_sql, (id, user_id))
        if result is None:
            raise NotFoundException
        self.id, self.name = result
        self.entry_type = "tag"

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        user_tags = db.retrieve(db.retrieve_tags_by_user_sql, (user_id,))
        if user_tags is None:
            user_tags = []
        if data["name"] not in user_tags:
            self.set_name(data["name"])
            db.create_update_delete(db.create_tag_sql, (self.id, user_id, self.name))
        self.load_by_id(self.id, user_id)
        return self, "tag created"

    def update(self, user_id: str, data: dict):
        user_tags = db.retrieve(db.retrieve_tags_by_user_sql, (user_id,))
        if user_tags is not None and data["name"] not in user_tags:
            self.set_name(data["name"])
            db.create_update_delete(db.update_tag_sql, (self.name, self.id, user_id))
        return self, "tag updated"

    def delete(self, user_id: str):
        db.create_update_delete(db.delete_tag_sql, (self.id, user_id))
        return "tag deleted"

    def set_name(self, name: str):
        validate_title(name)
        self.name = name
