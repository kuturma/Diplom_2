
from helpers.helper import generate_user_data



class TestData:

    LOGIN_OK = {                                                            #При успешной авторизации
        "code": 200
    }
    LOGIN_INVALID = {                                                       #Если логин или пароль неверные или нет одного из полей, вернётся код ответа 401 Unauthorized
        "code": 401,
        "message": "email or password are incorrect"
    }

    ORDER_OK = {                                                            #При успешном заказе
        "code": 200
    }
    ORDER_WITHOUT_AUTH = {                                                  #При заказе без авторизации
        "code": 302,
        "location": "/login"
    }
    ORDER_INVALID_INGR = {                                                  #Если в запросе передан невалидный хеш ингредиента, вернётся код ответа 500 Internal Server Error
        "code": 500
    }
    ORDER_WITHOUT_INGR = {                                                  #Если не передать ни один ингредиент, вернётся код ответа 400 Bad Request
        "code": 400,
        "message": "Ingredient ids must be provided"
    }

    REGISTER_OK = {                                                         #При успешной регистрации
        "code": 200
    }
    REGISTER_DUPLICATE = {                                                  #Если пользователь существует, вернётся код ответа 403 Forbidden
        "code": 403,
        "message": "User already exists"
    }
    REGISTER_INVALID = {                                                    #Если нет одного из полей, вернётся код ответа 403 Forbidden
        "code": 403,
        "message": "Email, password and name are required fields"
    }


    # Данные для неполных запросов на основе сгенерированных данных
    user_data = generate_user_data()
    # Нет почты
    register_data_miss_email = {
        "password": user_data["password"],
        "name": user_data["name"]
    }
    # Нет пароля
    register_data_miss_password = {
        "email": user_data["email"],
        "name": user_data["name"]
    }
    # Нет имени
    register_data_miss_name = {
        "email": user_data["email"],
        "password": user_data["password"]
    }


