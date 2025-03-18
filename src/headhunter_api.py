import logging
import os
from typing import Any

import requests
from requests import Response

from src.parser import Parser

logger = logging.getLogger("headhunter_api")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..", "logs", "headhunter_api.log"), "w", encoding="utf-8"
)
file_formatter = logging.Formatter("{asctime} {filename} {levelname}: {message}", style="{")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: dict[str, Any] = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies: list[dict] = []

    def _connect_to_api(self) -> Response | None:
        """Приватный метод подключения к API"""
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            response.raise_for_status()
            logger.info("Успешное подключение к API hh.ru")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка подключения к API hh.ru: {e}")
            return None

    def get_vacancies(self, keyword: str) -> list[dict]:
        """Получение списка вакансий с hh.ru"""
        logger.info(f"Поиск вакансий по ключевому слову: {keyword}")
        self.__params["text"] = keyword
        self.__params["page"] = 0
        self.__vacancies = []

        while self.__params["page"] < 20:
            response = self._connect_to_api()
            if response is None:
                logger.error("Ошибка: API недоступен, завершение работы.")
                break

            try:
                vacancies = response.json().get("items", [])
            except ValueError:
                logger.error("Ошибка обработки JSON, получен некорректный ответ от сервера.")
                break

            if not vacancies:
                logger.info("Вакансий больше нет, завершение поиска.")
                break

            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

        logger.info(f"Найдено {len(self.__vacancies)} вакансий.")
        return self.__vacancies
