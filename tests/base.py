__author__ = 'Peter'

from project import app,db
from flask.ext.testing import TestCase
from project.models import User,Download,Show
import datetime


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin","admin"))
        db.session.add(Show("Firefly",True,False,180))
        db.session.add(Download("test.avi",123456,"C:\\test.avi",datetime.datetime.now(),1))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()