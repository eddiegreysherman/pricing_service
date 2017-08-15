from functools import wraps
from src.app import app
from flask import session, redirect, url_for, request, flash


def requires_login(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash("You need to be logged in to access this section.")
            return redirect(url_for('users.login_user', next=request.path)) #sends back to alerts after login

        return func(*args, **kwargs)

    return decorated_func

def is_admin(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash("You need to be logged in to access this section.")
            return redirect(url_for('users.login_user', next=request.path)) #sends back to alerts after login
        if session['email'] not in app.config['ADMINS']:
            flash("You need to be an admin to access this section.")
            return redirect(url_for('users.login_user'))

        return func(*args, **kwargs)

    return decorated_func
