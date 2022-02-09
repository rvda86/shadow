from abc import ABC, abstractmethod
from shadow.entries import *

class EntryFactory(ABC):
    @abstractmethod
    def get_entry(self):
        pass

class CategoryFactory(EntryFactory):
    def get_entry(self):
        return EntryCategory()

class TopicFactory(EntryFactory):
    def get_entry(self):
        return EntryTopic()

class JournalFactory(EntryFactory):
    def get_entry(self):
        return EntryJournal()

class ToDoFactory(EntryFactory):
    def get_entry(self):
        return EntryToDo()

class HabitFactory(EntryFactory):
    def get_entry(self):
        return EntryHabit()

def get_entry_factory(entry_type):
    entry_types = {
        "category": CategoryFactory(),
        "topic": TopicFactory(),
        "journal": JournalFactory(),
        "todo": ToDoFactory(),
        "habit": HabitFactory()
    }
    if entry_type in entry_types:
        return entry_types[entry_type]
