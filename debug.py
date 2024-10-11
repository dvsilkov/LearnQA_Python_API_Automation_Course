import os
from datetime import date

import requests
import random
import linecache
import string

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

def random_string(length):
    letters = string.ascii_lowercase
    rnd_str = ""
    for i in range(length):
        rnd_str += random.choice(letters)
    return rnd_str


print(random_string(250))

base_url = "https://playground.learnqa.ru/api"
url = "/user/"
full_url = base_url + url
email = "w@example.com"
data = {
    "password": "123",
    "username": "learnqa",
    "firstName": "learnqa",
    "lastName": "learnqa",
    "email": email
}
shortest_name = data["username"][0]
data.update({"username": random_string(251)})
print("name is: ", shortest_name)
response = requests.post(full_url, data=data)  # POST: Create user
print(response.status_code)
print(response.content)

person = Person.from_birth_year("Egor", 1978)
print(person.name, person.year, person.age)
print(Person.is_adult(30))

my_env = os.environ
print(my_env)

