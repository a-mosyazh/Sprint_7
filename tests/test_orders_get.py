import allure
import requests

from global_params import orders_url


@allure.suite("GET /api/v1/orders")
class TestOrdersGet:

    @allure.title(f'Успешное получение списка заказов без указания query параметров.')
    @allure.description(f'Проверяется: в теле ответа имеются заказы (длина "orders") и статус код == 200.')
    def test_get_orders_successful(self):
        with allure.step("Отправка GET запроса для получения списка заказов"):
            r = requests.get(orders_url)

        with allure.step(f"Проверка: в теле ответа имеются заказы"):
            assert len(r.json()['orders']) > 0
        with allure.step(f"Проверка: статус код == 200"):
            assert r.status_code == 200
