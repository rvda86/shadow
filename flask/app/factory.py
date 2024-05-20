from app.models.entry.Category import Category
from app.models.entry.Habit import Habit
from app.models.entry.Journal import Journal
from app.models.entry.Tag import Tag
from app.models.entry.ToDo import ToDo
from app.models.entry.Topic import Topic


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
