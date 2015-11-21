__author__ = 'Peter'


from project import db
from project.models import Show

# create database and db tables

db.create_all()

# insert

db.session.add(Show("Firefly", True))
db.session.add(Show("Gotham", False))
db.session.add(Show("The Big Bang Theory", False))
db.session.add(Show("Glee", True))


# commit changes

db.session.commit()