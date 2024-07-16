import pytest

from utils.helpers import delete_courier, create_order, cancel_order, \
    create_and_register_courier_and_return_login_password, courier_login, get_order_id


# Фикстура для удаления созданных в ходе тестов пользователей
@pytest.fixture(scope='class')
def cleanup_users(request):
    def delete_users():
        for user in request.cls.created_users:
            if user.get('login') is True and user.get('password') is True:
                delete_courier(user['login'], user['password'])

    request.addfinalizer(delete_users)


# Фикстура для получения идентификаторов заказа и курьера, которые были удалены
@pytest.fixture(scope='class')
def setup_deleted_order_and_courier(request):
    # Получение и запись в переменную класса идентификатора заказа, который будет удален
    track_id = create_order()
    order_id = get_order_id(track_id)
    request.cls.cancelled_order_id = order_id
    cancel_order(track_id)
    # Получение и запись в переменную класса идентификатора курьера, который будет удален
    payload = create_and_register_courier_and_return_login_password()
    courier_id = courier_login(payload['login'], payload['password'])
    request.cls.deleted_courier_id = courier_id
    delete_courier(payload['login'], payload['password'])
