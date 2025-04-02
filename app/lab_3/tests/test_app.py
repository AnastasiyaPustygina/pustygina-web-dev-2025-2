import unittest
from flask import session
from app.lab_3.app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'supersecretkey'
        self.app = app.test_client()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_counter(self):
        with self.app as client:
            response = self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
            response_text = response.data.decode('utf-8')
            self.assertIn('Вы посетили эту страницу 1', response_text)
            response = self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
            response_text = response.data.decode('utf-8')
            self.assertIn('Вы посетили эту страницу 2', response_text)

    def test_login_valid(self):
        response = self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
        response_text = response.data.decode('utf-8').strip()
        self.assertIn('Вы посетили эту страницу', response_text)

    # 4️⃣ Тест неудачной аутентификации (остаемся на той же странице)
    def test_login_invalid(self):
        response = self.app.post('/login', data={'username': 'user', 'password': 'wrong'}, follow_redirects=True)
        response_text = response.data.decode('utf-8').strip()
        self.assertIn('Неверный логин или пароль', response_text)

    # 5️⃣ Тест доступа к секретной странице без логина (редирект на логин)
    def test_secret_page_without_login(self):
        response = self.app.get('/secret', follow_redirects=True)
        response_text = response.data.decode('utf-8').strip()
        self.assertIn('Войти', response_text)

    # 6️⃣ Тест доступа к секретной странице с логином
    def test_secret_page_with_login(self):
        self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
        response = self.app.get('/secret')
        self.assertEqual(response.status_code, 200)


    def test_redirect_after_login(self):
        response = self.app.get('/secret', follow_redirects=True)
        response_text = response.data.decode('utf-8').strip()
        self.assertIn('Войти', response_text)  # Ожидаем страницу логина
        response = self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
        self.assertEqual(response.request.path, '/')

    def test_remember_me(self):
        with self.app as client:
            client.post('/login', data={'username': 'user', 'password': 'qwerty', 'remember': 'y'},
                        follow_redirects=True)
            with client.session_transaction() as sess:
                remember = sess.get('_user_id')
            self.assertIsNotNone(remember)

    def test_logout(self):
        self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        response_text = response.data.decode('utf-8').strip()
        self.assertIn('Вы не вошли в систему.', response_text)

    def test_navbar_links(self):
        response = self.app.get('/')
        response_text = response.data.decode('utf-8').strip()
        self.assertIn('Войти', response_text)
        self.app.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
        response = self.app.get('/')
        response_text = response.data.decode('utf-8').strip()
        self.assertIn('Секретная страница', response_text)  # Проверяем, что ссылка появилась

if __name__ == '__main__':
    unittest.main()
