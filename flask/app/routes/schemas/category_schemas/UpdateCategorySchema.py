from app.constants.ValidationConstants import ValidationConstants
from app.validators.id import validate_id
from app.validators.string import validate_string


class UpdateCategorySchema:

    def __init__(self, id: str, name: str):
        self.id = validate_id(id)
        self.name = validate_string(name, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
