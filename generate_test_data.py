from faker import Faker
import json
import random

# Создаем генератор
fake = Faker('ru_RU')

def generate_users(count=10):
    """Генерирует указанное количество пользователей"""
    users = []
    for _ in range(count):
        user = {
            "id": _ + 1,
            "username": fake.user_name(),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            "registration_date": fake.date_time_this_year().isoformat()
        }
        users.append(user)
    return users

def generate_products(count=20):
    """Генерирует указанное количество товаров"""
    categories = ['electronics', 'clothing', 'books', 'home', 'sports']
    products = []
    
    for _ in range(count):
        product = {
            "id": _ + 1,
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=200),
            "price": round(random.uniform(10, 1000), 2),
            "category": random.choice(categories),
            "in_stock": random.choice([True, False]),
            "rating": round(random.uniform(3, 5), 1)
        }
        products.append(product)
    return products

# Пример использования
if __name__ == "__main__":
    # Генерируем тестовые данные
    users = generate_users(5)
    products = generate_products(10)
    
    # Сохраняем в файлы
    with open('test_users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    
    with open('test_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print("✅ Тестовые данные созданы:")
    print(f"   - Пользователи: {len(users)}")
    print(f"   - Товары: {len(products)}")
    
    # Выводим пример сгенерированных данных
    print("\n📊 Пример пользователя:")
    print(json.dumps(users[0], ensure_ascii=False, indent=2))