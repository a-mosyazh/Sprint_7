import json
import allure
import pytest
import requests

from data.data import not_enough_data_for_login, courier_not_found
from global_params import headers, courier_login_url
from utils.helpers import create_and_register_courier_and_return_login_password, delete_courier


@allure.suite("POST /api/v1/courier/login")
@pytest.mark.usefixtures("cleanup_users")
class TestCourierLogin:

    created_users = []

    @allure.title('Успешный логин курьера в системе с использованием логина и пароля.')
    @allure.description('Проверяется наличие идентификатора курьера в теле и статус код == 200.')
    def test_login_courier_login_with_login_and_password(self):
        with allure.step("Регистрация курьера и подготовка json"):
            payload = create_and_register_courier_and_return_login_password()
            payload_string = json.dumps(payload)
        with allure.step("Запись пользователя для очистки"):
            self.created_users.append(payload)

        with allure.step("Отправка POST запроса для входа курьера в систему"):
            r = requests.post(courier_login_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: в теле ответа есть идентификатор курьера"):
            assert r.json()['id'] > 0
        with allure.step(f"Проверка: статус код == 200"):
            assert r.status_code == 200

    @allure.title(f'Невозможно войти в систему, используя только пароль.')
    @allure.description(f'Проверяется: ошибка == "{not_enough_data_for_login}" и статус код == 400.')
    def test_login_courier_cannot_login_without_login(self):
        with allure.step("Регистрация курьера и подготовка json"):
            payload = create_and_register_courier_and_return_login_password()
            payload_only_login = {
                "password": payload['password']
            }
            payload_string = json.dumps(payload_only_login)
        with allure.step("Запись пользователя для очистки"):
            self.created_users.append(payload)

        with allure.step("Отправка POST запроса для входа курьера в систему"):
            r = requests.post(courier_login_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: ошибка == '{not_enough_data_for_login}'"):
            assert r.json()["message"] == not_enough_data_for_login
        with allure.step(f"Проверка: статус код == 400"):
            assert r.status_code == 400

    @allure.title('Невозможно войти в систему, используя даные несуществующего курьера.')
    @allure.description(f'Для проверки создается и удаляется курьер, под которым затем происходит попытка входа.'
                        f'Проверяется: ошибка == "{courier_not_found}" и статус код == 404.')
    def test_login_courier_non_existent_courier_cannot_login(self):
        with allure.step("Регистрация курьера и подготовка json"):
            payload = create_and_register_courier_and_return_login_password()
            payload_string = json.dumps(payload)

        with allure.step("Удаление курьера"):
            delete_courier(payload['login'], payload['password'])
        with allure.step("Отправка POST запроса для входа курьера в систему"):
            r = requests.post(courier_login_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: ошибка == '{courier_not_found}'"):
            assert r.json()['message'] == courier_not_found
        with allure.step(f"Проверка: статус код == 404"):
            assert r.status_code == 404
