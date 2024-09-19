"""
The command to run the tests via command line: pytest test_03_api_parametrize.py -k "test_hello_call"
"""
import pytest
import requests


class TestFirstApi:
    names = [
        ["Vitalii", "Hello, "],
        ["Arseniy", "Hello, "],
        ["", "Hello, someone"]
    ]

    @pytest.mark.parametrize("name, answer", names)
    def test_hello_call(self, name, answer):
        url = "https://playground.learnqa.ru/api/hello"
        params = {"name": name}

        res = requests.get(url, params=params)
        assert res.status_code == 200, "The status code is not 200"

        res_dict = res.json()
        assert "answer" in res_dict, "The key 'answer' is missing in the response"

        expected_res_text = f"{answer}{name}"
        actual_res_text = res_dict["answer"]
        assert actual_res_text == expected_res_text, "Actual text in the response is not correct"
