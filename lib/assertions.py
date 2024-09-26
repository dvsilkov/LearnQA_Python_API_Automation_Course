from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_key(response: Response, key, expected_value, error_message):
        """ Метод проверяет, что ответ в формате JSON и значение по ключу 'key' имеет ожидаемое значение"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response is '{response.text}'"
        assert key in response_as_dict, f"Response does not have key '{key}'"
        assert response_as_dict[key] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, key):
        """ Метод проверяет, что ответ в формате JSON и в нем есть ключ 'key'"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response is '{response.text}'"
        assert key in response_as_dict, f"Response does not have key '{key}'"

    @staticmethod
    def assert_status_code(response: Response, exp_status_code):
        """ Метод проверяет какой статус код в ответе"""
        assert response.status_code == exp_status_code, f"Unexpected status code '{response.status_code}', expected value '{exp_status_code}'"
