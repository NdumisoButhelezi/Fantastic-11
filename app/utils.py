from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                flash("Unauthorized access!", "danger")
                return redirect(url_for('role_selection'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
