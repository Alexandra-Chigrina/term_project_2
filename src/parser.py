from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    @abstractmethod
    def _connect_to_api(self) -> None:
        """Подключение к API (абстрактный метод)"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list[dict]:
        """Получение списка вакансий (абстрактный метод)"""
        pass
