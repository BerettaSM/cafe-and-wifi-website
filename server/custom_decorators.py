from functools import wraps
from http import HTTPStatus

from flask import abort
from flask_login import current_user


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.has_admin_privileges:
            return f(*args, **kwargs)
        return abort(HTTPStatus.FORBIDDEN, "You don't have permission to access this resource.")
    return decorated_function


def authenticated_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        return abort(HTTPStatus.FORBIDDEN, "You have to be logged in to access this resource.")
    return decorated_function


def anonymous_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous and not current_user.is_authenticated:
            return f(*args, **kwargs)
        return abort(HTTPStatus.FORBIDDEN, "You must be logged out to perform that action.")
    return decorated_function
