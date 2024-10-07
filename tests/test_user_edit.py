import allure
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User data editing cases")
class TestUserEdit(BaseCase):
    """ Класс с тестами по редактированию данных пользователя"""

    @allure.description("This test create new user, login into system and edit some field")
    def test_edit_just_created_user(self):
        """
        Метод
        """
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=register_data) # POST: Create user
        Assertions.assert_status_code(response_1,200)
        Assertions.assert_json_has_key(response_1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response_1, "id") # значение id пользователя

        # LOGIN
        login_data = {          # данные для авторизации
            "email": email,
            "password": password
        }

        response_2 = MyRequests.post("/user/login" , data=login_data) # POST: Logs user into the system
        auth_sid = self.get_cookie(response_2, "auth_sid")  # значение cookie
        token = self.get_header(response_2, "x-csrf-token")  # сам токен

        # EDIT
        new_name = "Changed name"
        response_3 = MyRequests.put(                # PUT: Update user (must be logged in as this user)
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid":auth_sid},
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
