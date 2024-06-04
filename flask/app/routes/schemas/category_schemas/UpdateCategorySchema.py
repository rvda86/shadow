from app.validators.name import validate_name


class CreateCategorySchema:

    def __init__(self, name):
        self.name = validate_name(name, 1, 30)
