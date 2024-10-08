import json.decoder
from datetime import datetime

import allure
from requests import Response

from lib.my_requests import MyRequests


class BaseCase:
    """ Класс с основными методами """

    def get_cookie(self, response: Response, cookie_name):
        """
        Метод принимает ответ полученный после авторизации и ожидаемое название cookie;
        Проверяет корректность cookie;
        Возвращает значение cookie.
        """
        with allure.step(f"Get cookie value from response"):
            assert cookie_name in response.cookies, f"Can not find cookies with name {cookie_name} in the last response"
            return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        """
        Метод принимает ответ полученный после авторизации и ожидаемое название header;
        Проверяет корректность header;
        Возвращает значение header.
        """
        with allure.step(f"Get header value from response"):
            assert headers_name in response.headers, f"Can not find header with name {headers_name} in the last response"
            return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        """ Метод проверяет, что ответ в формате JSON, преобразовывает в словарь и возвращает значение по ключу name """
        with allure.step(f"Get json key value from response"):
            try:
                response_as_dict = response.json()
            except json.decoder.JSONDecodeError:
                assert False, f"Response is not JSON format. Response is '{response.text}'"

            assert name in response_as_dict, f"Response does not have key '{name}'"
            return response_as_dict.get(name)

    def prepare_registration_data(self, email=None):
        """
        Метод создает набор пользовательских данных в виде словаря.
        В качестве параметра указан email со значением по умолчанию None, в этом случае он будет случайный
        """
        with allure.step(f"Create registration data to login"):
            if email is None:
                # случайный email, используя текущие дату и время
                email = f"learnqa{datetime.now().strftime("%d%m%Y%H%M%S")}@example.com"

            return {
                "password": "123",
                "username": "learnqa",
                "firstName": "learnqa",
                "lastName": "learnqa",
                "email": email
            }

    def user_logs_into_the_system(self, email="vinkotov@example.com", password="1234"):
        """
        Метод делает запрос по ссылке для авторизации пользователя по логину и паролю (по умолчанию значения заданы).
        Получает cookie, token и user id из ответа и возвращает их значения в виде словаря.
        """
        with allure.step(f"Login into the system using email and password"):
            # данные для авторизации
            data = {
                "email": email,
                "password": password
            }
            response = MyRequests.post("/user/login", data=data)  # POST: Logs user into the system
            # получаем cookie, token и user_id из ответа с помощью методов из класса BaseCase
            auth_sid = self.get_cookie(response, "auth_sid")  # значение cookie
            token = self.get_header(response, "x-csrf-token")  # сам токен
            user_id_from_auth_method = self.get_json_value(response, "user_id")  # значение id пользователя
            # возвращаем значения в виде кортежа
            return auth_sid, token, user_id_from_auth_method
