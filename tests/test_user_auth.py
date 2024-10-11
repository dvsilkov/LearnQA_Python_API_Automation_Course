"""
The command to run the tests via command line: pytest -s tests/test_user_auth.py
with allure: pytest -s --alluredir=allure_results/ tests/test_user_auth.py
run allure report: allure serve allure_results/
"""
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    """ Класс с тестами по проверке авторизации пользователя"""
    # Параметры для негативного теста
    exclude_params = [
        "no_cookies",
        "no_token"
    ]

    @allure.title("This test successfully authorize user by email and password")
    def test_auth_user(self):
        """
        Успешный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup
        """
        # получаем значения cookie, token и user id
        auth_sid, token, user_id_from_auth_method = self.user_logs_into_the_system()

        # GET: Get user id you are authorizes as OR get 0 if not authorized
        # запрос с использованием данных, полученных из запроса где происходи логин в методе "user_logs_into_the_system"
        res_2 = MyRequests.get(
            "/user/auth",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        # проверка, что в ответе есть id пользователя и что user id совпадают в обоих запросах
        Assertions.assert_json_value_by_key(
            res_2,
            "user_id",
            user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.title("This test checks authorization status without token or cookie")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_user(self, condition):
        """
        Негативный сценарий проверки аутентификации с использованием уже полученных cookies и headers в методе setup.
        Имеет параметр с двумя значениями, для запроса без cookies и без headers.
        В обоих случаях в ответе user_id должен быть равен 0
        """
        # получаем значения cookie, token и user id
        auth_sid, token, user_id_from_auth_method = self.user_logs_into_the_system()

        # GET Get user id you are authorizes as OR get 0 if not authorized
        # запрос с использованием данных, полученных из ответа после логина в методе "user_logs_into_the_system"
        if condition == "no_cookies":
            res_2 = MyRequests.get("/user/auth", headers={"x-csrf-token": token})
        else:
            res_2 = MyRequests.get("/user/auth", cookies={"auth_sid": auth_sid})

        # проверка, что в ответе есть id пользователя и что user id равен 0 во втором запросе
        Assertions.assert_json_value_by_key(
            res_2,
            "user_id",
            0,
            f"User has been authorized with condition {condition}"
        )
