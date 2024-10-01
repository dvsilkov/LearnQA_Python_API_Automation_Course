import pytest
import requests
from lib.base_case import BaseCase


@pytest.fixture(scope="function")
def user_logs_into_the_system(email="vinkotov@example.com", password="1234"):
    """
    Метод делает запрос по ссылке для авторизации пользователя по логину и паролю.
    Получает cookie, token и user id из ответа и возвращает их значения в виде словаря.
    """
    url = "https://playground.learnqa.ru/api/user/login"  # POST: Logs user into the system

    # данные для авторизации
    data = {
        "email": email,
        "password": password
    }
    res_1 = requests.post(url, data=data)
    # получаем cookie, token и user_id из ответа с помощью методов из класса BaseCase
    auth_sid = BaseCase().get_cookie(res_1, "auth_sid")  # значение cookie
    token = BaseCase().get_header(res_1, "x-csrf-token")  # сам токен
    user_id_from_auth_method = BaseCase().get_json_value(res_1, "user_id")  # значение id пользователя
    return {"auth_sid": auth_sid, "token": token, "user_id_from_auth_method": user_id_from_auth_method}
