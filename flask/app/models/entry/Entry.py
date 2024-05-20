from abc import ABC, abstractmethod


class Entry(ABC):

    @abstractmethod
    def create(self, user_id: str, data: dict):
        pass

    @abstractmethod
    def delete(self, user_id: str):
        pass

    @abstractmethod
    def load_by_id(self, entry_id: str, user_id: str):
        pass

    @abstractmethod
    def update(self, user_id: str, data: dict):
        pass


def to_dict(obj):
    dictionary = obj.__dict__
    for k, v in dictionary.items():
        if isinstance(v, list):
            dictionary[k] = [to_dict(item) if isinstance(item, Entry) else item for item in v]
    return dictionary
