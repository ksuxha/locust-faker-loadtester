from locust import HttpUser, task, between
from faker import Faker
import random
import json

# Создаем генератор фейковых данных на русском языке
fake = Faker('ru_RU')

class WebsiteUser(HttpUser):
    """
    Класс, представляющий виртуального пользователя.
    Каждый пользователь будет выполнять задачи с случайными интервалами.
    """
    
    # Время ожидания между задачами (от 1 до 5 секунд)
    wait_time = between(1, 5)
    
    # Базовый URL тестируемого API (используем бесплатное тестовое API)
    host = "https://fakestoreapi.com"
    
    def on_start(self):
        """
        Метод вызывается при запуске каждого пользователя.
        Здесь можно выполнить подготовительные действия.
        """
        # Генерируем данные для нового пользователя
        self.username = fake.user_name()
        self.email = fake.email()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        
        print(f"👤 Новый пользователь: {self.username} ({self.email})")
    
    @task(3)
    def get_all_products(self):
        """
        Задача: получить все товары (выполняется часто)
        Вес задачи 3 - будет выполняться в 3 раза чаще, чем задачи с весом 1
        """
        with self.client.get("/products", catch_response=True, name="Получить все товары") as response:
            if response.status_code == 200:
                response.success()
                products = response.json()
                print(f"✅ Получено товаров: {len(products)}")
            else:
                response.failure(f"Ошибка: {response.status_code}")
    
    @task(2)
    def get_single_product(self):
        """
        Задача: получить один случайный товар
        """
        # Выбираем случайный ID товара (в API есть товары с ID 1-20)
        product_id = random.randint(1, 20)
        
        with self.client.get(f"/products/{product_id}", catch_response=True, name="Получить товар по ID") as response:
            if response.status_code == 200:
                response.success()
                product = response.json()
                print(f"✅ Товар #{product_id}: {product['title']}")
            else:
                response.failure(f"Товар #{product_id} не найден")
    
    @task(1)
    def get_products_by_category(self):
        """
        Задача: получить товары по категории
        """
        categories = ['electronics', 'jewelery', "men's clothing", "women's clothing"]
        category = random.choice(categories)
        
        with self.client.get(f"/products/category/{category}", catch_response=True, name="Товары по категории") as response:
            if response.status_code == 200:
                response.success()
                products = response.json()
                print(f"✅ Категория '{category}': {len(products)} товаров")
            else:
                response.failure(f"Ошибка категории: {response.status_code}")
    
    @task(1)
    def add_to_cart(self):
        """
        Задача: добавить товар в корзину
        Используем Faker для генерации данных корзины
        """
        # Генерируем данные для корзины с помощью Faker
        cart_data = {
            "userId": random.randint(1, 10),
            "date": fake.date_time_this_month().isoformat(),
            "products": [
                {
                    "productId": random.randint(1, 20),
                    "quantity": random.randint(1, 5)
                }
            ]
        }
        
        # Отправляем POST запрос
        with self.client.post("/carts", 
                            json=cart_data, 
                            catch_response=True, 
                            name="Добавить в корзину") as response:
            if response.status_code == 200:
                response.success()
                print(f"✅ Товар добавлен в корзину (количество: {cart_data['products'][0]['quantity']})")
            else:
                response.failure(f"Ошибка добавления: {response.status_code}")
    
    @task(1)
    def create_user(self):
        """
        Задача: создать нового пользователя
        Используем Faker для генерации всех данных пользователя
        """
        # Генерируем данные пользователя с помощью Faker
        user_data = {
            "email": fake.email(),
            "username": fake.user_name(),
            "password": fake.password(),
            "name": {
                "firstname": fake.first_name(),
                "lastname": fake.last_name()
            },
            "address": {
                "city": fake.city_name(),
                "street": fake.street_name(),
                "number": random.randint(1, 999),
                "zipcode": fake.postcode(),
                "geolocation": {
                    "lat": str(fake.latitude()),
                    "long": str(fake.longitude())
                }
            },
            "phone": fake.phone_number()
        }
        
        # Отправляем POST запрос на создание пользователя
        with self.client.post("/users", 
                            json=user_data, 
                            catch_response=True, 
                            name="Создать пользователя") as response:
            if response.status_code == 200:
                response.success()
                print(f"✅ Создан пользователь: {user_data['username']}")
            else:
                response.failure(f"Ошибка создания: {response.status_code}")
    
    @task(1)
    def create_order(self):
        """
        Задача: создать заказ
        Генерируем реалистичные данные заказа с помощью Faker
        """
        # Генерируем данные заказа
        order_data = {
            "userId": random.randint(1, 10),
            "date": fake.date_time_this_month().isoformat(),
            "products": [
                {
                    "productId": random.randint(1, 20),
                    "quantity": random.randint(1, 3)
                } for _ in range(random.randint(1, 5))  # От 1 до 5 товаров в заказе
            ]
        }
        
        # Отправляем POST запрос на создание заказа
        with self.client.post("/carts",  # В этом API заказы тоже через /carts
                            json=order_data, 
                            catch_response=True, 
                            name="Создать заказ") as response:
            if response.status_code == 200:
                response.success()
                items_count = len(order_data['products'])
                print(f"✅ Создан заказ с {items_count} товарами")
            else:
                response.failure(f"Ошибка заказа: {response.status_code}")
    
    def on_stop(self):
        """
        Метод вызывается при остановке пользователя
        """
        print(f"👋 Пользователь {self.username} завершил работу")