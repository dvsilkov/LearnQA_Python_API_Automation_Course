import pprint
pp = pprint.PrettyPrinter(indent=4)

import requests
import json
print('API Testing is starting')

print("'''The Hello request'''")
payload = {'name': 'User'}
res = requests.get('https://playground.learnqa.ru/api/hello', params=payload)
print(res.text)

print("\n'''JSON parsing example'''")
string_as_json_format = '{"answer": "Hello, User"}'
obj = json.loads(string_as_json_format)     # получаем словарь
key = 'answer'
try:
    print('Type -', type(obj), '\nValue -', obj[key])
except KeyError:
    print(f"The key '{key}' is missing")

print("\n'''The get_text request'''")
res = requests.get('https://playground.learnqa.ru/api/get_text')
print(res.text)     # выводим ответ в виде текста
try:
    parsed_res_text = res.json()    # пробуем преобразовать в словарь
    print(parsed_res_text)
except requests.exceptions.JSONDecodeError:
    print("Response is not a JSON")

print("\n'''The check_type request'''")
# для GET параметры через аргумент params
res_get = requests.get('https://playground.learnqa.ru/api/check_type', params={"param_get": "value_get"})
print(res_get.text)     # выводим ответ с параметрами в виде текста
# для остальных типов запросов параметры через аргумент data
res_post = requests.post('https://playground.learnqa.ru/api/check_type', data={"param_post": "value_post"})
print(res_post.text)     # выводим ответ с параметрами в виде текста

print("\n'''The status_code requests'''")
res = requests.get('https://playground.learnqa.ru/api/check_type')      # успешный запрос с кодом 200
print(res.status_code, res.text)     # выводим код ответа и сам ответ
res = requests.get('https://playground.learnqa.ru/api/get_500')      # запрос с кодом 500
print(res.status_code, res.text)     # выводим код ответа но сам ответ пустой
res = requests.get('https://playground.learnqa.ru/api/something')      # запрос с кодом 404
print(res.status_code, res.text)     # выводим код ответа и сам ответ в виде HTML страницы
res = requests.get('https://playground.learnqa.ru/api/get_301')      # получаем ответ с кодом 403 Forbidden
print(res.status_code, res.text)     # выводим код ответа 403 и сам ответ
res = requests.get('https://playground.learnqa.ru/api/get_301', allow_redirects=False)      # получаем ответ с кодом 301
print(res.status_code, res.text)     # выводим код ответа 301 и сам ответ с сообщением о перенаправлении
res = requests.get('https://playground.learnqa.ru/api/get_301', allow_redirects=True)      # снова получаем ответ с кодом 403
print(res.status_code, res.text)     # выводим код ответа 403 и сам ответ
# объект ответа это массив, в котором содержатся ответы по всем URL, сколько было перенаправлений
first_res = res.history[0]      # изначальный ответ
second_res = res
print(f"The first URL: {first_res.url}\nThe second URL: {second_res.url}")  # выводим ссылки из ответов

print("\n'''Request and response headers'''")
headers = {"some_header": "123"}
res = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
print(res.text) # получаем ответ сервера с заголовками из запроса
print(res.headers) # получаем ответ сервера с заголовками из ответа

print("\n'''Get cookies'''")
payload = {"login": "secret_login", "password": "secret_pass"}
res = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)
print(res.text) # ответ будет пустой
print(res.status_code)
print(res.cookies) # выведет принт объекта похожего на словарь
print(dict(res.cookies)) # преобразовываем в словарь для читабельного вида
print(pp.pprint(dict(res.headers))) # через pprint выводим словарь в читаемом виде

print("\n'''Check cookies'''")
payload = {"login": "secret_login", "password": "secret_pass"}
res1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)
cookie_value = res1.cookies.get("auth_cookie") # получаем значение cookie по ключу "auth_cookie"
print(cookie_value)
cookies = {"auth_cookie": cookie_value} # создаем словарь с cookie
res2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies) # запрос с созданным cookie
print(res2.text)
