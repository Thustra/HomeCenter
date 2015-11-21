__author__ = 'Peter'

from app import db
from models import User

#insert data

db.session.add(User("admin","admin"))
db.session.add(User("super","super"))

#commit changes

db.session.commit()