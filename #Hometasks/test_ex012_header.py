import requests

"""
The command to run the tests via command line: pytest #Hometasks/test_ex011_header.py -s -k "test_header"
"""


class TestHeader:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        res = requests.get(url)
        header = res.headers
        print(header)
        #assert "HomeWork" in cookie_dict, "Cookie name is not 'Homework'"
        #assert cookie_dict["HomeWork"] == 'hw_value', "Cookie value is not 'hw_value'"
