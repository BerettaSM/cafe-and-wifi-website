from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash

from .models import User

from .custom_decorators import anonymous_only


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('POST',))
@anonymous_only
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember-me')
    user = User.query.filter_by(email=email).first()
    current_view = request.environ['HTTP_REFERER']
    if not (user and check_password_hash(user.password, password)):
        flash('Incorrect email/password.', category='error')
        return redirect(current_view)
    flash(f'Welcome {user.username}.', category='success')
    login_user(user, remember=remember == 'on')
    return redirect(current_view)


@auth.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
