from app.models.entry.entries import Category, Topic, Journal, ToDo, Habit, Tag

def get_entry(entry_type):
    entry_types = {
        "category": Category,
        "topic": Topic,
        "journal": Journal,
        "todo": ToDo,
        "habit": Habit,
        "tag": Tag
    }
    if entry_type in entry_types:
        return entry_types[entry_type]()