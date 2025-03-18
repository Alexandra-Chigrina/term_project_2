from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies


def test_filter_vacancies(vacancies):
    filtered_vacancies = filter_vacancies(vacancies, ["Python"])
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].title == "Python Developer"


def test_get_vacancies_by_salary(vacancies):
    filtered_vac = get_vacancies_by_salary(vacancies, "55000", "75000")
    assert len(filtered_vac) == 2


def test_get_vacancies_by_salary_invalid_input(vacancies):
    filtered_vac = get_vacancies_by_salary(vacancies, "invalid", "75000")
    assert filtered_vac == []


def test_get_vacancies_by_salary_min_greater_than_max(vacancies):
    filtered = get_vacancies_by_salary(vacancies, "90000", "50000")
    assert filtered == []


def test_sort_vacancies(vacancies):
    sorted_vac = sort_vacancies(vacancies)
    assert sorted_vac[0].title == "C++ Developer"
    assert sorted_vac[-1].title == "Java Developer"


def test_get_top_vacancies(vacancies):
    sort_vac = sort_vacancies(vacancies)
    top_vacs = get_top_vacancies(sort_vac, "2")
    assert len(top_vacs) == 2
    assert top_vacs[0].title == "C++ Developer"
    assert top_vacs[1].title == "Python Developer"


def test_get_top_vacancies_invalid_input(vacancies, capsys):
    top_vacs = get_top_vacancies(vacancies, "invalid")
    message = capsys.readouterr()
    assert top_vacs == []
    assert message.out.strip() == "Ошибка: Введите числовое значение для количества вакансий."


def test_get_top_vacancies_negative__int_input(vacancies, capsys):
    top_vacs = get_top_vacancies(vacancies, "-2")
    message = capsys.readouterr()
    assert top_vacs == []
    assert message.out.strip() == "Ошибка: Количество вакансий не должно быть отрицательным числом."


def test_print_vacancies_empty(capsys):
    print_vacancies([])
    message = capsys.readouterr()
    assert message.out.strip() == "Нет вакансий для отображения."


def test_print_vacancies(vacancies, capsys):
    print_vacancies(vacancies)
    message = capsys.readouterr()
    assert "1. Python Developer" in message.out
    assert "2. C++ Developer\n", "Зарплата: 70000 - 90000" in message.out
