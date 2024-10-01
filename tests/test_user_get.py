import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserGet(BaseCase):
    """ Класс с тестами, где проверяется получение информации о пользователе"""

    def test_get_user_details_not_auth(self):
        """
        Тест проверяет получение информации о неавторизованном пользователе.
        В ответе должно быть только поле "username"
        """
        user_id_not_auth = 2 # id неавторизованного пользователя
        # GET: Get user info by id (you can get more info for user you are authorized as)
        url = f"https://playground.learnqa.ru/api/user/{user_id_not_auth}"
        response = requests.get(url)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self, user_logs_into_the_system):
        """
        Тест проверяет получение информации об авторизованном пользователе.
        Сначала происходит авторизация и получение cookie, token и id.
        В ответе должен быть полный набор полей: "username", "email", "firstName", "lastName"
        """

        # GET: Get user info by id (you can get more info for user you are authorized as)
        url_2 = f"https://playground.learnqa.ru/api/user/{user_logs_into_the_system["user_id_from_auth_method"]}"
        response_2 = requests.get(
            url_2,
            headers={"x-csrf-token": user_logs_into_the_system["token"]},
            cookies={"auth_sid": user_logs_into_the_system["auth_sid"]}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response_2, expected_fields)
