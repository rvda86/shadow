from app.db_mysql import db_pool
from app.error_handling import InvalidDataError, NotFoundException, NotEmptyError
from app.models.entry.Entry import Entry
from app.models.entry.Habit import Habit
from app.models.entry.Journal import Journal
from app.models.entry.ToDo import ToDo
from app.validation import validate_id, validate_name
from app.utils.utils import uuid_generator

db = db_pool.acquire()


class Topic(Entry):

    id: str
    category_id: str
    name: str
    topic_type: str
    entry_type: str
    entries: list
    
    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_topic_sql, (id, user_id))
        if result is None:
            raise NotFoundException
        self.id, self.category_id, self.name, self.topic_type = result
        self.entry_type = "topic"    
        self.entries = self.load_entries(user_id)

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        self.set_category(data["category_id"])
        self.set_name(data["name"])
        self.set_topic_type(data["topic_type"])
        db.create_update_delete(db.create_topic_sql, (self.id, user_id, self.category_id, self.name, self.topic_type))
        self.load_by_id(self.id, user_id)
        return self, "topic created"
            
    def update(self, user_id: str, data: dict):
        self.set_name(data["name"])
        db.create_update_delete(db.update_topic_sql, (self.name, self.id, user_id))
        return self, "topic updated"
    
    def delete(self, user_id: str):
        if len(self.entries) > 0:
            raise NotEmptyError("cannot delete while there are entries in this topic")
        db.create_update_delete(db.delete_topic_sql, (self.id, user_id))
        return "topic deleted"

    def set_name(self, name: str):
        validate_name(name)
        self.name = name
    
    def set_topic_type(self, topic_type: str):
        if topic_type not in ["journal", "todo", "habit"]:
            raise InvalidDataError("invalid topic type")
        self.topic_type = topic_type
    
    def set_category(self, id: str):
        validate_id(id)
        self.category_id = id
    
    def load_entries(self, user_id: str):
        if self.topic_type == "todo":
            return self.load_todo_entries(user_id)
        if self.topic_type == "journal":
            return self.load_journal_entries(user_id)
        if self.topic_type == "habit":
            return self.load_habit_entries(user_id)

    def load_journal_entries(self, user_id: str):
        entries_ids = db.retrieve_all_by_id(db.retrieve_journal_ids_by_topic_sql, (self.id, user_id))
        entries = []
        for id in entries_ids:
            entry = Journal()
            entry.load_by_id(id[0], user_id)
            entries.append(entry)
        return entries

    def load_todo_entries(self, user_id: str):
        entries_ids = db.retrieve_all_by_id(db.retrieve_todo_ids_by_topic_sql, (self.id, user_id))
        entries = []
        for id in entries_ids:
            entry = ToDo()
            entry.load_by_id(id[0], user_id)
            entries.append(entry)
        return entries

    def load_habit_entries(self, user_id: str):
        entries_ids = db.retrieve_all_by_id(db.retrieve_habit_ids_by_topic_sql, (self.id, user_id))
        entries = []
        for id in entries_ids:
            entry = Habit()
            entry.load_by_id(id[0], user_id)
            entries.append(entry)
        return entries
