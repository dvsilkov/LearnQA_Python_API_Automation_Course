import requests
import random
import linecache

url = "https://playground.learnqa.ru/api/user/login"
data = {
    "email": "vinkotov@example.com",
    "password": "1234"
}
res = requests.post(url, data=data)
res_dict = res.json().get("user_id")
print(res_dict)
print(res.cookies)
print(res.headers)

auth_sid = res.cookies.get("auth_sid")  # значение cookie
token = res.headers.get("x-csrf-token")  # сам токен

res2 = requests.get("https://playground.learnqa.ru/api/user/auth", cookies={"auth_sid": auth_sid},
                    headers={"x-csrf-token": token})
print(res2.json().get("user_id"))
