import pytest
import requests
import allure

from data.data import TestData
from curl.url import TestEndpoint
from helpers.helper import generate_random_string, generate_password



class TestLogin:
     
    @allure.title('Успешная авторизация зарегистрированного пользователя')
    def test_authorization_true_user_success(self, login):

        with allure.step(' Проверка кода ответа, флага success, наличия accessToken, наличия refreshToken'):
            assert (login.status_code == TestData.LOGIN_OK["code"] and 
                login.json()["success"] and
                len(login.json()["accessToken"]) > 0 and
                len(login.json()["refreshToken"]) > 0)
        
    
    @allure.title('Вход с несуществующим email')
    def test_authorization_user_with_fake_email(self, new_user):

        # Генерируем несуществующий email
        fake_email = f"{generate_random_string(8)}@google.com"      #совпадений не будет, длинна разная, домен разный

        auth_data = new_user

        payload = {
            "email": fake_email,
            "password":auth_data[1]
        }

        with allure.step('Отправляем запрос на авторизацию пользователя'):
            response = requests.post(TestEndpoint.LOGIN, json = payload)

        with allure.step('Проверка статус-кода ошибки, флага success и сообщения об ошибке'):
            assert (response.status_code == TestData.LOGIN_INVALID["code"] and 
                response.json()["success"] == False and
                response.json()["message"] == TestData.LOGIN_INVALID["message"])


    @allure.title('Вход с несуществующим паролем')
    def test_authorization_user_with_fake_password(self, new_user):
        fake_password = generate_password(10)                       #совпадений не будет, длинна разная
        
        auth_data = new_user

        payload = {
            "email": auth_data[0],
            "password": fake_password
        }

        with allure.step('Отправляем запрос на авторизацию пользователя'):
            response = requests.post(TestEndpoint.LOGIN, json=payload)
        
        with allure.step('Проверка статус-кода ошибки, флага success и сообщения об ошибке'):
            assert (response.status_code == TestData.LOGIN_INVALID["code"] and 
                response.json()["success"] == False and
                response.json()["message"] == TestData.LOGIN_INVALID["message"])