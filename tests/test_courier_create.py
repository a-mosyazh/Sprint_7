import json
import allure
import pytest
import requests

from data.data import not_enough_data_for_creation, login_is_already_used, successful_ok_true_response
from global_params import courier_url, headers
from utils.helpers import generate_new_courier_data


@allure.suite("POST /api/v1/courier")
@pytest.mark.usefixtures("cleanup_users")
class TestCourierCreation:

    # Список созданных пользователей используется для их удаления после выполнения тестов
    created_users = []

    @allure.title('Успешное создание курьера с использованием всех возможных параметров.')
    @allure.description(f'Указанные параметры при выполнении: login, password, firstName. '
                        f'Проверяется: тело ответа == "{successful_ok_true_response}" и статус код == 201')
    def test_create_courier_with_login_password_first_name(self):
        with allure.step("Получение данных для создания курьера и приведение к json"):
            payload = generate_new_courier_data()
            payload_string = json.dumps(payload)
        with allure.step("Запись пользователя для очистки"):
            self.created_users.append(payload)

        with allure.step("Отправка POST запроса для создания курьера"):
            r = requests.post(courier_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: тело ответа == '{successful_ok_true_response}'"):
            assert r.text == successful_ok_true_response
        with allure.step(f"Проверка: статус код == 201"):
            assert r.status_code == 201

    @allure.title('Невозможно создать курьера с одинаковыми значениями login.')
    @allure.description(f'При выполнении теста один и тот же курьер создается дважды. '
                        f'Проверяется: ошибка == "{login_is_already_used}" и статус код == 201')
    def test_create_courier_only_unique_courier_created(self):
        with allure.step("Получение данных для создания курьера и приведение к json"):
            payload = generate_new_courier_data()
            payload_string = json.dumps(payload)
        with allure.step("Запись пользователя для очистки"):
            self.created_users.append(payload)

        with allure.step("Отправка POST запроса для создания курьера"):
            r_unique = requests.post(courier_url, data=payload_string, headers=headers)
        with allure.step("Отправка POST запроса для повторного создания того же курьера"):
            r_duplicated = requests.post(courier_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: тело ответа == '{successful_ok_true_response}' при первом создании"):
            assert r_unique.text == successful_ok_true_response
        with allure.step(f"Проверка: код ответа == 201 при первом создании"):
            assert r_unique.status_code == 201
        with allure.step(f"Проверка: ошибка == '{login_is_already_used}' при повторном создании"):
            assert r_duplicated.json()["message"] == login_is_already_used
        with allure.step(f"Проверка: код ответа == 409 при повторном создании"):
            assert r_duplicated.status_code == 409

    @allure.title('Невозможно создать курьера без пароля.')
    @allure.description(f'Указанные параметры при выполнении: login, firstName. '
                        f'Проверяется: ошибка == "{not_enough_data_for_creation}" и статус код == 400')
    def test_create_courier_courier_without_password_is_not_created(self):
        with allure.step("Получение данных для создания курьера и приведение к json"):
            payload = generate_new_courier_data(['password'])
            payload_string = json.dumps(payload)
        with allure.step("Запись пользователя для очистки"):
            self.created_users.append(payload)

        with allure.step("Отправка POST запроса для создания курьера"):
            r = requests.post(courier_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: ошибка == '{not_enough_data_for_creation}'"):
            assert r.json()["message"] == not_enough_data_for_creation
        with allure.step(f"Проверка: код ответа == 400"):
            assert r.status_code == 400

    @allure.title('Невозможно создать курьера без логина.')
    @allure.description(f'Указанные параметры при выполнении: password, firstName. '
                        f'Проверяется: ошибка == "{not_enough_data_for_creation}" и статус код == 400')
    def test_create_courier_courier_without_login_is_not_created(self):
        with allure.step("Получение данных для создания курьера и приведение к json"):
            payload = generate_new_courier_data(['login'])
            payload_string = json.dumps(payload)
        with allure.step("Запись пользователя для очистки"):
            self.created_users.append(payload)

        with allure.step("Отправка POST запроса для создания курьера"):
            r = requests.post(courier_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: ошибка == '{not_enough_data_for_creation}'"):
            assert r.json()["message"] == not_enough_data_for_creation
        with allure.step(f"Проверка: код ответа == 400"):
            assert r.status_code == 400

    @allure.title('Успешное создание пользователя без необязательного параметра firstName.')
    @allure.description(f'Указанные параметры при выполнении: login, password. '
                        f'Проверяется: тело ответа == "{successful_ok_true_response}" и статус код == 201')
    def test_create_courier_courier_without_first_name_is_created(self):
        with allure.step("Получение данных для создания курьера и приведение к json"):
            payload = generate_new_courier_data(['firstName'])
            payload_string = json.dumps(payload)
        with allure.step("Запись пользователя для очистки"):
            self.created_users.append(payload)

        with allure.step("Отправка POST запроса для создания курьера"):
            r = requests.post(courier_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: тело ответа == '{successful_ok_true_response}'"):
            assert r.text == successful_ok_true_response
        with allure.step(f"Проверка: статус код == 201"):
            assert r.status_code == 201
