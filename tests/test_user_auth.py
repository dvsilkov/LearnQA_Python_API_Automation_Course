"""
The command to run the tests via command line: pytest -s tests/test_user_auth.py
"""
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    """ Класс с тестами по проверке авторизации пользователя"""
    # Параметры для негативного теста
    exclude_params = [
        "no_cookies",
        "no_token"
    ]

    def test_auth_user(self, user_logs_into_the_system):
        """
        Успешный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup
        """
        url_2 = "https://playground.learnqa.ru/api/user/auth"  # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        res_2 = requests.get(
            url_2,
            cookies={"auth_sid": user_logs_into_the_system["auth_sid"]},
            headers={"x-csrf-token": user_logs_into_the_system["token"]}
        )

        # проверка, что в ответе есть id пользователя и что user id совпадают в обоих запросах
        Assertions.assert_json_value_by_key(
            res_2,
            "user_id",
            user_logs_into_the_system["user_id_from_auth_method"],
            "User id from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_user(self, user_logs_into_the_system, condition):
        """
        Успешный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup.
        Сделано два параметра, для запроса без cookies и без headers. В обоих случаях в ответе user_id должен быть равен 0
        """
        url_2 = "https://playground.learnqa.ru/api/user/auth"  # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        if condition == "no_cookies":
            res_2 = requests.get(url_2, headers={"x-csrf-token": user_logs_into_the_system["token"]})
        else:
            res_2 = requests.get(url_2, cookies={"auth_sid": user_logs_into_the_system["auth_sid"]})

        # проверка, что в ответе есть id пользователя и что user id равен 0 во втором запросе
        Assertions.assert_json_value_by_key(
            res_2,
            "user_id",
            0,
            f"User has been authorized with condition {condition}"
        )
