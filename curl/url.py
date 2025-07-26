class TestEndpoint:

    MAIN_URL = "https://stellarburgers.nomoreparties.site/api"

    REGISTER = f"{MAIN_URL}/auth/register"    #Создание пользователя
    LOGIN = f"{MAIN_URL}/auth/login"          #Авторизация
    ORDER = f"{MAIN_URL}/orders"              #Создание заказа
    LOGOUT = f"{MAIN_URL}/auth/logout"        #Выход из системы
    INGREDIENTS = f"{MAIN_URL}/ingredients"   #Получение данных об ингредиентах