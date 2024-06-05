from app.constants.ValidationConstants import ValidationConstants
from app.validators.id import validate_id
from app.validators.string import validate_string


class CreateHabitSchema:

    def __init__(self, name: str, topic_id: str):
        self.name = validate_string(name, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
        self.topic_id = validate_id(topic_id)
