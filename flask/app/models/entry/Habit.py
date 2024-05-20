from datetime import datetime, timedelta

from app.db_mysql import db_pool
from app.error_handling import NotFoundException
from app.models.entry.Entry import Entry
from app.validation import validate_date, validate_id, validate_name
from app.utils.utils import uuid_generator

db = db_pool.acquire()


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
            raise NotFoundException
        self.id, self.topic_id, self.date_posted, self.date_edited, self.name = result
        self.entry_type = "habit"
        self.days = self.load_days(user_id)

    def create(self, user_id: str, data: dict):
        self.id = uuid_generator()
        self.date_posted = datetime.utcnow()
        self.set_topic(data["topic_id"])
        self.set_name(data["name"])
        db.create_update_delete(db.create_habit_entry_sql,
                                (self.id, user_id, self.topic_id, self.date_posted, self.name))
        self.load_by_id(self.id, user_id)
        return self, "habit tracker created"

    def update(self, user_id: str, data: dict):
        self.date_edited = datetime.utcnow()
        self.set_name(data["name"])
        db.create_update_delete(db.update_habit_entry_sql, (self.date_edited, self.name, self.id, user_id))

        days_completed = self.load_days_completed(user_id)

        for day in data["days"]:
            validate_date(day["date"])
            if day["completed"] == 1:
                if day["date"] not in days_completed:
                    db.create_update_delete(db.create_habit_days_completed_sql, (user_id, self.id, day["date"]))

        for d in days_completed:
            for day in data["days"]:
                if day["date"] == d:
                    if day["completed"] == 0:
                        db.create_update_delete(db.delete_habit_days_completed_sql, (self.id, user_id, day["date"]))

        self.load_by_id(self.id, user_id)
        return self, "habit tracker updated"

    def delete(self, user_id: str):
        db.create_update_delete(db.delete_habit_entry_sql, (self.id, user_id))
        return "habit tracker deleted"

    def load_days_completed(self, user_id: str):
        days_completed = db.retrieve_all_by_id(db.retrieve_habit_days_completed_sql, (self.id, user_id))
        if days_completed is None:
            return []
        days_completed = [day[0] for day in list(days_completed)]
        return days_completed

    def load_days(self, user_id: str):
        days_completed = self.load_days_completed(user_id)

        first_monday = (self.date_posted + timedelta(days=-self.date_posted.weekday())).date()
        next_sunday = (datetime.utcnow() + timedelta(days=6 - datetime.utcnow().weekday())).date()

        days = []
        date = next_sunday
        format = "%a-%d/%m/%Y"
        while (date >= first_monday):
            date_formatted = date.strftime(format)
            if date_formatted in days_completed:
                days.insert(0, {"date": date_formatted, "completed": 1})
            else:
                days.insert(0, {"date": date_formatted, "completed": 0})
            date = date + timedelta(days=-1)

        return days

    def set_topic(self, id: str):
        validate_id(id)
        self.topic_id = id

    def set_name(self, name: str):
        validate_name(name)
        self.name = name
