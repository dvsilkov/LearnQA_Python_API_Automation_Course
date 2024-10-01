import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    """ Класс с тестами"""
    def test_edit_just_created_user(self):
        """
        Метод
        """
        # REGISTRATION
        url_reg = "https://playground.learnqa.ru/api/user/"  # POST: Create user
        register_data = self.prepare_registration_data()
        response_1 = requests.post(url_reg, data=register_data)
        Assertions.assert_status_code(response_1,200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response_1, "id") # значение id пользователя

        # LOGIN
        url_login = "https://playground.learnqa.ru/api/user/login"  # POST: Logs user into the system

        # данные для авторизации
        login_data = {
            "email": email,
            "password": password
        }

        response_2 = requests.post(url_login, data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")  # значение cookie
        token = self.get_header(response_2, "x-csrf-token")  # сам токен

        # EDIT
        new_name = "Changed name"
        url_get = f"https://playground.learnqa.ru/api/user/{user_id}" # PUT: Update user (must be logged in as this user)
        response_3 = requests.put(
            url_get,
            headers={"x-csrf-token": token},
            cookies={"auth_sid":auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response_3, 200)

        # GET
        response_4 = requests.get(
            url_get,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_key(
            response_4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )
