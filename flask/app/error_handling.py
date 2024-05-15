from functools import wraps

from app.constants.ExceptionMessages import ExceptionMessages


class CustomException(Exception):
    def __init__(self, status_code: int, message: str, headers=None):
        self.status_code = status_code
        self.message = message
        self.headers = headers


class InvalidDataError(Exception):
    pass


class UsernameTakenError(Exception):
    pass


class EmailTakenError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class NotFoundException(CustomException):
    def __init__(self, message=None):
        if not message:
            message = ExceptionMessages.ITEM_NOT_FOUND
        super().__init__(404, message)


class DatabaseError(Exception):
    pass


class VerificationMailError(Exception):
    pass


class NotEmptyError(Exception):
    pass


def error_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            return {"msg": e.message}, e.status_code
        except InvalidDataError as e:
            return {"msg": str(e)}, 422
        except UsernameTakenError:
            return {"msg": ExceptionMessages.USERNAME_NOT_AVAILABLE}, 409
        except EmailTakenError:
            return {"msg": ExceptionMessages.EMAIL_NOT_AVAILABLE}, 409
        except InvalidPasswordError:
            return {"msg": ExceptionMessages.PASSWORD_WRONG}, 401
        except DatabaseError:
            return {"msg": "something went wrong"}, 500
        except NotEmptyError as e:
            return {"msg": str(e)}, 409
        except ValueError as e:
            return {"msg": str(e)}, 422
    return inner
