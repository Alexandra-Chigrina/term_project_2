from unittest.mock import Mock, patch

import requests

from src.headhunter_api import HeadHunterAPI


def test_headhunter_api_init():
    api_hh = HeadHunterAPI()
    assert api_hh._HeadHunterAPI__url == "https://api.hh.ru/vacancies"
    assert api_hh._HeadHunterAPI__headers == {"User-Agent": "HH-User-Agent"}
    assert api_hh._HeadHunterAPI__params == {"text": "", "page": 0, "per_page": 100}
    assert api_hh._HeadHunterAPI__vacancies == []


@patch("requests.get")
def test_connect_to_api_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    response = api._connect_to_api()

    assert response is not None
    mock_get.assert_called_once_with(
        api._HeadHunterAPI__url, headers=api._HeadHunterAPI__headers, params=api._HeadHunterAPI__params
    )
    mock_response.raise_for_status.assert_called_once()


@patch("requests.get")
def test_connect_to_api_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException
    api = HeadHunterAPI()
    response = api._connect_to_api()
    assert response is None


@patch("requests.get")
def test_get_vacancies_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"items": [{"name": "Python Developer"}, {"name": "Backend Developer"}]}

    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    keyword = "Python Developer"
    vacancies = api.get_vacancies(keyword)

    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[1]["name"] == "Backend Developer"


@patch("requests.get")
def test_get_vacancies_unavailable(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python")

    assert vacancies == []
    assert mock_get.call_count == 1


@patch("requests.get")
def test_get_vacancies_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError

    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    keyword = "Python Developer"
    vacancies = api.get_vacancies(keyword)

    assert vacancies == []


@patch("requests.get")
def test_get_vacancies_no_more_vacancies(mock_get):
    mock_response_page_1 = Mock()
    mock_response_page_1.raise_for_status.return_value = None
    mock_response_page_1.json.return_value = {"items": [{"name": "Python Developer"}]}

    mock_response_page_2 = Mock()
    mock_response_page_2.raise_for_status.return_value = None
    mock_response_page_2.json.return_value = {"items": []}

    mock_get.side_effect = [mock_response_page_1, mock_response_page_2]

    api = HeadHunterAPI()
    keyword = "Python Developer"
    vacancies = api.get_vacancies(keyword)

    assert vacancies == [{"name": "Python Developer"}]
    assert mock_get.call_count == 2
