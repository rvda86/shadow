from functools import wraps

from app.constants.ExceptionMessages import ExceptionMessages

class InvalidDataError(Exception):
    pass


class UsernameTakenError(Exception):
    pass


class EmailTakenError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class NotFoundError(Exception):
    pass


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
        except InvalidDataError as e:
            return {"msg": str(e)}, 422
        except UsernameTakenError:
            return {"msg": ExceptionMessages.USERNAME_NOT_AVAILABLE}, 409
        except EmailTakenError:
            return {"msg": ExceptionMessages.EMAIL_NOT_AVAILABLE}, 409
        except InvalidPasswordError:
            return {"msg": "wrong password provided"}, 401
        except NotFoundError:
            return {"msg": "resource not found"}, 404
        except DatabaseError:
            return {"msg": "something went wrong"}, 500
        except NotEmptyError as e:
            return {"msg": str(e)}, 409
        except ValueError as e:
            return {"msg": str(e)}, 422
    return inner
