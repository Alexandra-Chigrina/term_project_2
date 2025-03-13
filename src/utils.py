import logging
import os

from src.vacancy import Vacancy

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..", "logs", "utils.log"), "w", encoding="utf-8"
)
file_formatter = logging.Formatter("{asctime} {filename} {levelname}: {message}", style="{")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def filter_vacancies(vacancies: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """Фильтрация вакансий по ключевым словам в описании"""
    return [vac for vac in vacancies if any(word.lower() in vac.description.lower() for word in filter_words)]


def get_vacancies_by_salary(vacancies: list[Vacancy], salary_min: str, salary_max: str) -> list[Vacancy]:
    """Фильтрация вакансий по диапазону зарплаты с проверкой входных данных"""
    try:
        salary_min_int = int(salary_min)
        salary_max_int = int(salary_max)
    except ValueError:
        logger.error("Ошибка: Введены некорректные данные для зарплаты.")
        print("Ошибка: Введите числовые значения для зарплатного диапазона.")
        return []

    if salary_min_int > salary_max_int:
        logger.warning("Ошибка: Минимальная зарплата больше максимальной.")
        print("Ошибка: Минимальная зарплата не может быть больше максимальной.")
        return []

    filtered_vacancies = [vac for vac in vacancies if salary_min_int <= vac.salary_from <= salary_max_int]

    return filtered_vacancies


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """Сортировка вакансий по зарплате (по убыванию)"""
    return sorted(vacancies, reverse=True, key=lambda vac: vac.salary_from or vac.salary_to)


def get_top_vacancies(vacancies: list[Vacancy], top_n: str) -> list[Vacancy]:
    """Получение топ-N вакансий"""
    try:
        top_n_int = int(top_n)
    except ValueError:
        logger.error("Ошибка: Введены некорректные данные для количества вакансий.")
        print("Ошибка: Введите числовое значение для количества вакансий.")
        return []

    if top_n_int < 0:
        logger.warning("Ошибка: Количество вакансий отрицательное число.")
        print("Ошибка: Количество вакансий не должно быть отрицательным числом.")
        return []

    return vacancies[:top_n_int]


def print_vacancies(vacancies: list[Vacancy]) -> None:
    """Вывод списка вакансий"""
    if not vacancies:
        print("Нет вакансий для отображения.")
        return

    for index, vacancy in enumerate(vacancies, start=1):
        print(f"{index}. {vacancy.title}")
        print(f"   Зарплата: {vacancy.salary_from} - {vacancy.salary_to}")
        print(f"   URL: {vacancy.url}")
        print(f"   Описание: {vacancy.description[:100]}...")
        print("-" * 80)
