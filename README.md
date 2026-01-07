````md
# 🛍 ENF — Интернет-магазин одежды
**Django 5.2 + PostgreSQL 16 + Docker (Dev/Prod) + HTMX + Alpine.js**

ENF — интернет-магазин одежды на Django с современным фронтенд-подходом (HTMX + Alpine.js), PostgreSQL и полностью предсказуемой инфраструктурой запуска в Docker. Проект поддерживает отдельные окружения разработки и продакшена через раздельные настройки `settings/base.py`, `settings/dev.py`, `settings/prod.py` и отдельные env-файлы `.env.dev` / `.env.prod`.

---

## 🌟 Особенности проекта

- **Современный стек**: Django 5.2 + HTMX + Alpine.js
- **База данных**: PostgreSQL 16
- **Docker-контейнеризация** (dev и prod)
- **Раздельные окружения**: `dev` / `prod` через `DJANGO_SETTINGS_MODULE`
- **Кастомная модель пользователя**: `AUTH_USER_MODEL = 'users.CustomUser'`
- **Платёжные системы**:
  - Stripe
  - Heleket (крипто)
- **Безопасность в prod**:
  - CSRF и secure cookies
  - Security headers
  - HSTS (при HTTPS)
  - Ограниченные `ALLOWED_HOSTS`
- **Dev без сюрпризов**: никаких `Secure` cookies и HTTPS-ограничений в разработке

---

## 🧱 Структура проекта (после изменений)

Рекомендуемая структура файлов и настроек:

```text
enf/
├── enf/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── docker/
│   └── nginx/
│       └── nginx.conf
│
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Dockerfile
├── .env.dev
├── .env.prod
├── manage.py
├── requirements.txt
└── README.md
````

> В этой схеме файл `enf/settings.py` больше не используется. Настройки берутся из пакета `enf/settings/` через переменную `DJANGO_SETTINGS_MODULE`.

---

## ✅ Предварительные требования

* Docker Engine (актуальная версия)
* Docker Compose v2
* Git

Проверка:

```bash
docker --version
docker compose version
git --version
```

---

## 🚀 Быстрый старт (Docker DEV — рекомендуется)

### 1) Подготовьте `.env.dev`

Создайте файл `.env.dev` в корне проекта:

```ini
DJANGO_SETTINGS_MODULE=enf.settings.dev
DEBUG=True

SECRET_KEY=dev-secret-key

POSTGRES_DB=enfdb
POSTGRES_USER=enfdb
POSTGRES_PASSWORD=enfdb
POSTGRES_HOST=db
POSTGRES_PORT=5432

STRIPE_SECRET_KEY=example
STRIPE_WEBHOOK_SECRET=example

HELEKET_API_KEY=example
HELEKET_SECRET_KEY=example
```

> В dev используется `POSTGRES_HOST=db`, потому что Django и PostgreSQL находятся в одной docker-сети.

---

### 2) Соберите и запустите dev-окружение

```bash
docker compose -f docker-compose.dev.yml up --build
```

Оставьте этот терминал работать (будут логи).

---

### 3) Примените миграции

Во втором терминале:

```bash
docker compose -f docker-compose.dev.yml exec web python manage.py migrate
```

---

### 4) Создайте суперпользователя

```bash
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

---

### 5) Откройте проект в браузере

