import requests
import pytest

"""
The command to run the tests via command line: pytest #Hometasks/test_ex013_user_agent.py -s -k "test_user_agent"
"""


class TestUserAgent:
    user_agent_values = [
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    ]

    @pytest.mark.parametrize("user_agent", user_agent_values)
    def test_user_agent(self, user_agent):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        res = requests.get(url, headers={"User-Agent": user_agent})
        print(res.text)
        # assert "HomeWork" in cookie_dict, "Cookie name is not 'Homework'"
        # assert cookie_dict["HomeWork"] == 'hw_value', "Cookie value is not 'hw_value'"
