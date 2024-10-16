"""
The command to run the tests via command line: pytest -s tests/test_user_edit.py
with allure: pytest -s --alluredir=allure_results/ tests/test_user_edit.py
run allure report: allure serve allure_results/
"""

import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User data editing cases")
class TestUserEdit(BaseCase):
    """ Класс с тестами по редактированию данных пользователя"""

    @allure.title("This test create new user, login into system and edit some field")
    def test_edit_just_created_auth_user(self):
        """
        Тест создает нового пользователя, авторизуется под ним, редактирует поле 'firstName'.
        После этого запрашивает данные по этому клиенту и проверяет, что значение поля 'firstName' изменено
        """
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=register_data)  # POST: Create user
        Assertions.assert_status_code(response_1,200)  # проверяем статус код
        Assertions.assert_json_has_key(response_1, "id")  # проверяем наличие поля 'id'

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response_1, "id")  # значение id пользователя

        # LOGIN
        login_data = {          # данные для авторизации
            "email": email,
            "password": password
        }

        response_2 = MyRequests.post("/user/login", data=login_data)  # POST: Logs user into the system
        auth_sid = self.get_cookie(response_2, "auth_sid")  # значение cookie
        token = self.get_header(response_2, "x-csrf-token")  # сам токен

        # EDIT
        new_name = "Changed name"
        # PUT: Update user (must be logged in as this user)
        response_3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response_3, 200)

        # GET
        response_4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_key(
            response_4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.title("This test create new user, login into system and edit 'email' field if address does not contain '@'")
    def test_edit_just_created_user_wrong_email(self):
        """
        Тест создает нового пользователя, авторизуется под ним.
        Далее попытка отредактировать поле 'email', но почтовый адрес не содержит символ '@'.
        Проверяет, status code и текст ошибки в ответе.
        """
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=register_data)  # POST: Create user
        Assertions.assert_status_code(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")
        email = register_data["email"]
        password = register_data["password"]

        # LOGIN - авторизуемся под новым пользователем и получаем значения для него cookie, token и user id
        auth_sid, token, user_id_from_auth_method = self.user_logs_into_the_system(email, password)

        # EDIT -
        new_email = email.replace("@", "")
        # PUT: Update user (must be logged in as this user)
        response_2 = MyRequests.put(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_status_code(response_2, 400)
        Assertions.assert_json_value_by_key(
            response_2,
            "error",
            "Invalid email format",
            "Incorrect error message"
        )



