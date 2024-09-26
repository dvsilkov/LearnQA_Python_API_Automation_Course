"""
The command to run the tests via command line: pytest -s tests/test_user_auth.py
"""
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    # Параметры для негативного теста
    exclude_params = [
        "no_cookies",
        "no_token"
    ]

    @pytest.fixture
    def setup(self):
        """
        Метод выполняется при запуске каждого теста.
        Делает запрос по первой ссылке, для авторизации пользователя по логину и паролю.
        Проверяет, что cookie корректный, в header есть токен, а в ответе есть user id
        """
        url_1 = "https://playground.learnqa.ru/api/user/login"  # POST Logs user into the system

        # данные для авторизации
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        res_1 = requests.post(url_1, data=data)
        # получаем cookie, token и user_id из ответа с помощью методов из класса BaseCase
        self.auth_sid = self.get_cookie(res_1, "auth_sid")  # значение cookie
        self.token = self.get_header(res_1, "x-csrf-token")  # сам токен
        self.user_id_from_auth_method = self.get_json_value(res_1, "user_id")  # значение id пользователя

    def test_auth_user(self, setup):
        """
        Успешный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup
        """
        url_2 = "https://playground.learnqa.ru/api/user/auth"  # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        res_2 = requests.get(url_2, cookies={"auth_sid": self.auth_sid}, headers={"x-csrf-token": self.token})

        # проверка, что в ответе есть id пользователя и что user id совпадают в обоих запросах
        Assertions.assert_json_value_by_key(
            res_2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_user(self, setup, condition):
        """
        Успешный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup.
        Сделано два параметра, для запроса без cookies и без headers. В обоих случаях в ответе user_id должен быть равен 0
        """
        url_2 = "https://playground.learnqa.ru/api/user/auth"  # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        if condition == "no_cookies":
            res_2 = requests.get(url_2, headers={"x-csrf-token": self.token})
        else:
            res_2 = requests.get(url_2, cookies={"auth_sid": self.auth_sid})

        # проверка, что в ответе есть id пользователя и что user id равен 0 во втором запросе
        Assertions.assert_json_value_by_key(
            res_2,
            "user_id",
            0,
            f"User has been authorized with condition {condition}"
        )
