from datetime import datetime
from time import strftime

import pytest
import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    """ Класс с тестами по созданию нового пользователя"""

    def test_create_user_successfully(self):
        """
        Тест проверяет создания нового пользователя.
        Также проверяется значение status code и наличие ключа "id".
        """
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data) # POST: Create user
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_try_create_user_with_existing_mail(self):
        """
        Тест проверяет невозможность создания пользователя с существующим email.
        Также проверяется значение status code и текст сообщения.
        """
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data) # POST: Create user
        Assertions.assert_status_code(response, 400)
        # проверка текста сообщения
        # response.content возвращает байтовую строку, поэтому преобразуем ее с помощью decode("utf-8")
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}'"
