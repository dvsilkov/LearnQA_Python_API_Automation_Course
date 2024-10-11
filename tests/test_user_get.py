"""
The command to run the tests via command line: pytest -s tests/test_user_get.py
with allure: pytest -s --alluredir=allure_results/ tests/test_user_get.py
run allure report: allure serve allure_results/
"""

import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("User data acquisition cases")
class TestUserGet(BaseCase):
    """ Класс с тестами, где проверяется получение информации о пользователе"""

    @allure.title("This test get user details if he is not authorized")
    def test_get_user_details_not_auth(self):
        """
        Тест проверяет получение информации о неавторизованном пользователе.
        В ответе должно быть только поле "username"
        """
        user_id_not_auth = 2 # id неавторизованного пользователя
        # GET: Get user info by id (you can get more info for user you are authorized as)
        response = MyRequests.get(f"/user/{user_id_not_auth}")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("This test get user details if he is authorized")
    def test_get_user_details_auth_as_same_user(self):
        """
        Тест проверяет получение информации об авторизованном пользователе.
        Сначала происходит авторизация и получение cookie, token и id.
        В ответе должен быть полный набор полей: "username", "email", "firstName", "lastName"
        """
        # получаем значения cookie, token и user id
        auth_sid, token, user_id_from_auth_method = self.user_logs_into_the_system()

        # GET: Get user info by id (you can get more info for user you are authorized as)
        response = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response, expected_fields)
