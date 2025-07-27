import pytest
import requests
import allure

from data.data import TestData
from curl.url import TestEndpoint
from helpers.helper import generate_random_string, generate_password



class TestLogin:
     
    @allure.title('Успешная авторизация зарегистрированного пользователя')
    def test_authorization_true_user_success(self, new_user):

        # Получаем email и пароль зарегистрированного пользователя
        email, password = new_user

         # Тело запроса
        payload = {
            "email": email,
            "password": password
        }

        with allure.step('Отправляем запрос на авторизацию пользователя'):
            response = requests.post(TestEndpoint.LOGIN, json=payload)

        with allure.step(' Проверка кода ответа, флага success, наличия accessToken, наличия refreshToken'):
            assert (response.status_code == TestData.LOGIN_OK["code"] and 
                response.json()["success"] and
                len(response.json()["accessToken"]) > 0 and
                len(response.json()["refreshToken"]) > 0)
        
    


    @pytest.mark.parametrize("field, value, description", [
        ("email", f"{generate_random_string(8)}@google.com", "несуществующий email"),
        ("password", generate_password(10), "несуществующий пароль")])

    @allure.title("Вход с некорректными данными: {description}")
    def test_authorization_with_invalid_credentials(self, new_user, field, value, description):
        email, password = new_user

        # Формируем тело запроса в зависимости от параметра
        payload = {
            "email": email if field != "email" else value,
            "password": password if field != "password" else value
        }

        with allure.step(f'Отправляем запрос на авторизацию с {description}'):
            response = requests.post(TestEndpoint.LOGIN, json=payload)

        with allure.step('Проверка статус-кода ошибки, флага success и сообщения об ошибке'):
            assert response.status_code == TestData.LOGIN_INVALID["code"], \
                f"Ожидался статус {TestData.LOGIN_INVALID['code']}, получен {response.status_code}"
            assert response.json()["success"] is False, "Ожидался success=False"
            assert response.json()["message"] == TestData.LOGIN_INVALID["message"], \
                f"Ожидалось сообщение: {TestData.LOGIN_INVALID['message']}"




