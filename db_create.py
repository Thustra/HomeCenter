__author__ = 'Peter'


from app import db
from models import Show

# create database and db tables

db.create_all()

# insert

db.session.add(Show("Firefly", True))
db.session.add(Show("Gotham", False))


# commit changes

db.session.commit()