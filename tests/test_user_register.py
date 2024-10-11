"""
The command to run the tests via command line: pytest -s tests/test_user_register.py
with allure: pytest -s --alluredir=allure_results/ tests/test_user_register.py
run allure report: allure serve allure_results/
"""

import allure
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    """ Класс с тестами по созданию нового пользователя"""

    @allure.title("This test successfully create new user")
    def test_create_user_successfully(self):
        """
        Тест проверяет создания нового пользователя.
        Также проверяется значение status code и наличие ключа "id".
        """
        data = self.prepare_registration_data()  # словарь с полными данными для создания пользователя
        response = MyRequests.post("/user/", data=data)  # POST: Create user
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("This test try to create user if use existing email")
    def test_try_create_user_with_existing_mail(self):
        """
        Тест проверяет невозможность создания пользователя с существующим email.
        Также проверяется значение status code и текст сообщения.
        """
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)  # словарь с полными данными для создания пользователя
        response = MyRequests.post("/user/", data=data)  # POST: Create user
        Assertions.assert_status_code(response, 400)
        # проверка текста сообщения
        # response.content возвращает байтовую строку, поэтому преобразуем ее с помощью decode("utf-8")
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content '{response.content}'"

    @allure.title("This test try to create user if use incorrect email address without '@'")
    def test_try_create_user_with_incorrect_mail(self):
        """
        Тест проверяет невозможность создания пользователя, если нет символа '@'
        Также проверяется значение status code и текст сообщения.
        """
        email = "vinkotov-wrongexample.com"
        data = self.prepare_registration_data(email)  # словарь с полными данными для создания пользователя
        response = MyRequests.post("/user/", data=data)  # POST: Create user
        Assertions.assert_status_code(response, 400)
        # проверка текста сообщения
        # response.content возвращает байтовую строку, поэтому преобразуем ее с помощью decode("utf-8")
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content '{response.content}'"

    @allure.title("This test try to create user if any field is missing in the request")
    @pytest.mark.parametrize("field", [
        "password",
        "username",
        "firstName",
        "lastName",
        "email"
    ])
    def test_try_create_user_without_any_field(self, field):
        """
        Тест проверяет невозможность создания пользователя, если нет одного из полей.
        Параметр 'field' определяет без какого поля будет попытка создания пользователя.
        Также проверяется значение status code и текст сообщения.
        """
        data = self.prepare_registration_data()  # словарь с полными данными для создания пользователя
        data.pop(field)
        response = MyRequests.post("/user/", data=data)  # POST: Create user
        Assertions.assert_status_code(response, 400)
        # проверка текста сообщения
        # response.content возвращает байтовую строку, поэтому преобразуем ее с помощью decode("utf-8")
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", \
            f"Unexpected response content '{response.content}'"

    @allure.title("This test try to create user if the 'username' field value is 1 character long")
    def test_try_create_user_with_the_shortest_name(self):
        """
        Тест проверяет невозможность создания пользователя, если поле 'username' длиной 1 символ.
        Также проверяется значение status code и текст сообщения.
        """
        data = self.prepare_registration_data()  # словарь с полными данными для создания пользователя
        data.update({"username": data["username"][0]})  # оставляем только первую букву имени
        response = MyRequests.post("/user/", data=data)  # POST: Create user
        Assertions.assert_status_code(response, 400)
        # проверка текста сообщения
        # response.content возвращает байтовую строку, поэтому преобразуем ее с помощью decode("utf-8")
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content '{response.content}'"

    @allure.title("This test try to create user if the 'username' field value is longer than 250 characters")
    def test_try_create_user_with_the_longest_name(self):
        """
        Тест проверяет невозможность создания пользователя, если поле 'username' длиной более 250 символов.
        Также проверяется значение status code и текст сообщения.
        """
        data = self.prepare_registration_data()  # словарь с полными данными для создания пользователя
        data.update({"username": self.random_string(251)})  # заменяем username на имя длиной более 250
        response = MyRequests.post("/user/", data=data)  # POST: Create user
        Assertions.assert_status_code(response, 400)
        # проверка текста сообщения
        # response.content возвращает байтовую строку, поэтому преобразуем ее с помощью decode("utf-8")
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"Unexpected response content '{response.content}'"
