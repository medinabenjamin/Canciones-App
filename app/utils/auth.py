from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.rol is None or current_user.rol.nombre not in roles:
                return abort(403)
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
