import pytest
from app.lab_2.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Flask-приложение работает!".encode("utf-8") in response.data

def test_url_params(client):
    response = client.get("/url_params?name=Alice")
    assert response.status_code == 200
    assert b"Alice" in response.data

def test_headers(client):
    response = client.get("/headers")
    assert response.status_code == 200
    assert b"User-Agent" in response.data

def test_cookies(client):
    response = client.get("/cookies")
    assert response.status_code == 200
    assert b"Cookie" in response.data

def test_form_params(client):
    response = client.post("/form_params", data={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 200
    assert b'Form submitted successfully' in response.data


def test_phone_validation(client):
    response = client.post("/validate_phone", data={"phone": "+1234567890"})

    assert response.status_code == 200

    assert b"8-123-456-78-90" in response.data


def test_phone_validation_error(client):
    response = client.post("/validate_phone", data={"phone": "+12345"})

    assert response.status_code == 400

    assert "Недопустимый ввод. Неверное количество цифр.".encode("utf-8") in response.data


def test_not_found(client):
    response = client.get("/non_existing_page")
    assert response.status_code == 404

def test_redirect(client):
    response = client.get("/redirect_example", follow_redirects=True)
    assert response.status_code == 200
    assert "Flask-приложение работает!".encode("utf-8") in response.data

def test_json_api(client):
    response = client.get("/api/data")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "key" in json_data

def test_form_missing_params(client):
    response = client.post("/form_params", data={"name": "Alice"})
    assert response.status_code == 400

def test_wrong_method(client):
    response = client.get("/validate_phone")
    assert response.status_code == 405

def test_set_cookie(client):
    response = client.get("/set_cookie")
    assert response.status_code == 200
    assert "Set-Cookie" in response.headers

def test_delete_cookie(client):
    client.set_cookie("localhost", "test_cookie", "12345")
    response = client.get("/delete_cookie")
    assert response.status_code == 200
    assert "Set-Cookie" in response.headers  # Cookie должно быть очищено

def test_post_json(client):
    response = client.post("/json_post", json={"key": "value"})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["key"] == "value"