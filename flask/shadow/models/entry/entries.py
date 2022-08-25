from abc import ABC, abstractmethod
from datetime import datetime
from shadow.validation import validate_title, validate_id, validate_date
from shadow.utils import uuid_generator
from shadow.db_mysql import db_pool
from shadow.error_handling import InvalidDataError, NotFoundError, TopicNotEmptyError

db = db_pool.acquire()

class Entry(ABC):

    @abstractmethod
    def load_by_id(self, entry_id: str, user_id: str):
        pass

    @abstractmethod
    def create(self, user_id: str, data: dict):
        pass

    @abstractmethod
    def update(self, user_id: str, data: dict):
        pass

    @abstractmethod
    def delete(self, user_id: str, data: dict):
        pass

def to_dict(obj):
    dictionary = obj.__dict__
    for k, v in dictionary.items():
        if isinstance(v, list):            
            dictionary[k] = [to_dict(item) if isinstance(item, Entry) else item for item in v]
    return dictionary

def get_all_categories_by_user(user_id: str):
    category_ids = db.retrieve_all_by_id(db.retrieve_all_categories_sql, (user_id, ))
    categories = []
    for id in category_ids:
        category = Category()
        category.load_by_id(id[0], user_id)
        categories.append(category)
    return categories

class Category(Entry):

    id: str
    name: str
    entry_type: str
    topics: list 
    
    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_category_sql, (id, user_id))
        if result == None:
            raise NotFoundError
        self.id, self.name = result
        self.entry_type = "category" 
        self.topics = self.load_topics(user_id)

    def create(self, user_id: str, data: dict):
        self.set_name(data["name"])
        self.id = uuid_generator()
        db.create_update_delete(db.create_category_sql, (self.id, user_id, self.name))
        self.entry_type = "category" 
        self.load_by_id(self.id, user_id)
        return self, "category successfully created"
    
    def update(self, user_id: str, data: dict):
        self.set_name(data["name"])
        db.create_update_delete(db.update_category_sql, (self.name, self.id, user_id))
        return self, "category successfully updated"

    def delete(self, user_id: str):
        db.create_update_delete(db.delete_category_sql, (self.id, user_id))
        return "category successfully deleted"
    
    def set_name(self, name: str):
        validate_title(name)
        self.name = name

    def load_topics(self, user_id: str):
        topic_ids = db.retrieve_all_by_id(db.retrieve_topic_ids_by_category_sql, (self.id, user_id))
        topics = []
        for id in topic_ids:
            topic = Topic()
            topic.load_by_id(id[0], user_id)
            topics.append(topic)
        return topics

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
            raise NotFoundError
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
        return self, "topic successfully created"
            
    def update(self, user_id: str, data: dict):
        self.set_name(data["name"])
        db.create_update_delete(db.update_topic_sql, (self.name, self.id, user_id))
        return self, "topic successfully updated"
    
    def delete(self, user_id: str):
        if len(self.entries) > 0:
            raise TopicNotEmptyError
        db.create_update_delete(db.delete_topic_sql, (self.id, user_id))
        return "topic successfully deleted"

    def set_name(self, name: str):
        validate_title(name)
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

class Journal(Entry):

    id: str
    topic_id: str
    date_posted: str
    date_edited: str
    title: str
    content: str
    entry_type: str
    tags: list
    
    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_journal_entry_sql, (id, user_id))
        if result is None:
            raise NotFoundError
        self.id, self.topic_id, self.date_posted, self.date_edited, self.title, self.content = result
        self.entry_type = "journal"
        self.tags = self.load_tags(user_id)

    def load_tags(self, user_id: str):
        tag_ids = db.retrieve_all_by_id(db.retrieve_tag_ids_by_user_sql, (user_id, ))
        tags = [] 
        for id in tag_ids:
            tag = Tag()
            tag.load_by_id(id[0], user_id)
            tags.append(tag)

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        self.set_topic(data["topic_id"])
        self.set_title(data["title"])
        self.set_content(data["content"])
        db.create_update_delete(db.create_journal_entry_sql, (self.id, user_id, self.topic_id, self.date_posted, self.title, self.content))
        self.load_by_id(self.id, user_id)
        return self, "entry successfully created"
    
    def update(self, user_id: str, data: dict):
        self.date_edited = datetime.utcnow()
        self.set_title(data["title"])
        self.set_content(data["content"])
        db.create_update_delete(db.update_journal_entry_sql, (self.date_edited, self.title, self.content, self.id, user_id))
        return self, "entry successfully updated"
   
    def delete(self, user_id: str):
        db.create_update_delete(db.delete_journal_entry_sql, (self.id, user_id))
        return "entry successfully deleted"

    def set_title(self, title: str):
        validate_title(title)
        self.title = title

    def set_content(self, content: str):
        if len(content) > 65535:
            raise InvalidDataError("post is too long")
        self.content = content

    def set_topic(self, id: str):
        validate_id(id)
        self.topic_id = id

