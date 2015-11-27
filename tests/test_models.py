__author__ = 'Peter'

# tests/test_models.py


import unittest

from flask.ext.login import current_user

from tests.base import BaseTestCase
from project import bcrypt
from project.models import User,Show,Download


class TestUser(BaseTestCase):

    def test_correct_register_user(self):
        with self.client:
            response =  self.client.post(
                '/register',
                data=dict(username="test", email="test@test.com", password="test", confirm="test"),
                follow_redirects=True
            )
            self.assertTrue(current_user.name == "test")
            self.assertIn(b'Welcome to Flask!', response.data)
            self.assertTrue(current_user.is_active)
            user = User.query.filter_by(name="test").first()
            self.assertTrue(str(user)== "User test")

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in user
        with self.client:
            self.client.post('/login', data=dict(
                username="admin", password='admin'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 10)

    def test_check_password(self):
        # Ensure given password is correct after unhashing
        user = User.query.filter_by(id=1).first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

class TestShow(BaseTestCase):

    def test_check_title(self):
        show = Show.query.filter_by(id=1).first()
        self.assertTrue(show.title == "Firefly")

    def test_check_watching(self):
        show = Show.query.filter_by(id=1).first()
        self.assertTrue(show.watching)

    def test_check_finished(self):
        show = Show.query.filter_by(id=1).first()
        self.assertFalse(show.finished)

    def test_representation(self):
        show = Show.query.filter_by(id=1).first()
        self.assertTrue(str(show) == "<title Firefly")

class TestDownload(BaseTestCase):

    def test_check_filename(self):
        download = Download.query.filter_by(id=1).first()
        self.assertTrue(download.filename == "test.avi")

    def test_check_location(self):
        download = Download.query.filter_by(id=1).first()
        self.assertTrue(download.location == "C:\\test.avi")

    def test_check_size(self):
        download = Download.query.filter_by(id=1).first()
        self.assertTrue(download.size == 123456)

    def test_representation(self):
        download = Download.query.filter_by(id=1).first()
        self.assertTrue(str(download) == "<File test.avi")


if __name__ == '__main__':
    unittest.main()