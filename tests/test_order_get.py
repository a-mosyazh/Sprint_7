import allure
import requests

from data.data import not_enough_data_for_search, order_not_found
from global_params import order_url
from utils.helpers import create_order, cancel_order


@allure.suite("GET /api/v1/orders/track")
class TestOrderGet:

    @allure.title(f'Успешное получение заказа по track_id.')
    @allure.description(f'Проверяется: в теле имеется запрашиваемый track_id и статус код == 200.')
    def test_get_order_successful(self):
        with allure.step("Получение track_id заказа"):
            order_track = int(create_order())
            payload = {'t': order_track}

        with allure.step("Отправка GET запроса для получения заказа"):
            r = requests.get(order_url, params=payload)

        with allure.step(f"Проверка: в теле ответа есть track id из query параметра"):
            assert r.json()['order']['track'] == order_track
        with allure.step(f"Проверка: статус код == 200"):
            assert r.status_code == 200

    @allure.title(f'Невозможно получить заказ, не указав track_id.')
    @allure.description(f'Проверяется: ошибка == "{not_enough_data_for_search}" и статус код == 400.')
    def test_get_order_no_track_id_in_query_params_order_not_found(self):
        with allure.step("Отправка GET запроса для получения заказа"):
            r = requests.get(order_url)

        with allure.step(f"Проверка: ошибка == '{not_enough_data_for_search}'"):
            assert r.json()['message'] == not_enough_data_for_search
        with allure.step(f"Проверка: код ответа == 400"):
            assert r.status_code == 400

    @allure.title(f'Невозможно получить несуществующий заказ.')
    @allure.description(f'В тесте создается и удаляется заказ. Затем по этому заказу запрашивается информация. '
                        f'Проверяется: ошибка == "{order_not_found}" и статус код == 404.')
    def test_get_order_track_id_does_not_exist_order_not_found(self):
        with allure.step("Получение track_id заказа"):
            track_id = create_order()
        with allure.step("Отмена заказа и подготовка query параметра"):
            cancel_order(track_id)
            payload = {'t': track_id}

        with allure.step("Отправка GET запроса для получения заказа"):
            r = requests.get(order_url, params=payload)

        with allure.step(f"Проверка: ошибка == '{order_not_found}'"):
            assert r.json()['message'] == order_not_found
        with allure.step(f"Проверка: код ответа == 404"):
            assert r.status_code == 404
