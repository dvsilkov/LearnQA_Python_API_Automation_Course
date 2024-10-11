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

    @allure.title("This test get user details if use id or another authorized user")
    def test_get_user_details_auth_as_another_user(self):
        """
        Тест проверяет получение информации об авторизованном пользователе.
        Сначала происходит авторизация и получение cookie, token и id известного пользователя.
        Далее регистрация нового пользователя и также авторизация и получение cookie, token и id.
        Далее запрос данных известного клиента, но с использованием id нового клиента.
        В ответе должно быть только поле "username"
        """
        # LOGIN - авторизуемся под известным пользователем и получаем значения cookie, token и user id
        auth_sid, token, user_id_from_auth_method = self.user_logs_into_the_system()

        # REGISTER - регистрируем нового пользователя
        register_data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=register_data)  # POST: Create user
        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")
        email = register_data["email"]
        password = register_data["password"]
        username = register_data["username"]

        # LOGIN - авторизуемся под новым пользователем и получаем значения для него cookie, token и user id
        new_auth_sid, new_token, new_user_id_from_auth_method = self.user_logs_into_the_system(email, password)

        # GET - делаем запрос для получения данных первого авторизованного пользователя, но id от второго пользователя
        # GET: Get user info by id (you can get more info for user you are authorized as)
        response_2 = MyRequests.get(
            f"/user/{new_user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_key(response_2, "username", username, "Unknown username value")
        Assertions.assert_json_has_not_key(response_2, "email")
        Assertions.assert_json_has_not_key(response_2, "firstName")
        Assertions.assert_json_has_not_key(response_2, "lastName")
