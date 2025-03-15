from unittest.mock import patch
from src.user_interaction import user_interaction

def test_user_interaction(vacancies):
    with patch("builtins.input", side_effect=["Developer", "2", "Python", "60000", "100000"]), \
         patch("src.headhunter_api.HeadHunterAPI.get_vacancies", return_value=[vac.to_dict() for vac in vacancies]), \
         patch("src.vacancy.Vacancy.cast_to_object_list", return_value=vacancies), \
         patch("src.json_saver.JSONSaver.add_vacancy"), \
         patch("src.utils.filter_vacancies", return_value=[vacancies[0]]), \
         patch("src.utils.get_vacancies_by_salary", return_value=[vacancies[0]]), \
         patch("src.utils.sort_vacancies", return_value=[vacancies[0]]), \
         patch("src.user_interaction.print_vacancies") as mock_print:

        user_interaction()

    mock_print.assert_called_once_with([vacancies[0]])
