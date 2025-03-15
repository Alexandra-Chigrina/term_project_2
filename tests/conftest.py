import pytest

from src.vacancy import Vacancy


@pytest.fixture
def first_vacancy():
    return Vacancy(
        title="Python-разработчик",
        url="https://hh.ru/vacancy/118199862",
        salary_from=120000,
        salary_to=150000,
        description="Владение Python. Знание основ Git. Знание библиотек pandas, requests.",
    )


@pytest.fixture
def second_vacancy():
    return Vacancy(
        title="Junior Python Developer",
        url="https://hh.ru/vacancy/110412718",
        salary_from=75000,
        salary_to=90000,
        description="Базовые знания Python. "
        "Опыт написания REST приложений на любом Python фреймворке (Flask, FastAPI, Django и др.).",
    )


@pytest.fixture
def third_vacancy():
    return Vacancy(
        title="Python-разработчик",
        url="https://hh.ru/vacancy/118199862",
        salary_from=-150,
    )


@pytest.fixture
def vacancy_json():
    return [
        {
            "name": "Программист (Junior - младший разработчик)",
            "alternate_url": "https://hh.ru/vacancy/118263819",
            "salary": {"from": 50000, "to": 70000},
            "snippet": {
                "requirement": "Знание одного из объектно-ориентированного языка программирования: "
                               "C++\\C#, Delphi, Python"
            },
        },
        {
            "name": "Python-разработчик",
            "alternate_url": "https://hh.ru/vacancy/118268562",
            "salary": {"from": 0, "to": 0},
            "snippet": {"requirement": "Опыт программирования на Python от 3 лет."},
        },
        {
            "name": "Python-разработчик",
            "alternate_url": "https://hh.ru/vacancy/118199862",
            "salary": {"from": 75000, "to": 100000},
            "snippet": {},
        },
    ]


@pytest.fixture
def vacancies():
    return [
        Vacancy("Python Developer", "http://example.com", 60000, 80000, "Опыт программирования на Python от 3 лет."),
        Vacancy("C++ Developer", "http://example.com", 70000, 90000, "Знание C++ и STL."),
        Vacancy("Java Developer", "http://example.com", 50000, 70000, "Опыт работы с Spring и Hibernate."),
    ]
