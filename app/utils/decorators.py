from functools import wraps

from flask import flash, redirect, session, url_for


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_user_id"):
            flash("Please log in to access the admin panel.", "warning")
            return redirect(url_for("admin.login"))
        return view_func(*args, **kwargs)

    return wrapped_view
