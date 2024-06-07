from app.constants.ValidationConstants import ValidationConstants
from app.routes.schemas.EntrySchema import EntrySchema
from app.validators.id import validate_id
from app.validators.string import validate_string


class CreateToDoSchema(EntrySchema):
    def __init__(self, task: str, topic_id: str):
        self.task = validate_string(task, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
        self.topic_id = validate_id(topic_id)
