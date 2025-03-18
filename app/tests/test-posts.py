import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from flask import url_for
from app.app import app, posts_list


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_index_page(client):
    response = client.get(url_for('index'))
    assert response.status_code == 200
    assert b'<!doctype html>' in response.data
    response_text = response.data.decode('utf-8').strip()
    assert 'Задание к лабораторной работе' in response_text


def test_about_page(client):
    response = client.get(url_for('about'))
    assert response.status_code == 200
    assert b'<!doctype html>' in response.data
    response_text = response.data.decode('utf-8').strip()
    assert '<h1 class="mt-5 text-center">Об авторе</h1>' in response_text


def test_posts_page(client):
    response = client.get(url_for('posts'))
    assert response.status_code == 200
    assert b'<!doctype html>' in response.data
    response_text = response.data.decode('utf-8').strip()
    assert '<h1 class="my-5">Последние посты</h1>' in response_text


def test_post_page(client):
    response = client.get(url_for('post', index=0))
    assert response.status_code == 200
    assert b'<!doctype html>' in response.data
    response_text = response.data.decode('utf-8').strip()
    assert '<h3>Комментарии</h3>' in response_text


def test_posts_page_title(client):
    response = client.get(url_for('posts'))
    for post in posts_list:
        assert post['title'].encode() in response.data


def test_post_page_data(client):
    post = posts_list[0]
    response = client.get(url_for('post', index=0))
    assert response.status_code == 200
    assert post['title'].encode() in response.data
    assert post['text'][:50].encode() in response.data
    assert post['author'].encode() in response.data
    assert post['date'].strftime('%d.%m.%Y').encode() in response.data


def test_non_existent_post(client):
    response = client.get(url_for('post', index=999))
    assert response.status_code == 302