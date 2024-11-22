# School Homework Management System

Веб-приложение для управления домашними заданиями в школе.

## Функции

- Управление домашними заданиями
- Управление классами и предметами
- Простая система аутентификации
- Адаптивный дизайн

## Технологии

- Python 3.12
- Flask 2.3.2
- SQLite
- Bootstrap
- HTML/CSS

## Установка

1. Клонируйте репозиторий:
```bash
git clone [URL вашего репозитория]
cd windsurf-project
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env:
```bash
echo "SECRET_KEY=your-secret-key-here" > .env
```

5. Запустите приложение:
```bash
python app.py
```

## Использование

1. Откройте браузер и перейдите по адресу `http://localhost:5000`
2. Войдите в систему, используя пароль: `sysyc`
3. Используйте панель администратора для управления заданиями, классами и предметами

## Развертывание

Для продакшн-развертывания рекомендуется использовать WSGI-сервер, например Gunicorn:

```bash
pip install gunicorn
gunicorn app:app
```

## Лицензия

MIT
