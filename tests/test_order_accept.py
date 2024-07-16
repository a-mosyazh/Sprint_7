import allure
import pytest
import requests

from data.data import (successful_ok_true_response, courier_does_not_exist, not_enough_data_for_search,
                       order_is_in_progress)
from global_params import order_accept_url
from utils.helpers import (create_and_register_courier_and_return_login_password, courier_login, create_order,
                           get_order_id)


@allure.suite("PUT /api/v1/orders/accept/:id")
@pytest.mark.usefixtures("cleanup_users", "setup_deleted_order_and_courier")
class TestOrderAccept:

    cancelled_order_id = None
    deleted_courier_id = None
    # Список созданных пользователей используется для их удаления после выполнения тестов
    created_users = []

    @allure.title(f'Успешное принятие заказа.')
    @allure.description(f'Проверяется: тело == "{successful_ok_true_response}" и статус код == 200.')
    def test_order_accept_successful_acceptance(self):
        with allure.step("Получение идентификатора курьера"):
            courier = create_and_register_courier_and_return_login_password()
            self.created_users.append(courier)
            courier_id = int(courier_login(courier['login'], courier['password']))
            payload = {'courierId': courier_id}
        with allure.step("Получение идентификатора заказа"):
            order_track = int(create_order())
            order_id = get_order_id(order_track)

        with allure.step("Отправка PUT запроса для принятия заказа"):
            r = requests.put(f'{order_accept_url}/{order_id}', params=payload)

        with allure.step(f"Проверка: тело ответа == '{successful_ok_true_response}'"):
            assert r.text == successful_ok_true_response
        with allure.step(f"Проверка: статус код == 200"):
            assert r.status_code == 200

    @allure.title(f'Заказ не принимается, если курьер не найден.')
    @allure.description(f'Проверяется: тело == "{courier_does_not_exist}" и статус код == 404.')
    def test_order_accept_courier_not_found_order_not_accepted(self):
        with allure.step("Установка query параметра с идентификатором удаленного курьера"):
            payload = {'courierId': self.deleted_courier_id}
        with allure.step("Получение идентификатора заказа"):
            order_track = int(create_order())
            order_id = get_order_id(order_track)

        with allure.step("Отправка PUT запроса для принятия заказа"):
            r = requests.put(f'{order_accept_url}/{order_id}', params=payload)

        with allure.step(f"Проверка: ошибка == '{courier_does_not_exist}'"):
            assert r.json()['message'] == courier_does_not_exist
        with allure.step(f"Проверка: код ответа == 404"):
            assert r.status_code == 404

    @allure.title(f'Заказ не принимается, если заказ не найден.')
    @allure.description(f'Проверяется: тело == "{order_is_in_progress}" и статус код == 409.')
    def test_order_accept_order_not_found_order_not_accepted(self):
        with allure.step("Получение идентификатора курьера"):
            courier = create_and_register_courier_and_return_login_password()
            self.created_users.append(courier)
            courier_id = int(courier_login(courier['login'], courier['password']))
            payload = {'courierId': courier_id}

        with allure.step("Отправка PUT запроса для принятия заказа"):
            r = requests.put(f'{order_accept_url}/{self.cancelled_order_id}', params=payload)

        with allure.step(f"Проверка: ошибка == '{order_is_in_progress}'"):
            assert r.json()['message'] == order_is_in_progress
        with allure.step(f"Проверка: код ответа == 409"):
            assert r.status_code == 409

    @allure.title(f'Заказ не принимается, если курьер не указан.')
    @allure.description(f'Проверяется: тело == "{not_enough_data_for_search}" и статус код == 400.')
    def test_order_accept_courier_not_specified_order_not_accepted(self):
        with allure.step("Получение идентификатора заказа"):
            order_track = int(create_order())

        with allure.step("Отправка PUT запроса для принятия заказа"):
            r = requests.put(f'{order_accept_url}/{order_track}')

        with allure.step(f"Проверка: ошибка == '{not_enough_data_for_search}'"):
            assert r.json()['message'] == not_enough_data_for_search
        with allure.step(f"Проверка: код ответа == 400"):
            assert r.status_code == 400
