## Установка

1. Загрузить репозитарий `git clone https://github.com/Aleksandr-Konoplev/effectivemobile_test.git`
2. Установить зависимости `pip install -r requirements.txt`
3. Создать файл `.env` в корневой директории из `.env.example`
4. Создать базу данных
5. Применить миграции `python manage.py migrate`
6. Создать базовые роли и права доступа `python mansge.py seed_rbac`
5. Создать суперпользователя `python manage.py csu`

## Эндпоинты

### Аутентификация

- `POST /users/login/` - получить пару `access` и `refresh`
- `POST /users/token/refresh/` - получить новый `access` по `refresh`
- `POST /users/logout/` - добавить `refresh` в blacklist

Используется JWT-аутентификация `djangorestframework-simplejwt`.

- `access` + `refresh` token
- Для logout используется blacklist refresh-токенов через `rest_framework_simplejwt.token_blacklist`.


### Пользователи

- `POST /users/register/` - регистрация пользователя
- `GET /users/list/` - список пользователей
- `GET /users/<pk>/detail/` - получить пользователя
- `PUT/PATCH /users/<pk>/update/` - обновить пользователя
- `DELETE /users/<pk>/delete/` - деактивировать пользователя

## Роли и права доступа
