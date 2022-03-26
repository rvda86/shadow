from functools import wraps

class InvalidDataError(Exception):
    pass

class UsernameOrEmailTakenError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class NotFoundError(Exception):
    pass

class DatabaseError(Exception):
    pass

class VerificationMailError(Exception):
    pass

def error_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidDataError as e:
            print(e) 
            return {"msg": "Invalid data"}, 422
        except UsernameOrEmailTakenError as e:
            print(e)
            return {"msg": "Username or email already taken"}, 409
        except InvalidPasswordError:
            return {"msg": "Wrong password provided"}, 401
        except NotFoundError:
            return {"msg": "Resource not found"}, 404
        except DatabaseError:
            return {"msg": "Something went wrong"}, 500
    return inner
