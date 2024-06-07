from app.constants.ExceptionMessages import ExceptionMessages
from app.constants.ValidationConstants import ValidationConstants
from app.routes.schemas.EntrySchema import EntrySchema
from app.validators.id import validate_id
from app.validators.string import validate_string


class UpdateToDoSchema(EntrySchema):
    def __init__(self, completed: str, id: str, task: str):
        if completed not in ["0", "1"]:
            raise ValueError(ExceptionMessages.COMPLETED_NOT_VALID)
        self.completed = completed
        self.id = validate_id(id)
        self.task = validate_string(task, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
