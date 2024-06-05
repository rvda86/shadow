from app.constants.ExceptionMessages import ExceptionMessages
from app.constants.ValidationConstants import ValidationConstants
from app.validators.id import validate_id
from app.validators.string import validate_string


class CreateTopicSchema:

    def __init__(self, category_id: str, name: str, topic_type: str):
        self.category_id = validate_id(category_id)
        self.name = validate_string(name, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
        if topic_type not in ["journal", "todo", "habit"]:
            raise ValueError(ExceptionMessages.TOPIC_TYPE_NOT_VALID)
        self.topic_type = topic_type
