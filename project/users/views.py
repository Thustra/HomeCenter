###########
# Imports #
###########

from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from app import app
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from functools import wraps

##########
# Config #
##########

users_blueprint = Blueprint(
    'users',__name__,
    template_folder='templates'
)

####################
# helper functions #
####################

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

##########
# Routes #
##########

@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out.')
    return redirect(url_for('welcome'))