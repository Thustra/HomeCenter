__author__ = 'Peter'

from project import app,db
from project.models import *
from flask import flash,redirect,session,url_for,render_template,Blueprint
from functools import wraps

##########
# Config #
##########

home_blueprint = Blueprint(
    'home', __name__,
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

@home_blueprint.route('/')
@login_required
def home():
    shows = db.session.query(Show).all()
    files = db.session.query(Download).all()
    return render_template('index.html', shows=shows, downloads=files)

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')