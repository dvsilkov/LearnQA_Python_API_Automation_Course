from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        """ Метод проверяет, что ответ в формате JSON и значение по ключу name имеет ожидаемое значение"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response is '{response.text}'"
        assert name in response_as_dict, f"Response does not have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message
