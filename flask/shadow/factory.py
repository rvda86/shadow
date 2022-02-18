from shadow.entries import Category, Topic, Journal, ToDo, Habit

def get_entry(entry_type):
    entry_types = {
        "category": Category,
        "topic": Topic,
        "journal": Journal,
        "todo": ToDo,
        "habit": Habit
    }
    if entry_type in entry_types:
        return entry_types[entry_type]()