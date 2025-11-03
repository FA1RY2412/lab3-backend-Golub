
# Лабораторна робота 3 — Валідація, обробка помилок, ORM
**Технології серверного ПЗ** — Група 3205, *Голуб Денис*

## Визначення варіанту
Обчислення: `3205 % 3 = 2` → **Варіант 2 — Користувацькі категорії витрат**.

### Суть варіанту
- Є **загальні категорії** (видно всім) і **користувацькі** (видно лише власнику).
- Користувач може створювати власні категорії.
- При створенні витрати можна використовувати власну категорію або будь-яку загальну.

---

## Стек
- Flask + flask-smorest (валидація/документація OpenAPI)
- Marshmallow (схеми та валідація)
- SQLAlchemy + Flask-Migrate (ORM + міграції)
- PostgreSQL (Docker)

## Запуск
1. Підніміть базу:
   ```bash
   docker-compose up -d db
   ```
2. Створіть `.env` на основі `.env.example` (за бажанням відредагуйте змінні).
3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
4. Ініціалізація БД (один раз на проєкт):
   ```bash
   export FLASK_APP=app.main:app
   flask db init
   flask db migrate -m "init"
   flask db upgrade
   ```
   > Під час `flask db` команди застосунок читає `DATABASE_URL` з `.env`/env.
5. Запустіть API:
   ```bash
   flask run
   ```
   або
   ```bash
   python -m app.main
   ```

Веб-документація (Swagger UI): **http://localhost:5000/docs**

## Модель даних
- `User(id, username)` — створюється автоматично при першому запиті з header `X-User-Id`.
- `Category(id, name, is_global, user_id?)` — глобальні/користувацькі.
- `Expense(id, amount, description?, user_id, category_id?)`

## Політика доступу (спрощено для лаби)
- `X-User-Id` — обов'язковий заголовок у всіх запитах.
- Категорії:
  - `GET /api/categories` — повертає глобальні + категорії поточного користувача.
  - `POST /api/categories` — створює **лише користувацьку** категорію (is_global ігнорується).
  - `DELETE /api/categories/{id}` — можна видалити **лише власну** категорію; глобальні видаляти заборонено.
- Витрати:
  - `GET /api/expenses` — витрати поточного користувача.
  - `POST /api/expenses` — створення (можна вказати `category_id`, якщо це глобальна або своя).
  - `GET /api/expenses/{id}`, `PATCH`, `DELETE` — тільки з власними витратами.

## Приклади запитів (Postman / cURL)
```bash
curl -H "X-User-Id: 1" http://localhost:5000/api/categories
curl -H "X-User-Id: 1" -X POST http://localhost:5000/api/categories -H "Content-Type: application/json" -d '{"name": "Їжа"}'

curl -H "X-User-Id: 1" -X POST http://localhost:5000/api/expenses -H "Content-Type: application/json" -d '{"amount":"120.50","description":"кава та булочка"}'
```

## Postman
- Колекція: `postman_collection.json`
  - Працює з `{{baseUrl}}` (за замовчуванням http://localhost:5000) та заголовком `X-User-Id`.
- Додайте середовище `local.postman_environment.json` та встановіть `userId`.

## Git Flow
- Рекомендовано створити тег:  
  ```bash
  git tag v2.0.0 -a -m "Lab 2"
  git push --tags
  ```
  (з методички; для ЛР3 теж релевантно для відстеження версій)

## Оцінювання (чекліст)
- [x] Валідація та обробка помилок (flask-smorest, marshmallow)
- [x] ORM + робота з БД (SQLAlchemy + PostgreSQL)
- [x] Додаткове завдання (користувацькі категорії витрат)
- [x] Postman колекція + environment
- [x] README з визначенням варіанту
