__author__ = 'Peter'

from flask import Flask,render_template, redirect, url_for,session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
#import sqlite3

# Configuration variables

app = Flask(__name__)

##########
# Config #
##########

import os
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *
from project.users.views import users_blueprint

# Register the blueprints

app.register_blueprint(users_blueprint)

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

@app.route('/')
@login_required
def home():
    shows = db.session.query(Show).all()
    files = db.session.query(Download).all()
    return render_template('index.html', shows=shows, downloads=files)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

##############
# Run Server #
##############

if __name__ == '__main__':
    app.run()