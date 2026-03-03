# Нагрузочное тестирование на Locust

Проект для нагрузочного тестирования веб-сайтов с использованием Python и Locust.

Я создала этот проект, чтобы показать навыки нагрузочного тестирования. Здесь есть генерация тестовых данных, разные сценарии поведения пользователей и анализ результатов.

## Технологии
Python, Locust, Faker, CSV, Git/GitHub

## Структура проекта
locust-website-tests/
  data/ - тестовые данные (CSV файлы)
  reports/ - отчеты о тестировании
  utils/data_generator.py - генератор данных
  locustfile.py - сценарии тестирования
  requirements.txt - зависимости
  README.md - описание проекта

## Как запустить

Скачать проект:
git clone https://github.com/79264528166m-cell/locust-website-tests.git
cd locust-website-tests

Создать и активировать виртуальное окружение:
python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Mac/Linux)

Установить зависимости:
pip install -r requirements.txt

Сгенерировать тестовые данные:
python utils/data_generator.py

Запустить тест:
locust -f locustfile.py

Открыть браузер: http://localhost:8089
Ввести: Users 10, Spawn rate 2, Host https://jsonplaceholder.typicode.com
Нажать Start swarming

## Сценарии
Главная страница (часто)
Поиск товаров (часто)
Категории (средне)
Карточка товара (средне)
Корзина (редко)
Авторизация (редко)

## Результаты
В отчете смотреть: Fails = 0 (нет ошибок), 95% < 500 ms (быстрый ответ), RPS стабилен
