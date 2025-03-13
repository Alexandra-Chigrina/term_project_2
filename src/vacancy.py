import logging
import os
from typing import Optional

logger = logging.getLogger("vacancy")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..", "logs", "vacancy.log"), "w", encoding="utf-8"
)
file_formatter = logging.Formatter("{asctime} {filename} {levelname}: {message}", style="{")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    __slots__ = ("title", "url", "salary_from", "salary_to", "description")

    def __init__(
        self, title: str, url: str, salary_from: int = 0, salary_to: int = 0, description: Optional[str] = None
    ) -> None:
        self.title = title
        self.url = url
        self.salary_from = self.__validate_salary(salary_from)
        self.salary_to = self.__validate_salary(salary_to)
        self.description = description if description is not None else "Описание отсутствует"

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнение по минимальной зарплате, если не указана - по максимальной"""
        return (self.salary_from or self.salary_to) < (other.salary_from or other.salary_to)

    def __gt__(self, other: "Vacancy") -> bool:
        return (self.salary_from or self.salary_to) > (other.salary_from or other.salary_to)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (self.salary_from or self.salary_to) == (other.salary_from or other.salary_to)

    def to_dict(self) -> dict:
        """Метод для преобразования объекта вакансии в словарь"""
        return {
            "title": self.title,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "description": self.description,
        }

    @staticmethod
    def __validate_salary(salary: int) -> int:
        """Проверяет корректность зарплаты"""
        return salary if isinstance(salary, int) and salary >= 0 else 0

    @classmethod
    def cast_to_object_list(cls, vacancies_json: list[dict]) -> list["Vacancy"]:
        """Преобразование списка вакансий из JSON в список объектов Vacancy"""
        logger.info("Преобразование JSON в объекты Vacancy")
        vacancies_list = []
        for item in vacancies_json:
            salary = item.get("salary", {})
            salary_from = salary["from"] if isinstance(salary, dict) and salary.get("from") is not None else 0
            salary_to = salary["to"] if isinstance(salary, dict) and salary.get("to") is not None else 0
            vacancies_list.append(
                cls(
                    title=item.get("name", ""),
                    url=item.get("alternate_url", ""),
                    salary_from=salary_from,
                    salary_to=salary_to,
                    description=item.get("snippet", {}).get("requirement", "Описание отсутствует"),
                )
            )
        logger.info(f"Создано {len(vacancies_list)} вакансий.")

        return vacancies_list
