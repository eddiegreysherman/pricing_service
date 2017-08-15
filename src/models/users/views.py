from flask import Blueprint, request, redirect, url_for, render_template, session

from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # Check login is valid
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e :
            return e.message

    return render_template('users/login.html') # Send an error if the login is invalid


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():

    if request.method == 'POST':
        # Check login is valid
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e :
            return e.message

    return render_template('users/register.html') # Send an error if the login is invalid

@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts)

@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass