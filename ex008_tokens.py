'''
Иногда API-метод выполняет такую долгую задачу, что за один HTTP-запрос от него нельзя сразу получить готовый ответ.
Это может быть подсчет каких-то сложных вычислений или необходимость собрать информацию по разным источникам.
В этом случае на первый запрос API начинает выполнения задачи, а на последующие ЛИБО говорит, что задача еще не готова,
ЛИБО выдает результат. Сегодня я предлагаю протестировать такой метод.
Сам API-метод находится по следующему URL: https://playground.learnqa.ru/ajax/api/longtime_job

Если мы вызываем его БЕЗ GET-параметра token, метод заводит новую задачу, а в ответ выдает нам JSON со следующими полями:

* seconds - количество секунд, через сколько задача будет выполнена
* token - тот самый токен, по которому можно получить результат выполнения нашей задачи

Если же вызвать метод, УКАЗАВ GET-параметром token, то мы получим следующий JSON:

* error - будет только в случае, если передать token, для которого не создавалась задача. В этом случае в ответе будет следующая надпись - No job linked to this token
* status - если задача еще не готова, будет надпись Job is NOT ready, если же готова - будет надпись Job is ready
* result - будет только в случае, если задача готова, это поле будет содержать результат

Наша задача - написать скрипт, который делал бы следующее:

1) создавал задачу
2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
'''

import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
res_1 = requests.get(url) # первый запрос
res_1_to_json = res_1.json() # преобразовываем в словарь
token = res_1_to_json.get("token") # получаем значение по ключу token
seconds = res_1_to_json.get("seconds") # получаем значение по ключу seconds
print(token, seconds)

params = {"token": token} # словарь со значением полученного токена
res_2 = requests.get(url, params=params) # запрос с полученным токеном
print(res_2.text)

time.sleep(seconds) # ждем таймаут, полученный из первого запроса
res_3 = requests.get(url, params=params) # запрос с полученным токеном после таймаута
print(res_3.text)

params = {"token": token + "q"} # меняем токен на заведомо неверный
res_4 = requests.get(url, params=params) # запрос с неправильным токеном
print(res_4.text)

