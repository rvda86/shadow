from app.constants.ExceptionMessages import ExceptionMessages
from app.constants.ValidationConstants import ValidationConstants
from app.routes.schemas.EntrySchema import EntrySchema
from app.validators.date import validate_date
from app.validators.id import validate_id
from app.validators.string import validate_string


class UpdateHabitSchema(EntrySchema):

    def __init__(self, days, id: str, name: str):
        for day in days:
            validate_date(day["date"])
            if day["completed"] not in [0, 1]:
                raise ValueError(ExceptionMessages.COMPLETED_NOT_VALID)
        self.days = days
        self.id = validate_id(id)
        self.name = validate_string(name, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
