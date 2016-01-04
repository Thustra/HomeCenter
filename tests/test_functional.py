__author__ = 'Peter'

# tests/test_functional.py

import unittest

from flask.ext.login import current_user

from tests.base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    # Ensure that welcome page loads
    def test_welcome_route_works_as_expected(self):
        response = self.client.get('/welcome', follow_redirects=True)
        self.assertIn(b'Welcome to Flask!', response.data)

    # Ensure main page requires a login
    def test_main_route_requires_login(self):

        response =  self.client.get('/', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    # Ensure series show up on the main page
    def test_posts_show_up(self):

        response =  self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Firefly', response.data)


class UserViewsTests(BaseTestCase):

 # Ensure the login page loads
    def test_login_page_loads(self):

        response =  self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure the login works correctly with the right credentials
    def test_correct_login(self):

        response =  self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'You were just logged in.', response.data)

    # Ensure the login works with incorrect credentials
    def test_incorrect_login(self):
        response =  self.client.post(
            '/login',
            data=dict(username="admin", password="wrongpassword"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    def test_incorrect_login_shows_error(self):
        response =  self.client.post(
            '/login',
            data=dict(username="", password=""),
            follow_redirects=True
        )
        self.assertIn(b'This field is required', response.data)

    def test_incorrect_register_shows_error(self):
        response =  self.client.post(
            '/register',
            data=dict(username="", email="", password="", confirm=""),
            follow_redirects=True
        )
        self.assertIn(b'This field is required', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True)
            response =  self.client.get(
                '/logout',
                follow_redirects=True
            )
            self.assertIn(b'You were just logged out.', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure logout page requires a login
    def test_logout_route_requires_login(self):

        response =  self.client.get('/logout', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    # Ensure logged in user is the user that logged in

    def test_correct_login_user(self):
        with self.client:
            response =  self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            self.assertTrue(current_user.name == "admin")

    def test_correct_login_user_isactive(self):
        with self.client:
            response =  self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            self.assertTrue(current_user.is_active)

class HomeViewsTests(BaseTestCase):

    def test_add_requires_login(self):
        response =  self.client.get('/add', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    def test_add(self):
        with self.client:
            response =  self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
        response = self.client.post(
                '/add',
                data=dict(title="Friends", watching=True, finished=False,tvmaze_id=100),
                follow_redirects=True
            )
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Successfully added!',response.data)

if __name__ == '__main__':
    unittest.main()