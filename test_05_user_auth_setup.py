"""
The command to run the tests via command line: pytest -s test_05_user_auth_setup.py
"""
import pytest
import requests

class TestUserAuth():

    # Параметры для негативного теста
    exclude_params = [
        ("no_cookies"),
        ("no_token")
    ]

    """
    Метод делает запрос по первой ссылке, для авторизации пользователя по логину и паролю.
    Проверяет, что cookie корректный, в header есть токен, а в ответе есть user id
    """
    def setup(self):
        url_1 = "https://playground.learnqa.ru/api/user/login"  # POST Logs user into the system

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

        self.auth_sid = res_1.cookies.get("auth_sid")  # значение cookie
        self.token = res_1.headers.get("x-csrf-token")  # сам токен
        self.user_id_from_auth_method = res_1.json().get("user_id")  # значение id пользователя

    """ 
    Успешный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup
    """
    def test_auth_user(self):
        url_2 = "https://playground.learnqa.ru/api/user/auth" # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        res_2 = requests.get(url_2, cookies={"auth_sid": self.auth_sid}, headers={"x-csrf-token": self.token})
        # проверка, что в ответе есть id пользователя
        assert "user_id" in res_2.json(), "There is no user id in the second response"
        user_id_from_check_method = res_2.json().get("user_id") # значение id пользователя из ответа во втором запросе

        # проверка, что user id совпадают в обоих запросах
        assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

    """
    Успешный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup.
    Сделано два параметра, для запроса без cookies и без headers. В обоих случаях в ответе user_id должен быть равен 0
    """
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_user(self, condition):
        url_2 = "https://playground.learnqa.ru/api/user/auth" # GET Get user id you are authorizes as OR get 0 if not authorized

        # второй запрос с использованием данных, полученных из первого
        if condition == "no_cookies":
            res_2 = requests.get(url_2, headers={"x-csrf-token": self.token})
        else:
            res_2 = requests.get(url_2, cookies={"auth_sid": self.auth_sid})
        # проверка, что в ответе из второго запроса есть id пользователя
        assert "user_id" in res_2.json(), "There is no user id in the second response"
        user_id_from_check_method = res_2.json().get("user_id") # значение id пользователя из ответа во втором запросе

        # проверка, что user id равен 0
        assert user_id_from_check_method == 0, f"User has been authorized with condition {condition}"
