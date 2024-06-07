from app.db_mysql import db_pool
from app.error_handling import NotFoundException, NotEmptyError
from app.models.entry.Entry import Entry
from app.models.entry.Topic import Topic
from app.routes.schemas.category_schemas.CreateCategorySchema import CreateCategorySchema
from app.routes.schemas.category_schemas.UpdateCategorySchema import UpdateCategorySchema
from app.validation import validate_name
from app.utils.utils import uuid_generator

db = db_pool.acquire()


def get_all_categories_by_user(user_id: str):
    category_ids = db.retrieve_all_by_id(db.retrieve_all_categories_sql, (user_id,))
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

    def create(self, user_id: str, data: CreateCategorySchema):
        self.set_name(data.name)
        self.id = uuid_generator()
        db.create_update_delete(db.create_category_sql, (self.id, user_id, self.name))
        self.entry_type = "category"
        self.load_by_id(self.id, user_id)
        return self, "category created"

    def delete(self, user_id: str):
        if len(self.topics) > 0:
            raise NotEmptyError("cannot delete while there are topics in this category")
        db.create_update_delete(db.delete_category_sql, (self.id, user_id))
        return "category deleted"

    def load_by_id(self, id: str, user_id: str):
        result = db.retrieve(db.retrieve_category_sql, (id, user_id))
        if result is None:
            raise NotFoundException
        self.id, self.name = result
        self.entry_type = "category"
        self.topics = self.load_topics(user_id)

    def update(self, user_id: str, data: UpdateCategorySchema):
        self.set_name(data.name)
        db.create_update_delete(db.update_category_sql, (self.name, self.id, user_id))
        return self, "category updated"

    def set_name(self, name: str):
        validate_name(name)
        self.name = name

    def load_topics(self, user_id: str):
        topic_ids = db.retrieve_all_by_id(db.retrieve_topic_ids_by_category_sql, (self.id, user_id))
        topics = []
        for id in topic_ids:
            topic = Topic()
            topic.load_by_id(id[0], user_id)
            topics.append(topic)
        return topics
