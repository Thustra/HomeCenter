__author__ = 'Peter'

from flask import Flask,render_template, redirect, request, url_for,session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
#import sqlite3

# Configuration variables

app = Flask(__name__)

# Config
import os
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])


# create the sqlalchemy object

db = SQLAlchemy(app)

from models import *

# routes

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    #shows = []
    #try:
        # g is temporary object
    #    g.db = connect_db()
    #    cur = g.db.execute('select * from shows')
        # cur.fetchall() --> list of tuples which we then cast to a list of dicts
    #    shows = [dict(title=row[1], finished=row[2]) for row in cur.fetchall()]
    #    g.db.close()
    #except sqlite3.OperationalError:
    #    flash("You have no database")

    shows = db.session.query(Show).all()
    return render_template('index.html', shows=shows)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET','POST'])
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

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out.')
    return redirect(url_for('welcome'))

#def connect_db():
#    return sqlite3.connect('shows.db')


if __name__ == '__main__':
    app.run()