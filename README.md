#  Bookmark service - сервис для хранения ссылок (закладок)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Описание проекта

Проект выгружен на сервер. Документация доступна по ссылке: http://194.76.46.5/swagger

Различные эндпоинты: http://194.76.46.5/api/

Настроен троттлинг со следующими параметрами:

```shell
"user": "200/hour",
"anon": "100/hour",
```

После регистрации в сервисе пользователь может создавать различные коллекции в которые будет добавлять свои закладки.
Одна и та же закладка может быть в одной или нескольких коллекциях сразу. Либо быть без коллекции. Для закладок подгружается информация из og и meta HTML-тегов предоставленной страницы.

## Особенности

- Пользователь может регистрироваться, получать токен (`login`) для API и удалять его (`logout`).
- Пользователь может создавать персональные `коллекции` закладок, а также изменять и удалять их.
- Пользователь может добавлять `закладку`, указывая ссылку на страницу и коллекции, в которые необходимо добавить ссылку.
- В фоне `Celery Worker` зайдет на указанную ссылку и получит необходимые OG и meta данные.
- Если на странице есть `OG image`, то данное изображение будет выгружено и сохранено локально.
- Пользователь может добавлять и удалять закладки в коллекции.

### Используемый стек

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![DRF][DRF-badge]][DRF-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Nginx][Nginx-badge]][Nginx-url]
[![Docker][Docker-badge]][Docker-url]
[![Redis][Redis-badge]][Redis-url]
[![Celery][Celery-badge]][Celery-url]
[![Poetry][Poetry-badge]][Poetry-url]

### Автор проекта

Илья Малашенко (github: melax08, telegram: @ScreamOFF)

### Системные требования

- Python 3.11+;
- Docker (19.03.0+) c docker compose;

### Архитектура проекта

| Директория              | Описание                               |
|-------------------------|----------------------------------------|
| `infra`                 | Docker-compose файл, конфиг Nginx      |
| `src/backend`           | Django приложение                      |
| `src/backend/bookmarks` | Основное приложение Django             |
| `src/backend/api`       | Django REST Framework API              |
| `src/backend/users`     | Приложение для работы с пользователями |
| `src/backend/core`      | Дополнительные сущности проекта        |

## Установка и эксплуатация

### Установка проекта через Docker

1. Клонируем репозиторий с проектом и переходим в его директорию:

```shell
git clone https://github.com/melax08/bookmarks_service.git && cd bookmarks_service
```

2. Копируем файл `.env.example` с новыми названием `.env` и заполняем его необходимыми данными:

```shell
cp .env.example .env && nano .env
```

3. Переходим в каталог с инфраструктурой:

```shell
cd infra
```

4. В файле `nginx.conf` указываем домен или IP (или и то и другое) для вашего сайта в параметре `server_name`.

5. Запускаем `docker compose` (должен быть предварительно установлен на сервере):

```shell
docker-compose up -d
```

или

```shell
docker compose up -d
```

<details><summary>Создание суперпользователя</summary>

<br>

Если вы хотите создать `суперпользователя Django` в запущенном проекте, используйте команду:

```shell
docker compose exec bookmarks_backend python manage.py createsuperuser
```

Команду необходимо использовать в каталоге `infra`.

</details>

### Примеры использования

Сразу после запуска, API документация проекта со всеми эндпоинтами будет доступна по ссылке: http://127.0.0.1/swagger/

Вместо 127.0.0.1 - нужно подставить домен или IP-адрес вашего сайта.

### Информация для разработчиков

1. Для локальной разработки проекта необходимо установить `Poetry`, [инструкция в официальной документации](https://python-poetry.org/docs/#installation).

2. Установку зависимостей проекта локально можно осуществить с помощью команды:

```shell
poetry install
```

3. Для автоматического применения `black`, `isort`, `flake8` и других хуков при использовании `git commit`, необходимо активировать `pre-commit`:

```shell
pre-commit install
```

### Что еще не было реализовано

<details><summary>Посмотреть</summary>

<br>

- Админка не поддерживает функционал API, такой, как фоновая подрузка информации по закладке, а также, обновление времени изменения закладки/коллекции. Решил это этот функционал на уровне админки может быть избыточным.
- Пагинация, без конкретной технической задачи решил не реализовывать никакую.
- Более оптимальный способ выгрузки информации о странице.
- У основных эндпоинтов в документации не описаны примеры ответов при кодах ответов отличных от 200 и 201.

</details>


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/
[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white
[Django-url]: https://github.com/django/django
[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white
[DRF-url]: https://github.com/encode/django-rest-framework
[DRF-badge]: https://img.shields.io/badge/DRF-a30000?style=for-the-badge
[Postgres-url]: https://www.postgresql.org/
[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white
[Nginx-url]: https://nginx.org
[Nginx-badge]: https://img.shields.io/badge/nginx-009900?style=for-the-badge&logo=nginx&logoColor=white
[Docker-url]: https://www.docker.com
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Redis-badge]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
[Celery-badge]: https://img.shields.io/badge/Celery-37814A.svg?style=for-the-badge&logo=Celery&logoColor=white
[Celery-url]: https://docs.celeryq.dev/en/stable/
[Poetry-url]: https://python-poetry.org
[Poetry-badge]: https://img.shields.io/badge/poetry-blue?style=for-the-badge&logo=Poetry&logoColor=white&link=https%3A%2F%2Fpython-poetry.org
