from datetime import datetime
from time import strftime

import pytest
import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserRegister(BaseCase):

    @pytest.fixture
    def setup(self):
        """ Метод генерирует случайный email, используя текущие дату и время"""
        self.email = f"learnqa{datetime.now().strftime("%d%m%Y%H%M%S")}@example.com"

    def test_create_user_successfully(self, setup):
        """
        Тест проверяет создания пользователя.
        Также проверяется значение status code и текст сообщения.
        """
        url = "https://playground.learnqa.ru/api/user/"  # POST Create user
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email
        }
        response = requests.post(url=url, data=data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_mail(self):
        """
        Тест проверяет невозможность создания пользователя с существующим email.
        Также проверяется значение status code и текст сообщения.
        """
        url = "https://playground.learnqa.ru/api/user/"  # POST Create user
        email = "vinkotov@example.com"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }
        response = requests.post(url=url, data=data)
        Assertions.assert_status_code(response, 400)
        # response.content возвращает байтовую строку, поэтому преобразуем ее с помощью decode("utf-8")
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}'"
