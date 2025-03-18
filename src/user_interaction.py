import logging
import os

from src.headhunter_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy import Vacancy

logger = logging.getLogger("user-interaction")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..", "logs", "user-interaction.log"), "w", encoding="utf-8"
)
file_formatter = logging.Formatter("{asctime} {filename} {levelname}: {message}", style="{")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем"""
    logger.info("Запуск взаимодействия с пользователем")
    search_query = input("Введите поисковый запрос: ")
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    logger.info(f"Загружено {len(vacancies_list)} вакансий")

    json_saver = JSONSaver()
    json_saver.add_vacancy(vacancies_list)
    logger.info("Вакансии сохранены в JSON-файл.")

    top_n = input("Введите количество вакансий для вывода в топ N: ")
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_min = input("Введите минимальную зарплату: ")
    salary_max = input("Введите максимальную зарплату: ")

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    logger.info(f"Отфильтровано {len(filtered_vacancies)} вакансий по ключевым словам")
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_min, salary_max)
    logger.info(f"Осталось {len(ranged_vacancies)} вакансий после фильтрации по зарплате")
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    logger.info(f"Выведено {len(top_vacancies)} топ-вакансий пользователю")
    print_vacancies(top_vacancies)
    return
