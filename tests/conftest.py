import pytest
import requests

from curl.url import TestEndpoint
from helpers.helper import generate_user_data


# Регистрирует нового пользователя и возвращает список из email и пароля
@pytest.fixture
def new_user():

    # создаём список, чтобы метод мог его вернуть
    auth_data = []

    # собираем тело запроса
    payload = generate_user_data()

    # получаем email и password из сгенерированных данных
    email = payload["email"]
    password = payload["password"]

    # отправляем запрос на регистрацию пользователя и сохраняем ответ в переменную response
    response = requests.post(TestEndpoint.REGISTER, json=payload)

    # если регистрация прошла успешно (код ответа 200), добавляем в список email и пароль пользователя
    if response.status_code == 200:
        auth_data.append(email)
        auth_data.append(password)

    # возвращаем список
    return auth_data


# Логинит зарегистрированного пользователя
@pytest.fixture()
def login(new_user):

    # собираем тело запроса
    payload = {
        "email": new_user[0],
        "password": new_user[1]
    }

    # отправляем запрос на авторизацию пользователя и сохраняем ответ в переменную response
    response = requests.post(TestEndpoint.LOGIN, json=payload)

    # возвращаем список
    return response


# Возвращает список токенов авторизированного пользователя
@pytest.fixture()
def token(login):
    # создаём список, чтобы метод мог его вернуть
    tokens = []

    # если авторизация прошла успешно (код ответа 200), добавляем в список accessToken и refreshToken
    if login.status_code == 200:
        tokens.append(login.json()["accessToken"])
        tokens.append(login.json()["refreshToken"])

    return tokens


# Возвращает список _id всех доступных ингредиентов
@pytest.fixture
def list_ingredient():
    response = requests.get(TestEndpoint.INGREDIENTS)
    json_response = response.json()
    return [ingredient["_id"] for ingredient in json_response["data"]]