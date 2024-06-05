from app.constants.ValidationConstants import ValidationConstants
from app.validators.string import validate_string


class CreateCategorySchema:

    def __init__(self, name: str):
        self.name = validate_string(name, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
