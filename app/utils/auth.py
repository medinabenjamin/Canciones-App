from functools import wraps

from flask import abort, redirect, request, url_for
from flask_login import current_user

from app.extensions import login_manager


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for(login_manager.login_view, next=request.url))
            if current_user.rol is None or current_user.rol.nombre not in roles:
                return abort(403)
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
