from datetime import datetime

from app.db_mysql import db_pool
from app.error_handling import InvalidDataError, NotFoundException
from app.models.entry.Entry import Entry
from app.models.entry.Tag import Tag
from app.routes.schemas.journal_schemas.CreateJournalSchema import CreateJournalSchema
from app.routes.schemas.journal_schemas.UpdateJournalSchema import UpdateJournalSchema
from app.validation import validate_id, validate_title
from app.utils.utils import uuid_generator

db = db_pool.acquire()


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
            raise NotFoundException
        self.id, self.topic_id, self.date_posted, self.date_edited, self.title, self.content = result
        self.entry_type = "journal"
        self.tags = self.load_tags(user_id)

    def load_tags(self, user_id: str):
        tag_ids = db.retrieve_all_by_id(db.retrieve_tag_ids_by_user_sql, (user_id,))
        tags = []
        for id in tag_ids:
            tag = Tag()
            tag.load_by_id(id[0], user_id)
            tags.append(tag)

    def create(self, user_id: str, data: CreateJournalSchema):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        self.set_topic(data.topic_id)
        self.set_title(data.title)
        self.set_content(data.content)
        db.create_update_delete(db.create_journal_entry_sql,
                                (self.id, user_id, self.topic_id, self.date_posted, self.title, self.content))
        self.load_by_id(self.id, user_id)
        return self, "journal entry created"

    def update(self, user_id: str, data: UpdateJournalSchema):
        self.date_edited = datetime.utcnow()
        self.set_title(data.title)
        self.set_content(data.content)
        db.create_update_delete(db.update_journal_entry_sql,
                                (self.date_edited, self.title, self.content, self.id, user_id))
        return self, "journal entry updated"

    def delete(self, user_id: str):
        db.create_update_delete(db.delete_journal_entry_sql, (self.id, user_id))
        return "journal entry deleted"

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
