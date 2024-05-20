from datetime import datetime

from app.db_mysql import db_pool
from app.error_handling import InvalidDataError, NotFoundException
from app.models.entry.Entry import Entry
from app.validation import validate_id, validate_name
from app.utils.utils import uuid_generator

db = db_pool.acquire()


class ToDo(Entry):
    id: str
    topic_id: str
    date_posted: str
    date_edited: str
    task: str
    completed: str
    entry_type: str

    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_todo_entry_sql, (id, user_id))
        if result is None:
            raise NotFoundException
        self.id, self.topic_id, self.date_posted, self.date_edited, self.task, self.completed = result
        self.entry_type = "todo"

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        self.set_topic(data["topic_id"])
        self.set_task(data["task"])
        db.create_update_delete(db.create_todo_entry_sql,
                                (self.id, user_id, self.topic_id, self.date_posted, self.task))
        self.load_by_id(self.id, user_id)
        return self, "todo entry created"

    def update(self, user_id: str, data: dict):
        self.date_edited = datetime.utcnow()
        self.set_task(data["task"])
        self.set_completed(data["completed"])
        db.create_update_delete(db.update_todo_entry_sql,
                                (self.date_edited, self.task, self.completed, self.id, user_id))
        return self, "todo entry updated"

    def delete(self, user_id: str):
        db.create_update_delete(db.delete_todo_entry_sql, (self.id, user_id))
        return "todo entry deleted"

    def set_topic(self, id: str):
        validate_id(id)
        self.topic_id = id

    def set_task(self, task: str):
        validate_name(task)
        self.task = task

    def set_completed(self, completed: str):
        if completed not in ["0", "1"]:
            raise InvalidDataError("invalid value")
        self.completed = completed
