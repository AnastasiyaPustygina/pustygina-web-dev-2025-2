import unittest
from app.lab_3 import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_valid(self):
        response = self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
        self.assertIn(b'Вы успешно вошли!', response.data)

    def test_login_invalid(self):
        response = self.app.post('/login', data={'username': 'user', 'password': 'wrong'}, follow_redirects=True)
        self.assertIn(b'Неверный логин или пароль', response.data)

    def test_secret_page_without_login(self):
        response = self.app.get('/secret', follow_redirects=True)
        self.assertIn(b'Войти', response.data)

    def test_secret_page_with_login(self):
        self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
        response = self.app.get('/secret')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
