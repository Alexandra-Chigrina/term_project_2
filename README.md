# **Term_project_#2 - HeadHunter API Vacancy Parser**

## **Описание**:

Данный проект представляет собой парсер вакансий с HeadHunter API, который позволяет:

- искать вакансии по ключевому слову;
- фильтровать вакансии по зарплате и ключевым словам;
- сортировать вакансии;
- сохранять вакансии в JSON-файл.

## **Установка**:

1. Клонируйте репозиторий

```
git@github.com:Alexandra-Chigrina/term_project_2.git
```

2. В терминале инициализируйте Poetry и активируйте виртуальное окружение

```
poetry init
poetry shell
```

3. Установите зависимости

```
pip install -r requirements.txt
```

## **Использование**:

### Запуск основного модуля.

   Запустите скрипты из модуля main.py в корне репозитория.   
   Модуль main.py связывает все функциональности проекта, вызывая ключевые функции.

```commandline
python main.py
```

При запуске программы пользователь вводит ключевое слово для поиска вакансий, найденные вакансии сохраняются
в JSON-файл.  
Затем программа предлагает:

- ввести количество вакансий для вывода (топ-N);
- фильтровать вакансии по ключевым словам;
- фильтровать вакансии по диапазону зарплаты.

После обработки данные сортируются, и результаты выводятся на экран. 

### Описание основных классов и функций

* Класс `HeadHunterAPI` - класс для работы с API HeadHunter  
  Модуль: src/headhunter_api.py  
  Наследуется от: Parser  
```commandline
class HeadHunterAPI(Parser):
```

Основные методы:  
`_connect_to_api() -> Response | None` – подключение к API hh.ru  
`get_vacancies(keyword: str) -> list[dict]` – поиск вакансий по ключевому слову

* Класс `Vacancy` - класс вакансии  
Модуль: src/vacancy.py

```commandline
class Vacancy:
```

Основные методы:  
`to_dict() -> dict` – конвертация объекта в словарь  
`cast_to_object_list(vacancies_json: list[dict]) -> list["Vacancy"]` – создание списка объектов Vacancy

Методы сравнения: __lt__, __gt__, __eq__ – сравнение по зарплате

* Класс `JSONSaver` - класс для работы с JSON-файлом  
Модуль: src/json_saver.py  
Наследуется от: Saver  
```commandline
class JSONSaver(Saver):
```

Основные методы:  
`add_vacancy(vacancies: Vacancy | list[Vacancy]) -> None` – добавление вакансий  
`delete_vacancy(vacancies: Vacancy | list[Vacancy]) -> None` – удаление вакансий  
`_load_from_file() -> list[dict]` – загрузка данных из JSON  
`_save_to_file(vacancies: list[dict]) -> None` – сохранение в JSON

* Класс `Saver` - абстрактный класс для сохранения вакансий  
Модуль: src/saver.py  
Наследуется от: ABC  
```commandline
class Saver(ABC):
```

Абстрактные методы (должны быть реализованы в потомках):  
`add_vacancy(vacancy: Vacancy) -> None`  
`get_vacancies_data(criteria: Any) -> list[Vacancy]`  
`delete_vacancy(vacancy: Vacancy) -> None`  

* Класс `Parser` - абстрактный класс для работы с API  
Модуль: src/parser.py  
Наследуется от: ABC  
```commandline
class Parser(ABC):
```

Абстрактные методы (должны быть реализованы в потомках):  
`_connect_to_api() -> Response | None` – подключение к API  
`get_vacancies(keyword: str) -> list[dict]` – получение списка вакансий

* `Utils` - вспомогательные функции  
Модуль: src/utils.py

Функции:  
`filter_vacancies()` – фильтрация вакансий по ключевым словам  
`get_vacancies_by_salary()` – фильтрация по зарплате  
`sort_vacancies()` – сортировка по убыванию зарплаты  
`get_top_vacancies()` – получение N лучших вакансий  
`print_vacancies()` – вывод вакансий в консоль  

* Функция `user_interaction()` - обработка пользовательского ввода    
Модуль: src/user_interaction.py
```commandline
def user_interaction() -> None:
```
Процесс:  
- получает запрос от пользователя;
- ищет вакансии через HeadHunterAPI;
- сохраняет вакансии в JSONSaver;
- фильтрует и сортирует вакансии через Utils;
- выводит вакансии пользователю.


## **Тестирование**

1. Установите pytest через Poetry

```
poetry add --group dev pytest
```

2. Запустить тестирование можно из модулей 'test_name', находящихся в папке 'tests' или в терминале

```
pytest
```

3. Для анализа покрытия кода тестами установите библиотеку 'pytest-cov'

```commandline
poetry add --group dev pytest-cov
```

4. Запустите тесты с оценкой покрытия

```commandline
pytest --cov=src --cov-report=term-missing tests/
``` 


## **Структура проекта**

├── src/                         # Основной код  
│   ├── parser.py                # Абстрактный класс для работы с API вакансий  
│   ├── saver.py                 # Абстрактный класс для сохранения вакансий  
│   ├── headhunter_api.py        # Класс для работы с API HeadHunter  
│   ├── vacancy.py               # Класс для работы с вакансиями  
│   ├── json_saver.py            # Сохранение вакансий в JSON-файл  
│   ├── utils.py                 # Фильтрация, сортировка, вывод вакансий  
│   ├── main.py                  # Взаимодействие с пользователем  
├── data/                        # Данные  
│   ├── vacancy.json             # Файл с сохраненными вакансиями  
├── tests/                       # Тесты  
│   ├── test_headhunter_api.py   # Тесты для headhunter_api.py  
│   ├── test_vacancy.py          # Тесты для vacancy.py   
│   ├── test_json_saver.py       # Тесты для json_saver.py  
│   ├── test_utils.py            # Тесты для utils.py    
│   ├── test_main.py             # Тесты для main.py   
├── logs                         # Логи работы программы  
├── main.py                      # Основная логика проекта  
├── user_settings.json      # Файл пользовательских настроек  
├── .venv                   # Виртуальное окружение  
├── .git/                   # Git-репозиторий  
├── .gitignore              # Исключения файлов из Git  
├── .config.py              # Файл конфигурации  
├── .flake8                 # Настройки линтера Flake8  
├── .coverage               # Отчеты покрытия кода тестами  
├── .poetry.lock            # Фиксированные зависимости проекта  
├── .pyproject.toml         # Основной конфигурационный файл проекта  
├── README.md               # Документация  
