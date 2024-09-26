import requests

"""
The command to run the tests via command line: pytest #Hometasks/test_ex011_cookie.py -s -k "test_cookie"
"""
class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        res = requests.get(url)
        cookie = res.cookies
        cookie_dict = dict(cookie)
        print(cookie, cookie_dict)
        assert "HomeWork" in cookie_dict, "Cookie name is not 'Homework'"
        assert cookie_dict["HomeWork"] == 'hw_value', "Cookie value is not 'hw_value'"
