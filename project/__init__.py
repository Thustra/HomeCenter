###########
# Imports #
###########

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView,expose
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
# Login #
#########

from project.models import *

login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

#########
# Admin #
#########

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        arg1 = 'Hello'
        return self.render('admin/myhome.html', arg1=arg1)

admin = Admin(app,name='HomeCenter',index_view=MyHomeView())

class CustomModelView(ModelView):

    def is_accessible(self):
        print(current_user)
        return current_user.is_authenticated

admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(Show, db.session))
admin.add_view(CustomModelView(Expense_category, db.session))
admin.add_view(CustomModelView(Expense, db.session))