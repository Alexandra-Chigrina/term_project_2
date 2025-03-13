import pprint

from src.headhunter_api import HeadHunterAPI
import json

from src.json_saver import JSONSaver
from src.vacancy import Vacancy
from config import PATH_TO_JSON_DATA


# Создание экземпляра класса для работы с API сайтов с вакансиями
# hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
# hh_vacancies = hh_api.get_vacancies("Python")

# Преобразование набора данных из JSON в список объектов
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

# Пример работы контструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")

# Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем
def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    # platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")

    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(search_query)
    # print(json.dumps(hh_vacancies[:5], indent=4, ensure_ascii=False))
    print(len(hh_vacancies))

    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
    #
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    print(vacancies_list[0])
    print(vacancies_list[0].title)
    print(vacancies_list[0].url)
    print(vacancies_list[0].salary_from)
    print(vacancies_list[0].salary_to)
    pprint.pprint(vacancies_list[0].description, width=80)


    vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", 100000, 150000, "Требования: опыт работы от 3 лет...")
    json_saver = JSONSaver()

    json_saver.add_vacancy(vacancies_list[0:4])
    json_saver.add_vacancy(vacancy)
    json_saver.delete_vacancy(vacancies_list[0:2])
    json_saver.delete_vacancy(vacancy)
    #
    #
    # filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    #
    # ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    #
    # sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
