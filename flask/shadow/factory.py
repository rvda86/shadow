from shadow.entries import EntryCategory, EntryTopic, EntryJournal, EntryToDo

def get_entry(entry_type):
    entry_types = {
        "category": EntryCategory,
        "topic": EntryTopic,
        "journal": EntryJournal,
        "todo": EntryToDo,
    }
    if entry_type in entry_types:
        return entry_types[entry_type]()