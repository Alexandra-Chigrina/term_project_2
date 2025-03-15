import json
from unittest.mock import mock_open, patch

from config import PATH_TO_JSON_DATA
from src.json_saver import JSONSaver


def test_json_saver_init():
    custom_filename = "custom_vacancies.json"
    saver = JSONSaver(filename=custom_filename)
    assert saver._JSONSaver__filename == custom_filename

    saver_default = JSONSaver()
    assert saver_default._JSONSaver__filename == PATH_TO_JSON_DATA


def test_load_from_file(vacancy_json):
    mock_data = json.dumps(vacancy_json)
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_data)
    ) as mock_file:
        saver = JSONSaver("test_file.json")
        loaded_vacancies = saver._load_from_file()
    assert loaded_vacancies == vacancy_json
    mock_file.assert_called_once_with("test_file.json", "r", encoding="utf-8")


def test_load_from_file_incorrect_data():
    mock_data = json.dumps({"invalid": "data"})
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_data)
    ):
        saver = JSONSaver("test_file.json")
        loaded_vacancies = saver._load_from_file()
    assert loaded_vacancies == []


def test_load_from_file_error():
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data="{invalid json}")
    ), patch("json.load", side_effect=json.JSONDecodeError("Expecting value", doc="", pos=0)):
        saver = JSONSaver("test_file.json")
        loaded_vacancies = saver._load_from_file()
    assert loaded_vacancies == []


def test_load_from_file_not_exists():
    with patch("os.path.exists", return_value=False):
        saver = JSONSaver("test_file.json")
        loaded_vacancies = saver._load_from_file()
    assert loaded_vacancies == []


def test_save_to_file(vacancy_json):
    with patch("builtins.open", mock_open()) as mock_file:
        saver = JSONSaver("test_file.json")
        saver._save_to_file(vacancy_json)

    mock_file.assert_called_once_with("test_file.json", "w", encoding="utf-8")


def test_add_vacancy_new(first_vacancy):
    with patch("src.json_saver.JSONSaver._load_from_file", return_value=[]), patch(
        "src.json_saver.JSONSaver._save_to_file"
    ) as mock_save:
        saver = JSONSaver("test_file.json")
        saver.add_vacancy(first_vacancy)

    mock_save.assert_called_once_with([first_vacancy.to_dict()])


def test_add_vacancy_existing(first_vacancy):
    with patch("src.json_saver.JSONSaver._load_from_file", return_value=[first_vacancy.to_dict()]), patch(
        "src.json_saver.JSONSaver._save_to_file"
    ) as mock_save:
        saver = JSONSaver("test_file.json")
        saver.add_vacancy(first_vacancy)

    mock_save.assert_not_called()


def test_delete_vacancy_existing(second_vacancy):
    with patch("src.json_saver.JSONSaver._load_from_file", return_value=[second_vacancy.to_dict()]), patch(
        "src.json_saver.JSONSaver._save_to_file"
    ) as mock_save:

        saver = JSONSaver("test_file.json")
        saver.delete_vacancy(second_vacancy)

    mock_save.assert_called_once_with([])


def test_delete_vacancy_not_found(first_vacancy, second_vacancy):
    with patch("src.json_saver.JSONSaver._load_from_file", return_value=[second_vacancy.to_dict()]), patch(
        "src.json_saver.JSONSaver._save_to_file"
    ) as mock_save:

        saver = JSONSaver("test_file.json")
        saver.delete_vacancy(first_vacancy)

    mock_save.assert_not_called()
