from abc import ABC, abstractmethod
from datetime import datetime
from shadow.utils import uuid_generator
from shadow.db_mysql import db_pool
from shadow.error_handling import db_error_handler, NotFoundError

db = db_pool.acquire()


class Entry(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def set_values(self, data, user_id):
        pass

    @abstractmethod
    def load_data(self, entry_id, user_id):
        pass

    @abstractmethod
    def create(self, user_id):
        pass

    @abstractmethod
    def update(self, user_id):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass

@db_error_handler
def get_all_categories_by_user(user_id):
    category_ids = db.retrieve_all_records_by_id(db.retrieve_all_categories_sql, (user_id, ))
    categories = []
    for id in category_ids:
        category = EntryCategory()
        category.load_data(id[0], user_id)
        categories.append(category)
    return categories

class EntryCategory(Entry):

    id: str
    user_id: str
    name: str
    entry_type: str
    topics: tuple 

    def set_values(self, data, user_id):
        self.name = data["name"]
        self.user_id = user_id
    
    @db_error_handler
    def load_data(self, id, user_id):
        result = db.retrieve_record(db.retrieve_category_sql, (id, user_id))
        if result == None:
            raise NotFoundError
        self.id, self.name = result
        self.entry_type = "category" 
        self.topics = self.get_all_topics_by_category(user_id)

    @db_error_handler
    def create(self, user_id):
        self.id = uuid_generator()
        db.create_update_delete_record(db.create_category_sql, (self.id, user_id, self.name))
        return "category successfully created"

    @db_error_handler
    def update(self, user_id):
        db.create_update_delete_record(db.update_category_sql, (self.name, self.id, user_id))
        return "category successfully updated"

    @db_error_handler
    def delete(self, user_id):
        db.create_update_delete_record(db.delete_category_sql, (self.id, user_id))
        return "category successfully deleted"

    @db_error_handler
    def get_all_topics_by_category(self, user_id):
        topic_ids = db.retrieve_all_records_by_id(db.retrieve_topic_ids_by_category_sql, (self.id, user_id))
        topics = []
        for id in topic_ids:
            topic = EntryTopic()
            topic.load_data(id[0], user_id)
            topics.append(topic)
        return topics

class EntryTopic(Entry):

    id: str
    user_id: str
    category_id: str
    name: str
    topic_type: str
    entry_type: str
    entries: tuple

    def set_values(self, data, user_id):
        self.name = data["name"]
        self.user_id = user_id
        if "topic_type" in data: self.topic_type = data["topic_type"]
        if "category_id" in data: self.category_id = data["category_id"]

    @db_error_handler
    def load_data(self, id, user_id):
        result = db.retrieve_record(db.retrieve_topic_sql, (id, user_id))
        if result is None:
            raise NotFoundError
        self.id, self.category_id, self.name, self.topic_type = result
        self.entry_type = "topic"    
        self.entries = self.get_all_entries_by_topic(user_id)

    @db_error_handler
    def create(self, user_id):
        self.id = uuid_generator()
        db.create_update_delete_record(db.create_topic_sql, (self.id, user_id, self.category_id, self.name, self.topic_type))
        return "topic successfully created"

    @db_error_handler        
    def update(self, user_id):
        db.create_update_delete_record(db.update_topic_sql, (self.name, self.id, user_id))
        return "topic successfully updated"

    @db_error_handler
    def delete(self, user_id):
        db.create_update_delete_record(db.delete_topic_sql, (self.id, user_id))
        return "topic successfully deleted"

    @db_error_handler
    def get_all_entries_by_topic(self, user_id):
        sql = {"journal": db.retrieve_journal_ids_by_topic_sql, "todo": db.retrieve_todo_ids_by_topic_sql, "habit": ""} 
        entries_ids = db.retrieve_all_records_by_id(sql[self.topic_type], (self.id, user_id))
        entries = []
        for id in entries_ids:
            entry_objs = {"journal": EntryJournal(), "todo": EntryToDo()}
            entry = entry_objs[self.topic_type]
            entry.load_data(id[0], user_id)
            entries.append(entry)
        return entries

class EntryJournal(Entry):

    id: str
    user_id: str
    topic_id: str
    date_posted: str
    date_edited: str
    title: str
    content: str
    entry_type: str

    def set_values(self, data, user_id):
        self.title = data["title"]
        self.content = data["content"]
        self.user_id = user_id
        if "topic_id" in data: self.topic_id = data["topic_id"]

    @db_error_handler
    def load_data(self, id, user_id):
        result = db.retrieve_record(db.retrieve_journal_entry_sql, (id, user_id))
        if result is None:
            raise NotFoundError
        self.id, self.topic_id, self.date_posted, self.date_edited, self.title, self.content = result
        self.entry_type = "journal"

    @db_error_handler
    def create(self, user_id):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        db.create_update_delete_record(db.create_journal_entry_sql, (self.id, user_id, self.topic_id, self.date_posted, self.title, self.content))
        return "entry successfully created"

    @db_error_handler
    def update(self, user_id):
        self.date_edited = datetime.utcnow()
        db.create_update_delete_record(db.update_journal_entry_sql, (self.date_edited, self.title, self.content, self.id, user_id))
        return "entry successfully updated"

    @db_error_handler
    def delete(self, user_id):
        db.create_update_delete_record(db.delete_journal_entry_sql, (self.id, user_id))
        return "entry successfully deleted"

class EntryToDo(Entry):

    user_id: str
    
    def set_values(self, data, user_id):
        self.task = data["task"]
        self.due_date = data["due_date"]
        self.user_id = user_id
        if "completed" in data: self.completed = data["completed"]
        if "topic_id" in data: self.topic_id = data["topic_id"]

    @db_error_handler
    def load_data(self, id, user_id):
        result = db.retrieve_record(db.retrieve_todo_entry_sql, (id, user_id))
        if result is None:
            raise NotFoundError
        self.id, self.topic_id, self.date_posted, self.date_edited, self.task, self.due_date, self.completed = result
        self.entry_type = "todo"

    @db_error_handler
    def create(self, user_id):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        db.create_update_delete_record(db.create_todo_entry_sql, (self.id, user_id, self.topic_id, self.date_posted, self.task, self.due_date))
        return "entry successfully created"

    @db_error_handler
    def update(self, user_id):
        self.date_edited = datetime.utcnow()
        db.create_update_delete_record(db.update_todo_entry_sql, (self.date_edited, self.task, self.due_date, self.completed, self.id, user_id))
        return "entry successfully updated"
 
    @db_error_handler
    def delete(self, user_id):
        db.create_update_delete_record(db.delete_todo_entry_sql, (self.id, user_id))
        return "entry successfully deleted"


