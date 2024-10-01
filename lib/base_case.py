import json.decoder
from datetime import datetime

from requests import Response

class BaseCase:
    """ Класс с основными методами """

    def get_cookie(self, response: Response, cookie_name):
        """
        Метод принимает ответ полученный после авторизации и ожидаемое название cookie;
        Проверяет корректность cookie;
        Возвращает значение cookie.
        """
        assert cookie_name in response.cookies, f"Can not find cookies with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        """
        Метод принимает ответ полученный после авторизации и ожидаемое название header;
        Проверяет корректность header;
        Возвращает значение header.
        """
        assert headers_name in response.headers, f"Can not find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        """ Метод проверяет, что ответ в формате JSON, преобразовывает в словарь и возвращает значение по ключу name """
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format. Response is '{response.text}'"

        assert name in response_as_dict, f"Response does not have key '{name}'"
        return response_as_dict.get(name)

    def prepare_registration_data(self, email=None):
        """
        Метод создает набор пользовательских данных.
        В качестве параметра указан email со значением по умолчанию None, в этом случае он будет случайный
        """
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
