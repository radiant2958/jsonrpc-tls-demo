# JSON-RPC Демонстрационный Клиент

## Установка и настройка

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/radiant2958/jsonrpc-demo.git
   cd jsonrpc-demo
   ```
2. Создайте виртуальное окружение
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости
   ```sh
   pip install django
   ```
4. Запустите сервер разработки:

   ```sh
   python manage.py runserver
   ```
5. Откройте приложение в браузере: http://127.0.0.1:8000/


Тестирование
Для запуска юнит-тестов выполните команду
   ```sh
   python manage.py test
   ```
