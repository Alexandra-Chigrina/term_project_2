from abc import ABC, abstractmethod
from typing import Any

from src.vacancy import Vacancy


class Saver(ABC):  # pragma: no cover
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies_data(self, criteria: Any) -> list[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass
