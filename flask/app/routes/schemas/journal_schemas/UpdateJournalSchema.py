from app.constants.ValidationConstants import ValidationConstants
from app.validators.id import validate_id
from app.validators.string import validate_string


class UpdateJournalSchema:
    def __init__(self, content: str, id: str, title: str):
        self.content = validate_string(content, ValidationConstants.MIN_JOURNAL_LENGTH, ValidationConstants.MAX_JOURNAL_LENGTH)
        self.id = validate_id(id)
        self.title = validate_string(title, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
