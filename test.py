# -*- coding: utf-8 -*-
from app import app
import unittest


class FlaskTestCass(unittest.TestCase):

    #Login that returns a response
    def login_with_response(self, user, psw, tester):
        return tester.post(
            '/login',
            data=dict(username=user, password=psw),
            follow_redirects=True
        )

    #Login without returning a response
    def login_no_response(self, user, psw, tester):
        tester.post('/login',
            data=dict(username=user, password=psw),
            follow_redirects=True
        )

    #Log user out
    def logout(self, tester):
        return tester.get('/logout', follow_redirects=True)

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login', response.data)

    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = self.login_with_response("admin", "admin", tester)
        self.assertIn(b'You were just logged in!', response.data)

    # Ensure login behaves correctly given incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = self.login_with_response("kyle", "pass", tester)
        self.assertIn(b'Invalid credentials.  Please try again.',
            response.data
        )

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        self.login_no_response("admin", "admin", tester)
        response = self.logout(tester)
        self.assertIn(b'You were just logged out!', response.data)

    # Ensure that the main page requires login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    # Ensure that logout requires user to be logged in
    def test_logout_requires_login(self):
        tester = app.test_client(self)
        response = self.logout(tester)
        self.assertIn(b'You need to login first.', response.data)

    # Ensure that posts show up on the main page
    def test_posts_on_main_page(self):
        tester = app.test_client()
        response = self.login_with_response("admin", "admin", tester)
        self.assertIn(b'well.', response.data)
        self.assertIn(b'good.', response.data)

if __name__ == '__main__':
    unittest.main()