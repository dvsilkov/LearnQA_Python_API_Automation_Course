import requests
import allure

from lib.my_logger import MyLogger
from environment import env_object


class MyRequests:
    """ Класс с методами запросов """

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        """
        Метод для выполнения GET запроса.
        Принимает необходимые параметры и возвращает ответ
        """
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "GET")

    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        """
        Метод для выполнения POST запроса.
        Принимает необходимые параметры и возвращает ответ
        """
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        """
        Метод для выполнения PUT запроса.
        Принимает необходимые параметры и возвращает ответ
        """
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        """
        Метод для выполнения DELETE запроса.
        Принимает необходимые параметры и возвращает ответ
        """
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):
        """
        Название метода начинается с "_". Это приватный метод для использования внутри модуля или класса.
        Выполняет непосредственно запрос через библиотеку requests, исходя из переданных параметров
        """
        base_url = env_object.get_base_url()  # основной url в зависимости от выбранной переменной среды
        full_url = f"{base_url}{url}"  # полный url
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        # запись в лог параметров, с которыми сделан запрос
        MyLogger.add_request(full_url, data, headers, cookies, method)

        if method == "GET":
            response = requests.get(full_url, params=data, headers=headers, cookies=cookies)
        elif method == "POST":
            response = requests.post(full_url, data=data, headers=headers, cookies=cookies)
        elif method == "PUT":
            response = requests.put(full_url, data=data, headers=headers, cookies=cookies)
        elif method == "DELETE":
            response = requests.delete(full_url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        # запись ответа в лог
        MyLogger.add_response(response)

        return response
