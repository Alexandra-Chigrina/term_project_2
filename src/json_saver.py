import json
import os.path
import logging
from typing import Any

from src.saver import Saver
from src.vacancy import Vacancy
from config import PATH_TO_JSON_DATA


logger = logging.getLogger("json_saver")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..", "logs", "json_saver.log"), "w", encoding="utf-8"
)
file_formatter = logging.Formatter("{asctime} {filename} {levelname}: {message}", style="{")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class JSONSaver(Saver):
    """Класс для сохранения вакансий в JSON-файл"""

    def __init__(self, filename: str = PATH_TO_JSON_DATA) -> None:
        self.__filename = filename

    def add_vacancy(self, vacancies: Vacancy | list[Vacancy]) -> None:
        """Добавление одной или нескольких вакансий в JSON-файл"""
        if isinstance(vacancies, Vacancy):
            vacancies = [vacancies]
        existing_vacancies = self._load_from_file()
        new_vacancies = [vac.to_dict() for vac in vacancies if vac.to_dict() not in existing_vacancies]
        if new_vacancies:
            existing_vacancies.extend(new_vacancies)
            self._save_to_file(existing_vacancies)
            logger.info(f"Добавлено {len(new_vacancies)} вакансий")
        else:
            logger.info("Нет новых вакансий для добавления.")

    def get_vacancies_data(self, criteria: Any) -> list[Vacancy]:
        """Получение вакансий по критериям (заглушка)"""
        logger.info("Метод get_vacancies пока не реализован.")
        return []

    def delete_vacancy(self, vacancies: Vacancy | list[Vacancy]) -> None:
        """Удаление одной или нескольких вакансий из JSON-файла"""
        if isinstance(vacancies, Vacancy):
            vacancies = [vacancies]
        existing_vacancies = self._load_from_file()
        updated_vacancies = [v for v in existing_vacancies if v not in [vac.to_dict() for vac in vacancies]]
        if len(existing_vacancies) == len(updated_vacancies):
            logger.warning("Ни одна из указанных вакансий не найдена в файле.")
        else:
            self._save_to_file(updated_vacancies)
            logger.info(f"Удалено {len(existing_vacancies) - len(updated_vacancies)} вакансий.")

    def _load_from_file(self) -> list[dict]:
        """Загрузка данных из JSON-файла"""
        if os.path.exists(self.__filename):
            try:
                with open(self.__filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                logger.warning("Файл поврежден или пуст, возвращен пустой список.")
                return []
        return []

    def _save_to_file(self, vacancies: list[dict]) -> None:
        """Сохранение данных в JSON-файл"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)
