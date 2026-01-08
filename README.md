# 📦 Order Management API
## Система управления заказами с кастомной JWT RBAC

![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![Django](https://img.shields.io/badge/Django-5.0-green?style=flat-square)
![Auth](https://img.shields.io/badge/Custom-JWT%20RBAC-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 Описание проекта

Fullstack-решение для управления заказами с **кастомной системой аутентификации** и **динамическим распределением прав доступа (RBAC)**.

Главный акцент на **безопасности** и **архитектурной чистоте**. Вместо использования готовых библиотек (SimpleJWT), реализован собственный механизм обработки JWT-токенов через Middleware, обеспечивающий полный контроль над авторизацией.

---

## ⚡ Ключевые особенности

### 🔐 Кастомная архитектура безопасности

- **JWT Middleware** — собственный слой (`core/middleware.py`) для перехвата и валидации Bearer-токенов
- **Dynamic RBAC** — права доступа хранятся в БД, система проверяет Роль → Ресурс → HTTP-метод
- **DRF Адаптер** — кастомный класс аутентификации, интегрирующий Middleware с Django REST Framework

### 🚀 Bonus-функционал

| Функция | Описание |
|---------|---------|
| **Swagger UI** | Автоматическая генерация интерактивной документации API (drf-spectacular) |
| **Frontend SPA** | Панель управления на чистом JavaScript + Bootstrap 5 |
| **Автотесты** | Интеграционные тесты (APITestCase) с полным циклом |
| **Seed Script** | Автоматическое наполнение БД начальными данными |

---

## 🛠 Технический стек

```
Backend:
├── Python 3.11
├── Django 5.0
├── Django REST Framework 3.14
├── PyJWT (токены)
└── Bcrypt (хеширование)

Frontend:
├── HTML5
├── Bootstrap 5
└── Fetch API

Database:
└── SQLite (легко мигрируется на PostgreSQL)

Documentation:
└── OpenAPI 3.0 (Swagger)
```

---

## 🚀 Быстрый старт

### 1️⃣ Клонирование и установка

```bash
# Клонируем репозиторий
git clone <YOUR_GITHUB_LINK>
cd em_tt_jan26

# Создаем виртуальное окружение
python -m venv venv

# Активируем окружение
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 2️⃣ Инициализация базы данных

```bash
# Используем кастомную команду для заполнения БД
python manage.py seed_db
```

Команда `seed_db` автоматически:
- Применяет миграции
- Создает роли (Admin, User, Manager)
- Создает ресурсы и разрешения
- Создает тестового администратора

### 3️⃣ Запуск сервера

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: **http://localhost:8000**

---

## 📚 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|---------|
| `POST` | `/api/auth/register/` | Регистрация пользователя |
| `POST` | `/api/auth/login/` | Вход и получение JWT токена |
| `GET` | `/api/orders/` | Список заказов (с проверкой прав) |
| `POST` | `/api/orders/` | Создание заказа |
| `GET` | `/api/orders/{id}/` | Детали заказа |
| `PUT` | `/api/orders/{id}/` | Обновление заказа |
| `DELETE` | `/api/orders/{id}/` | Удаление заказа |

### Интерактивная документация

Доступна по адресу: **http://localhost:8000/api/docs/**

---

## 🧪 Тестирование

```bash
# Запуск всех тестов
python manage.py test

# Запуск с verbose выводом
python manage.py test --verbosity=2
```

**Покрытие тестами:**
- ✅ Регистрация пользователей
- ✅ Аутентификация и JWT токены
- ✅ RBAC проверки доступа
- ✅ CRUD операции с заказами
- ✅ Обработка ошибок и валидация

---

## 📂 Структура проекта

```
em_tt_jan26/
├── core/
│   ├── middleware.py          # JWT Middleware
│   ├── authentication.py       # DRF адаптер аутентификации
│   └── permissions.py         # RBAC проверки
├── api/
│   ├── serializers.py         # DRF сериализаторы
│   ├── views.py               # API views
│   ├── urls.py                # Роутинг
│   └── models.py              # Django модели
├── templates/
│   ├── index.html             # Frontend SPA
│   └── static/
│       ├── css/               # Bootstrap, кастомные стили
│       └── js/                # Fetch API клиент
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔑 Примеры использования

### Регистрация

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!",
    "email": "john@example.com"
  }'
```

### Вход и получение токена

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "user"
  }
}
```

### Создание заказа (с авторизацией)

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -d '{
    "title": "Заказ #1",
    "description": "Описание заказа",
    "status": "pending"
  }'
```

---

## 🔐 Система разрешений (RBAC)

### Роли и права доступа

| Роль | GET | POST | PUT | DELETE |
|------|-----|------|-----|--------|
| **Admin** | ✅ | ✅ | ✅ | ✅ |
| **Manager** | ✅ | ✅ | ✅ | ❌ |
| **User** | ✅ | ✅ | ❌ | ❌ |
| **Guest** | ❌ | ❌ | ❌ | ❌ |

Все разрешения хранятся в таблице `permissions` и проверяются динамически.

---

## 🛡️ Безопасность

- ✅ JWT токены с подписью HS256
- ✅ Bcrypt хеширование паролей
- ✅ CORS защита
- ✅ Валидация входных данных
- ✅ SQL injection защита (ORM Django)
- ✅ XSS защита (Content Security Policy)
- ✅ RBAC проверки на каждый endpoint

---

## 📝 Переменные окружения

Создайте файл `.env` в корне проекта:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
JWT_SECRET=your-jwt-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 🤝 Развертывание на Production

### Подготовка к production

```bash
# Собираем static файлы
python manage.py collectstatic --noinput

# Запускаем тесты
python manage.py test

# Используем gunicorn
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Docker (опционально)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```
=======
**Alexander Trofimov**  
Full-stack Python Developer  
[GitHub](https://github.com/trofimovby) | [LinkedIn](https://linkedin.com/in/trofimovby)
>>>>>>> 1564ca651ee301f05df44b73b080088e5fbe577a

---

## 📞 Контакты 

- **GitHub:** [trofimovby/em_tt_jan26](https://github.com/trofimovby)

---


