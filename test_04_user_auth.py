"""
The command to run the tests via command line: pytest -s test_04_user_auth.py
"""
import pytest
import requests

class TestUserAuth:

    """ Успешный сценарий аутентификации"""
    def test_auth_user(self):
        url_1 = "https://playground.learnqa.ru/api/user/login" # POST Logs user into the system

        # данные для авторизации
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        res_1 = requests.post(url_1, data=data)
        # проверки, что в ответе есть нужный cookie, нужный header и нужный id пользователя
        assert "auth_sid" in res_1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in res_1.headers, "There is no CSRF token in the response"
        assert "user_id" in res_1.json(), "There is no user id in the response"

        auth_sid = res_1.cookies.get("auth_sid") # значение cookie
        token = res_1.headers.get("x-csrf-token") # сам токен
        user_id_from_auth_method = res_1.json().get("user_id") # значение id пользователя

        url_2 = "https://playground.learnqa.ru/api/user/auth" # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        res_2 = requests.get(url_2, cookies={"auth_sid": auth_sid}, headers={"x-csrf-token": token})
        # проверка, что в ответе есть id пользователя
        assert "user_id" in res_2.json(), "There is no user id in the second response"
        user_id_from_check_method = res_2.json().get("user_id") # значение id пользователя из ответа во втором запросе

        # проверка, что user id совпадают в обоих запросах
        assert user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"


    exclude_params = [
        ("no_cookies"),
        ("no_token")
    ]

    """
    Неуспешный сценарий аутентификации. Сделано два параметра, для запроса без cookies и без headers. В обоих случаях
    в ответе user_id должен быть равен 0
    """
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_user(self, condition):
        url_1 = "https://playground.learnqa.ru/api/user/login" # POST Logs user into the system

        # данные для авторизации
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        res_1 = requests.post(url_1, data=data)
        # проверки, что в ответе есть нужный cookie, нужный header и нужный id пользователя
        assert "auth_sid" in res_1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in res_1.headers, "There is no CSRF token in the response"
        assert "user_id" in res_1.json(), "There is no user id in the response"

        auth_sid = res_1.cookies.get("auth_sid") # значение cookie
        token = res_1.headers.get("x-csrf-token") # сам токен

        url_2 = "https://playground.learnqa.ru/api/user/auth" # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        if condition == "no_cookies":
            res_2 = requests.get(url_2, headers={"x-csrf-token": token})
        else:
            res_2 = requests.get(url_2, cookies={"auth_sid": auth_sid})
        # проверка, что в ответе из второго запроса есть id пользователя
        assert "user_id" in res_2.json(), "There is no user id in the second response"
        user_id_from_check_method = res_2.json().get("user_id") # значение id пользователя из ответа во втором запросе

        # проверка, что user id равен 0
        assert user_id_from_check_method == 0, f"User has been authorized with condition {condition}"
