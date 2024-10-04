from datetime import date

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

""" Сравнение staticmethod и classmethod """


class Person:
    def __init__(self, name, year, age):
        self.name = name
        self.year = year
        self.age = age

    @classmethod
    def from_birth_year(cls, name, year):
        return cls(f"name: {name},", f"year: {year},", f"age from birth year: {date.today().year - year}")

    @staticmethod
    def is_adult(age):
        return age > 18


person = Person.from_birth_year("Egor", 1978)
print(person.name, person.year, person.age)
print(Person.is_adult(30))
