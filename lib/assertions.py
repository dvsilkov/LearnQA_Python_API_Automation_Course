import allure
from requests import Response
import json


class Assertions:
    """Класс с методами для различных проверок полученного ответа """
    @staticmethod
    def assert_json_value_by_key(response: Response, key, expected_value, error_message):
        """ Метод проверяет, что ответ в формате JSON и значение по ключу 'key' имеет ожидаемое значение"""
        with allure.step(f"Check the JSON value by the key in the response"):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not JSON format. Response is '{response.text}'"
            assert key in response_as_dict, f"Response does not have key '{key}'"
            assert response_as_dict[key] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, key):
        """ Метод проверяет, что ответ в формате JSON и в нем есть ключ 'key'"""
        with allure.step(f"Check that the JSON response has necessary key"):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not JSON format. Response is '{response.text}'"
            assert key in response_as_dict, f"Response does not have key '{key}'"

    @staticmethod
    def assert_json_has_keys(response: Response, keys: list):
        """ Метод проверяет, что ответ в формате JSON и в нем есть набор ключей 'keys'"""
        with allure.step(f"Check that the JSON response has necessary keys"):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not JSON format. Response is '{response.text}'"
            for key in keys:
                assert key in response_as_dict, f"Response does not have key '{key}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, key):
        """ Метод проверяет, что ответ в формате JSON и в нем нет определенного ключа 'key'"""
        with allure.step(f"Check that the JSON response has not a specific key"):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not JSON format. Response is '{response.text}'"
            assert key not in response_as_dict, f"Response JSON should not have key '{key}'. But it is present"

    @staticmethod
    def assert_status_code(response: Response, exp_status_code):
        """ Метод проверяет какой статус код в ответе"""
        with allure.step(f"Check that the response has a correct status code"):
            assert response.status_code == exp_status_code, \
                f"Unexpected status code '{response.status_code}', expected value '{exp_status_code}'"
