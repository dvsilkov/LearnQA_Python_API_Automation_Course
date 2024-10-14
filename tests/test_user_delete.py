"""
The command to run the tests via command line: pytest -s tests/test_user_delete.py
with allure: pytest -s --alluredir=allure_results/ tests/test_user_delete.py
run allure report: allure serve allure_results/
"""

import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User deletion cases")
class TestUserDelete(BaseCase):
    """ Класс с тестами по удалению пользователя"""

    @allure.title("This test try to delete not authorized user")
    def test_delete_not_auth_user(self):
        """
        Тест делает попытку удаления пользователя, который не авторизован'.
        Проверяет, что статус код 400 и текст ответа.
        """

        # id пользователя для удаления
        user_id = 2

        # DELETE: Delete user by id (must be logged in as this user)
        response = MyRequests.delete(f"/user/{user_id}")
        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_value_by_key(
            response,
            "error",
            "Auth token not supplied",
            "Incorrect error message"
        )

    @allure.title("This test delete authorized user")
    def test_delete_auth_user(self):
        """
        Тест создает нового пользователя, авторизуется под ним.
        Удаляет авторизованного пользователя. Проверяет статус код и текст ответа.
        Делает запрос данных по нему. Проверяет статус код и текст ответа.
        """

        # REGISTRATION POST: Create user
        register_data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response_1, "id")

        # LOGIN POST: Logs user into the system
        data = {
            "email": email,
            "password": password
        }
        response_2 = MyRequests.post("/user/login", data=data)
        Assertions.assert_status_code(response_2, 200)
        Assertions.assert_json_value_by_key(response_2, "user_id", int(user_id), "User id mismatch")
        auth_sid = self.get_cookie(response_2, "auth_sid")  # значение cookie
        token = self.get_header(response_2, "x-csrf-token")  # сам токен

        # DELETE: Delete user by id (must be logged in as this user)
        response_3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_status_code(response_3, 200)
        Assertions.assert_json_value_by_key(
            response_3,
            "success",
            "!",
            "Incorrect error message"
        )