* Сайт: [http://localhost:8000](http://localhost:8000)
* Админка: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🧪 Работа с проектом (Docker DEV)

### Основные команды

```bash
# Запуск dev
docker compose -f docker-compose.dev.yml up

# Запуск dev в фоне
docker compose -f docker-compose.dev.yml up -d

# Остановка
docker compose -f docker-compose.dev.yml down

# Остановка с удалением volume (полный сброс БД)
docker compose -f docker-compose.dev.yml down -v

# Логи web
docker compose -f docker-compose.dev.yml logs -f web

# Логи db
docker compose -f docker-compose.dev.yml logs -f db
```

### Django команды внутри контейнера

```bash
# Проверка конфигурации
docker compose -f docker-compose.dev.yml exec web python manage.py check

# Django shell
docker compose -f docker-compose.dev.yml exec web python manage.py shell

# Создание миграций
docker compose -f docker-compose.dev.yml exec web python manage.py makemigrations

# Применение миграций
docker compose -f docker-compose.dev.yml exec web python manage.py migrate
```

---

## 🧩 Локальный запуск БЕЗ Docker (опционально)

> Этот режим возможен, но **не рекомендуется**, так как ломает идею единообразной среды.
> Если всё же нужно: в этом режиме Docker DNS (`db`) не работает, значит `POSTGRES_HOST` должен быть `127.0.0.1` или `localhost`.

### Вариант A: полностью локальная БД (PostgreSQL установлен на машине)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=enf.settings.dev
export POSTGRES_HOST=127.0.0.1

python manage.py migrate
python manage.py runserver
```

### Вариант B: Postgres в Docker, Django локально (нежелательно)

Нужно пробросить порт у `db`:

```yaml
ports:
  - "5432:5432"
```

И затем в `.env` для локального запуска:

```ini
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

---

## ⚙️ Настройки Django (Dev/Prod)

### Принцип

* **`settings/base.py`** — общие настройки проекта
* **`settings/dev.py`** — dev-конфигурация (HTTP, без Secure cookies, разрешённые хосты шире)
* **`settings/prod.py`** — prod-конфигурация (HTTPS, Secure cookies, HSTS, строгие хосты)

Выбор окружения выполняется через переменную:

```ini
DJANGO_SETTINGS_MODULE=enf.settings.dev
# или
DJANGO_SETTINGS_MODULE=enf.settings.prod
```

---

## 🧷 Файлы окружения

### `.env.dev` (разработка)

Ключевые принципы:

* `DEBUG=True`
* HTTP
* безопасные флаги cookie выключены
* `ALLOWED_HOSTS` максимально либеральный (обычно `['*']`)

Пример:

```ini
DJANGO_SETTINGS_MODULE=enf.settings.dev
DEBUG=True
SECRET_KEY=dev-secret-key

POSTGRES_DB=enfdb
POSTGRES_USER=enfdb
POSTGRES_PASSWORD=enfdb
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### `.env.prod` (продакшен)

Ключевые принципы:

* `DEBUG=False`
* HTTPS
* secure cookies включены
* `ALLOWED_HOSTS` — домены проекта
* сертификаты обслуживаются Nginx

Пример:

```ini
DJANGO_SETTINGS_MODULE=enf.settings.prod
DEBUG=False
SECRET_KEY=super-secret-prod-key

POSTGRES_DB=enfdb
POSTGRES_USER=enfdb
POSTGRES_PASSWORD=strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## 🐳 Docker: рекомендованные compose-файлы

### `docker-compose.dev.yml` (рекомендуемый dev)

* `web` запускается через `runserver` для быстрой разработки
* `db` — PostgreSQL
* том для postgres сохраняет данные между перезапусками

Пример логики:

* `web` зависит от `db` по healthcheck
* приложение доступно на `http://localhost:8000`

---

### `docker-compose.prod.yml` (prod-контур)

Prod обычно включает:

* `web` (gunicorn)
* `db`
* `nginx` (TLS, статика, прокси)

После старта в prod обязательно:

* `migrate`
* `collectstatic`

---

## 🔒 Безопасность (важно понимать различия)

### Dev

* **HTTP**
* **без `Secure` cookies**
* **без HSTS**
* минимальные ограничения (удобство разработки)

### Prod

* **HTTPS**
* `CSRF_COOKIE_SECURE=True`
* `SESSION_COOKIE_SECURE=True`
* `SECURE_HSTS_SECONDS=31536000` (+ includeSubDomains/preload при необходимости)
* `ALLOWED_HOSTS` строго ограничен доменами
* `CSRF_TRUSTED_ORIGINS` содержит `https://...`

---

## 🧾 Nginx + SSL (prod)

В продакшене Nginx выполняет:

* TLS termination (сертификаты Let’s Encrypt/другие)
* проксирование запросов на `web`
* раздачу `static/` и `media/`

Если используешь Let’s Encrypt (пример):

```bash
sudo certbot --nginx -d domen.com -d www.domen.com
```

> В dev Nginx обычно не нужен.

---

## 🧹 Сброс базы (dev)

Если требуется полностью пересоздать PostgreSQL (например, после изменений в архитектуре или env):

```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up --build
docker compose -f docker-compose.dev.yml build --no-cache
docker compose -f docker-compose.dev.yml exec web python manage.py migrate
```
```bash
# ОБЯЗАТЕЛЬНАЯ пересборка (правильно)
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml build --no-cache
docker compose -f docker-compose.dev.yml up -d

# Контрольная проверка (после сборки)
docker exec -it enf-web-1 python manage.py shell
# Пример:
from PIL import features
features.check("webp")
features.check("avif")
```
---

## ✅ Чек-лист запуска «без сюрпризов»

### Docker-dev

1. Убедитесь, что вы используете `.env.dev` и `DJANGO_SETTINGS_MODULE=enf.settings.dev`
2. Запуск:

   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```
3. Миграции:

   ```bash
   docker compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```
4. Суперпользователь:

   ```bash
   docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   ```
5. Проверка:

   ```bash
   docker compose -f docker-compose.dev.yml exec web python manage.py check
   ```
6. Открыть:

   * [http://localhost:8000](http://localhost:8000)
   * [http://localhost:8000/admin](http://localhost:8000/admin)

### Типовые ошибки и их причины

* **`could not translate host name "db"`**
  Django запущен **не в Docker**, а `POSTGRES_HOST=db` относится к Docker DNS.
* **Не работает login/CSRF в dev**
  Включены `CSRF_COOKIE_SECURE=True` / `SESSION_COOKIE_SECURE=True` при работе по HTTP.
* **404 на статику в prod**
  Не сделан `collectstatic` или неверно смонтированы volumes в Nginx.

---

## 🧭 Инструкции по деплою

Внешний гайд (репозиторий):
`https://github.com/s6ptember/for-deploy-guide.git`

---

## 📝 Примечания

* В одном проекте не рекомендуется параллельно держать MySQL/MariaDB и PostgreSQL без необходимости.
* Для PostgreSQL рекомендуется использовать отдельный volume под данные и не смешивать его с другими проектами.
* В dev лучше избегать Nginx и Gunicorn (они нужны в prod).

---

## 📄 Лицензия

Уточняется владельцем проекта.
Проект для личного и коммерческого использования.
Ответственность за платежные интеграции и данные клиентов несёт владелец проекта.
Если вы скачали этот проект, вы стали его владельцем.

```


