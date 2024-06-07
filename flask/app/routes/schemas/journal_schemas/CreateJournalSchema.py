from app.constants.ValidationConstants import ValidationConstants
from app.routes.schemas.EntrySchema import EntrySchema
from app.validators.id import validate_id
from app.validators.string import validate_string


class CreateJournalSchema(EntrySchema):
    def __init__(self, content: str, title: str, topic_id: str):
        self.content = validate_string(content, ValidationConstants.MIN_JOURNAL_LENGTH, ValidationConstants.MAX_JOURNAL_LENGTH)
        self.title = validate_string(title, ValidationConstants.MIN_TITLE_LENGTH, ValidationConstants.MAX_TITLE_LENGTH)
        self.topic_id = validate_id(topic_id)
