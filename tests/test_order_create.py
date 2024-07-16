import json
import allure
import pytest
import requests

from data.data import order_body_without_color
from global_params import headers, orders_url


@allure.suite("POST /api/v1/orders")
class TestOrderCreation:

    @allure.title(f'Успешное создание заказа с указанием всех параметров и комбинациями значений параметра "color".')
    @allure.description(f'Проверяется: в теле имеется track и статус код == 201.')
    @pytest.mark.parametrize("color",
                             [
                                 ["BLACK"],
                                 ["BLACK", "GREY"],
                                 ["GREY"],
                                 []
                             ])
    def test_create_order_successful_creation(self, color):
        with allure.step("Формирование тела запроса и приведение к json"):
            payload = order_body_without_color.copy()
            payload['color'] = color
            payload_string = json.dumps(payload)

        with allure.step("Отправка POST запроса для создания заказа"):
            r = requests.post(orders_url, data=payload_string, headers=headers)

        with allure.step(f"Проверка: в теле ответа есть track id"):
            assert r.json()['track'] > 0
        with allure.step(f"Проверка: статус код == 201"):
            assert r.status_code == 201

    @allure.title(f'Успешное создание заказа без указания цвета в "color".')
    @allure.description(f'Проверяется: в теле имеется track и статус код == 201.')
    def test_create_order_successful_creation_without_color(self):
        with allure.step("Формирование тела запроса и приведение к json"):
            payload_string_1 = json.dumps(order_body_without_color)

        with allure.step("Отправка POST запроса для создания заказа"):
            r = requests.post(orders_url, data=payload_string_1, headers=headers)

        with allure.step(f"Проверка: в теле ответа есть track id"):
            assert r.json()['track'] > 0
        with allure.step(f"Проверка: статус код == 201"):
            assert r.status_code == 201
