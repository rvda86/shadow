from flask import jsonify
from shadow.entries import get_all_categories_by_user

def standard_strategy(entry, entry_id, user_id):
    entry.load_by_id(entry_id, user_id)
    entry = entry.__dict__
    return entry

def category_strategy(category, category_id, user_id):
    category.load_by_id(category_id, user_id)
    for topic in category.topics:
        topic.entries = [entry.__dict__ for entry in topic.entries]
    category.topics = [topic.__dict__ for topic in category.topics]
    category = category.__dict__            
    return category

def categories_strategy(user_id):
    categories = [category_strategy(category, category.id, user_id) for category in get_all_categories_by_user(user_id)]
    return categories

def topic_strategy(topic, topic_id, user_id):
    topic.load_by_id(topic_id, user_id)
    topic.entries = [entry.__dict__ for entry in topic.entries]
    topic = topic.__dict__
    return topic
    
def get_serializer(entry_type):
    entry_types = {
        "categories": categories_strategy,
        "category": category_strategy,
        "topic": topic_strategy,
        "journal": standard_strategy,
        "todo": standard_strategy,
        "habit": standard_strategy
    }
    if entry_type in entry_types:
        return entry_types[entry_type]

