import json

import requests
import random
import string

from data.data import order_body_without_color
from global_params import courier_url, courier_login_url, orders_url, headers, order_cancel_url, order_url


def generate_new_courier_data(exclude_parameter=None):
    if exclude_parameter is None:
        exclude_parameter = []

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login = generate_random_string(15)
    password = generate_random_string(15)
    first_name = generate_random_string(15)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    if len(exclude_parameter) > 0:
        for i in exclude_parameter:
            del payload[i]

    return payload


def create_and_register_courier_and_return_login_password():
    payload = generate_new_courier_data()
    response = requests.post(courier_url, data=payload)

    if response.status_code == 201:
        payload = {
            "login": payload["login"],
            "password": payload["password"]
        }
        return payload


def courier_login(login, password):
    payload = {
        "login": login,
        "password": password
    }
    r = requests.post(courier_login_url, data=payload)
    if r.status_code == 200:
        return r.json()["id"]


def delete_courier(login, password):
    courier_id = courier_login(login, password)
    payload = {
        "id": str(courier_id)
    }
    requests.delete(f'{courier_url}/{courier_id}', data=payload)


def create_order():
    payload = order_body_without_color.copy()
    payload_string = json.dumps(payload)
    r = requests.post(orders_url, data=payload_string, headers=headers)
    return r.json()['track']


def get_order_id(track_id):
    payload = {'t': track_id}
    r = requests.get(order_url, params=payload)
    return r.json()['order']['id']


def cancel_order(track_id):
    payload = {'track': track_id}
    requests.put(order_cancel_url, params=payload)
