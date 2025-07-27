import random
import string


#Генерирует строку из 12 символов 
def generate_random_string(length=12, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for i in range(length))


#Генерирует пароль из 12 символов
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return generate_random_string(length, chars)


#Генерирует данные пользователя:
def generate_user_data():
    return {
        "email": f"{generate_random_string()}@yandex.ru",
        "password": generate_password(),
        "name": generate_random_string()
    }