class ToDo(Entry):

    id: str
    topic_id: str
    date_posted: str
    date_edited: str
    task: str
    due_date: str
    completed: str
    entry_type: str
    
    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_todo_entry_sql, (id, user_id))
        if result is None:
            raise NotFoundError
        self.id, self.topic_id, self.date_posted, self.date_edited, self.task, self.due_date, self.completed = result
        self.entry_type = "todo"

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        self.set_topic(data["topic_id"])
        self.set_task(data["task"])
        self.set_due_date(data["due_date"])
        db.create_update_delete(db.create_todo_entry_sql, (self.id, user_id, self.topic_id, self.date_posted, self.task, self.due_date))
        self.load_by_id(self.id, user_id)
        return self, "entry successfully created"

    def update(self, user_id: str, data: dict):
        self.date_edited = datetime.utcnow()
        self.set_task(data["task"])
        self.set_due_date(data["due_date"])
        self.set_completed(data["completed"])
        db.create_update_delete(db.update_todo_entry_sql, (self.date_edited, self.task, self.due_date, self.completed, self.id, user_id))
        return self, "entry successfully updated"
 
    def delete(self, user_id: str):
        db.create_update_delete(db.delete_todo_entry_sql, (self.id, user_id))
        return "entry successfully deleted"

    def set_topic(self, id: str):
        validate_id(id)
        self.topic_id = id

    def set_task(self, task: str):
        validate_title(task)
        self.task = task

    def set_due_date(self, date: str):
        validate_date(date)
        self.due_date = date

    def set_completed(self, completed: str):
        if completed not in ["0", "1"]:
            raise InvalidDataError("invalid value")
        self.completed = completed

class Habit(Entry):

    id: str
    topic_id: str
    date_posted: str
    date_edited: str
    name: str
    days_completed: list
    entry_type: str
    
    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_habit_entry_sql, (id, user_id))
        if result is None:
            raise NotFoundError
        self.id, self.topic_id, self.date_posted, self.date_edited, self.name = result
        self.entry_type = "habit"
        self.days_completed = self.load_days_completed(user_id)

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        self.set_topic(data["topic_id"])
        self.set_name(data["name"])
        db.create_update_delete(db.create_habit_entry_sql, (self.id, user_id, self.topic_id, self.date_posted, self.name))
        self.load_by_id(self.id, user_id)
        return self, "entry successfully created"

    def update(self, user_id: str, data: dict):
        self.date_edited = datetime.utcnow()
        self.set_name(data["name"])
        db.create_update_delete(db.update_habit_entry_sql, (self.date_edited, self.name, self.id, user_id))
        for day in data["days_completed"]:
            if day not in self.days_completed:
                db.create_update_delete(db.create_habit_days_completed_sql, (user_id, self.id, day))
        for day in self.days_completed:
            if day not in data["days_completed"]:
                db.create_update_delete(db.delete_habit_days_completed_sql, (self.id, user_id))
        self.set_days_completed(data["days_completed"])
        return self, "entry successfully updated"

    def delete(self, user_id: str):
        db.create_update_delete(db.delete_habit_entry_sql, (self.id, user_id))
        return "entry successfully deleted"
 
    def load_days_completed(self, user_id: str):
        days_completed = db.retrieve(db.retrieve_habit_days_completed_sql, (self.id, user_id))
        if days_completed is None:
            return []
        return list(days_completed)
    
    def set_days_completed(self, days_completed: list):
        for day in days_completed:
            validate_date(day)
        self.days_completed = days_completed
    
    def set_topic(self, id: str):
        validate_id(id)
        self.topic_id = id

    def set_name(self, name: str):
        validate_title(name)
        self.name = name

class Tag(Entry):
    id: str
    name: str
    
    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_tag_sql, (id, user_id))
        if result is None:
            raise NotFoundError
        self.id, self.name = result
        self.entry_type = "tag"

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        user_tags = db.retrieve(db.retrieve_tags_by_user_sql, (user_id, ))
        if user_tags is None:
            user_tags = []
        if data["name"] not in user_tags:
            self.set_name(data["name"])
            db.create_update_delete(db.create_tag_sql, (self.id, user_id, self.name))
        self.load_by_id(self.id, user_id)
        return self, "tag successfully created"

    def update(self, user_id: str, data: dict):
        user_tags = db.retrieve(db.retrieve_tags_by_user_sql, (user_id, ))
        if user_tags is not None and data["name"] not in user_tags:
            self.set_name(data["name"])
            db.create_update_delete(db.update_tag_sql, (self.name, self.id, user_id))
        return self, "tag successfully updated"

    def delete(self, user_id: str):
        db.create_update_delete(db.delete_tag_sql, (self.id, user_id))
        return "tag successfully deleted"
 
    def set_name(self, name: str):
        validate_title(name)
        self.name = name