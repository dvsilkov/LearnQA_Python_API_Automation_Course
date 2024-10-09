from datetime import datetime
import os

from requests import Response


class MyLogger:
    """
    Класс с методами для записи в лог запросов и ответов
    """

    # имя файла
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = rf"C:\Users\Denis_Silkov.EPAM\Documents\Trainings\Python\LearnQA_Python_API_Automation_Course\logs"
    file_name = rf"{path}\log_{time}.log"

    @classmethod
    def _write_log_to_file(cls, data: str):
        """
        Название метода начинается с "_". Это приватный метод для использования внутри модуля или класса.
        Декоратор @classmethod, чтобы был доступ к атрибутам класса. Вместо "self" используется "cls".
        Метод используется для непосредственной записи события в файл.
        """
        with open(cls.file_name, "a", encoding="utf-8") as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        """
        Декоратор @classmethod, чтобы был доступ к атрибутам класса. Вместо "self" используется "cls".
        Метод на входе получает данные, с которыми был сделан запрос, приводит их соответствующему виду, добавляя время.
        Записывается все файл с помощью метода "_write_log_to_file"
        """
        test_name = os.environ.get("PYTEST_CURRENT_TEST") # получение имени запущенного теста

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {datetime.now()}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += f"\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        """
        Декоратор @classmethod, чтобы был доступ к атрибутам класса. Вместо "self" используется "cls".
        Метод получает на вход ответ на запрос. Из ответа берутся нужные данные.
        Записывается все файл с помощью метода "_write_log_to_file"
        """
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += f"-----\n"

        cls._write_log_to_file(data_to_add)



