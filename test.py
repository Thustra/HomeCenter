__author__ = 'Peter'

from project import app
import unittest

class FlaskTestCase(unittest.TestCase):

    #ensure flask is setup correctly

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure the login page loads
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure the login works correctly with the right credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'You were just logged in.', response.data)

    # Ensure the login works with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="wrongpassword"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)


    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get(
            '/logout',
            follow_redirects=True
        )
        self.assertIn(b'You were just logged out.', response.data)

    # Ensure main page requires a login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)

    # Ensure logout page requires a login
    def test_logout_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)

    # Ensure posts show up on the mainpage
    def test_posts_show_up(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Firefly', response.data)


if __name__ == '__main__':
    unittest.main()
