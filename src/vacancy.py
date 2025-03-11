class Vacancy:
    """
    Класс для работы с вакансиями
    """
    __slots__ = ("title", "url", "salary_from", "salary_to", "description")

    def __init__(self,  title: str, url: str, salary_from: int = 0, salary_to: int = 0, description: str = None) -> None:
        self.title = title
        self.url = url
        self.salary_from = self.__validate_salary(salary_from)
        self.salary_to = self.__validate_salary(salary_to)
        self.description = description if description is not None else "Описание отсутствует"

    @staticmethod
    def __validate_salary(salary: int) -> int:
        """Проверяет корректность зарплаты"""
        return salary if isinstance(salary, int) and salary >= 0 else 0

