import allure
import pytest
import requests

from data.data import TestData
from curl.url import TestEndpoint
from helpers.helper import generate_user_data

class TestRegisterUser:

    @allure.title('Успешная регистрация нового пользователя')
    def test_register_new_user_all_valid_data_success(self):

        payload = generate_user_data()

        with allure.step('Запрос: регистрация нового пользователя'):
            response = requests.post(TestEndpoint.REGISTER, json=payload)

        assert (response.status_code == TestData.REGISTER_OK["code"] and response.json()["success"] and
                len(response.json()["accessToken"]) > 0 and
                len(response.json()["refreshToken"]) > 0)
        

    @allure.title('Проверка регистрации существующего пользователя')
    def test_register_duplicate_user_shows_error(self):

        payload = generate_user_data()

        with allure.step('Запрос: регистрация нового пользователя'):
            requests.post(TestEndpoint.REGISTER, json=payload)

        with allure.step('Запрос: регистрация нового пользователя (дубликат пользователя)'):
            response = requests.post(TestEndpoint.REGISTER, json=payload)

        assert (response.status_code == TestData.REGISTER_DUPLICATE["code"] and response.json()['success']  == False and
                response.json()['message'] == TestData.REGISTER_DUPLICATE["message"])
    

    @allure.title('Проверка создания пользователя при отправке неполного тела запроса')
    @pytest.mark.parametrize('payload', [
        TestData.register_data_miss_email, TestData.register_data_miss_password, TestData.register_data_miss_name])
    def test_add_user_not_valid_data(self, payload):

        with allure.step('Запрос: регистрация пользователя, тело запроса не полное'):
            response = requests.post(TestEndpoint.REGISTER, json=payload)

        assert (response.status_code == TestData.REGISTER_INVALID["code"] and 
                response.json()['success']  == False and
                response.json()['message'] == TestData.REGISTER_INVALID["message"])