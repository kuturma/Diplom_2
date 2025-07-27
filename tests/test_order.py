import requests
import allure
import random

from data.data import TestData
from curl.url import TestEndpoint

class TestOrder:

    @allure.title('Успешное создание заказа, код 200, авторизованным пользователем, с существующими ингредиентами')
    def test_create_order_with_authorized_user_and_true_ingredient(self, token, list_ingredient):

        selected_ingredients = random.sample(list_ingredient, k=3)
        payload = {"ingredients": selected_ingredients}


        with allure.step('Запрос: заказ с существующими ингридиентами'):
            response = requests.post(TestEndpoint.ORDER, json = payload, headers={"Authorization": token[0]})


        assert (response.status_code == TestData.ORDER_OK["code"] and 
                response.json()["success"] and
                len(response.json()["name"]) > 0 and 
                response.json()["order"]["number"] > 0)     
        

    @allure.title('Ошибка, код 302 при заказе без авторизации пользователя, с существующими ингредиентами')
    def test_create_order_without_authorized_user_and_true_ingredient_shows_error(self, list_ingredient):
        
        selected_ingredients = random.sample(list_ingredient, k=3)
        payload = {"ingredients": selected_ingredients}

        with allure.step('Запрос: заказ с существующими ингридиентами, без авторизации'):
            response = requests.post(TestEndpoint.ORDER, json=payload)

        assert (response.status_code == TestData.ORDER_WITHOUT_AUTH["code"] and
                response.headers["location"] == TestData.ORDER_WITHOUT_AUTH["location"])
        

    @allure.title('Ошибка, код 500, при заказе с авторизованным пользователем, с несуществующими ингредиентами')
    def test_create_order_with_authorized_user_and_fake_ingredient_shows_error(self, token):

        payload = {
            "ingredients": ["675br20fbb","80naty374yzg2" , "312dmjr1nfn3875"]
        }

        with allure.step('Запрос: заказ с несушествующими ингридиентами'):
            response = requests.post(TestEndpoint.ORDER, json=payload, headers={"Authorization": token[0]})

        assert response.status_code == TestData.ORDER_INVALID_INGR["code"]


    @allure.title('Ошибка 400 при заказе с авторизованным пользователем при отсутствии ингредиентов')
    def test_create_order_with_authorized_user_and_without_ingredient_shows_error(self, token):

        payload = {
            "ingredients": []
        }

        with allure.step('Запрос: заказ где ингридиенты отсутствуют'):
            response = requests.post(TestEndpoint.ORDER, json=payload, headers={"Authorization": token[0]})

        assert (response.status_code == TestData.ORDER_WITHOUT_INGR["code"] and 
                response.json()["success"] == False and
                response.json()["message"] == TestData.ORDER_WITHOUT_INGR["message"])
