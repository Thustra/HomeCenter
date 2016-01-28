###########
# Imports #
###########

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

##########
# Config #
##########

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
admin = Admin(app,name='HomeCenter')

##############
# Blueprints #
##############

from project.users.views import users_blueprint
from project.home.views import home_blueprint
from project.budget.views import budget_blueprint

# Register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(budget_blueprint)

#########
# Admin #
#########



#########
# Login #
#########

from project.models import User

login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()