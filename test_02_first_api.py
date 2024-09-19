"""
The command to run the tests via command line: pytest test_02_first_api.py -k "test_hello_call"
"""

import requests
class TestFirstApi:

    def test_hello_call(self):
        url = "https://playground.learnqa.ru/api/hello"
        name = "Vitalii"
        params = {"name": name}

        res = requests.get(url, params=params)
        assert res.status_code == 200, "The status code is not 200"

        res_dict = res.json()
        assert "answer" in res_dict, "The key 'answer' is missing in the response"

        expected_res_text = f"Hello, {name}"
        actual_res_text = res_dict["answer"]
        assert actual_res_text == expected_res_text, "Actual text in the response is not correct"