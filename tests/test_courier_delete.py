import json
import allure
import requests

from data.data import successful_ok_true_response, no_courier_with_such_id
from global_params import courier_url, headers
from utils.helpers import create_and_register_courier_and_return_login_password, courier_login


@allure.suite("DELETE /api/v1/courier/:id")
class TestCourierDeletion:

    @allure.title(f'Успешное удаление курьера.')
    @allure.description(f'Проверяется: тело ответа == "{successful_ok_true_response}" и статус код == 200.')
    def test_delete_courier_successfully(self):
        with allure.step("Регистрация курьера"):
            courier_creds = create_and_register_courier_and_return_login_password()
        with allure.step("Вход курьера в систему"):
            courier_id = courier_login(courier_creds['login'], courier_creds['password'])
        with allure.step("Сборка тела запроса и приведение к json"):
            payload = {
                "id": str(courier_id)
            }
            payload_string = json.dumps(payload)

        with allure.step("Отправка DELETE запроса для удаления курьера"):
            r = requests.delete(f'{courier_url}/{courier_id}', data=payload_string, headers=headers)

        with allure.step(f"Проверка: тело ответа == '{successful_ok_true_response}'"):
            assert r.text == successful_ok_true_response
        with allure.step(f"Проверка: статус код == 200"):
            assert r.status_code == 200

    @allure.title('Невозможно удалить несуществующего курьера.')
    @allure.description(f'Для проверки создается курьер, затем удаляется и удаляется еще раз. '
                        f'При повторной попытке удаления не происходит. '
                        f'Проверяется: ошибка == "{no_courier_with_such_id}" и статус код == 404.')
    def test_delete_courier_non_existent_courier_cannot_be_deleted(self):
        with allure.step("Регистрация курьера"):
            courier_creds = create_and_register_courier_and_return_login_password()
        with allure.step("Вход курьера в систему"):
            courier_id = courier_login(courier_creds['login'], courier_creds['password'])
        with allure.step("Сборка тела запроса и приведение к json"):
            payload = {
                "id": str(courier_id)
            }
            payload_string = json.dumps(payload)

        with allure.step("Отправка DELETE запроса для удаления курьера"):
            requests.delete(f'{courier_url}/{courier_id}', data=payload_string, headers=headers)
        with allure.step("Отправка повторного DELETE запроса для удаления того же курьера"):
            r = requests.delete(f'{courier_url}/{courier_id}', data=payload_string, headers=headers)

        with allure.step(f"Проверка: ошибка == '{no_courier_with_such_id}'"):
            assert r.json()['message'] == no_courier_with_such_id
        with allure.step(f"Проверка: статус код == 404"):
            assert r.status_code == 404
