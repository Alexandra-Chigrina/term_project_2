from src.vacancy import Vacancy


def test_vacancy_init(first_vacancy, second_vacancy):
    assert first_vacancy.title == "Python-разработчик"
    assert first_vacancy.url == "https://hh.ru/vacancy/118199862"
    assert first_vacancy.salary_from == 120000
    assert first_vacancy.salary_to == 150000
    assert first_vacancy.description == "Владение Python. Знание основ Git. Знание библиотек pandas, requests."


def test_salary_validation_negative(third_vacancy):
    assert third_vacancy.salary_from == 0


def test_vacancy_comparison(first_vacancy, second_vacancy):

    assert first_vacancy > second_vacancy
    assert second_vacancy < first_vacancy
    assert first_vacancy != second_vacancy


def test_vacancy_equality_with_other_type(first_vacancy):
    non_vacancy_object = "не вакансия"

    assert first_vacancy.__eq__(non_vacancy_object) is NotImplemented


def test_to_dict_method(first_vacancy):
    vacancy_dict = first_vacancy.to_dict()

    expected_dict = {
        "title": "Python-разработчик",
        "url": "https://hh.ru/vacancy/118199862",
        "salary_from": 120000,
        "salary_to": 150000,
        "description": "Владение Python. Знание основ Git. Знание библиотек pandas, requests.",
    }

    assert vacancy_dict == expected_dict


def test_cast_to_object_list(vacancy_json):
    vacancies = Vacancy.cast_to_object_list(vacancy_json)
    assert len(vacancies) == 3
    assert vacancies[0].title == "Программист (Junior - младший разработчик)"
    assert vacancies[0].salary_from == 50000
    assert vacancies[0].salary_to == 70000
    assert (
        vacancies[0].description
        == "Знание одного из объектно-ориентированного языка программирования: C++\\C#, Delphi, Python"
    )

    assert vacancies[1].title == "Python-разработчик"
    assert vacancies[1].salary_from == 0
    assert vacancies[1].salary_to == 0
    assert vacancies[1].description == "Опыт программирования на Python от 3 лет."

    assert vacancies[2].title == "Python-разработчик"
    assert vacancies[2].url == "https://hh.ru/vacancy/118199862"
    assert vacancies[2].description == "Описание отсутствует"
