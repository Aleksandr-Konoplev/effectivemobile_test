## Установка

1. Загрузить репозитарий `git clone https://github.com/Aleksandr-Konoplev/effectivemobile_test.git`
2. Установить зависимости `pip install -r requirements.txt`
3. Создать файл `.env` в корневой директории из `.env.example`
4. Создать базу данных в соответствии с настройками подключения
5. Применить миграции `python manage.py migrate`
6. Создать базовые роли и права доступа `python mansge.py seed_rbac`
7. Создать суперпользователя `python manage.py csu`

---

## Эндпоинты

**Все доступные эндпоинты с примерами запросов можно посмотреть на 
http://127.0.0.1:8000/swager/ и http://127.0.0.1:8000/redoc/**

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
- `PATCH /users/<pk>/update/` - обновить пользователя
- `DELETE /users/<pk>/delete/` - деактивировать пользователя

### Продукты 

- `POST /products/create/` - создание продукта
- `GET /products/list/` - список продуктов
- `GET /products/<pk>/detail/` - детали продукта
- `PATCH /products/<pk>/update` - изменение продукта
- `DELETE /products/<pk>/delete` - удаление продукта

---

## Роли и права доступа

- Роли: `admin`, `manager`, `user`, `guest` (хранятся в БД).
- Права: `resource.action.scope` (пример: `product.delete.own`).
- Матрица доступа:
  - `admin` - полный доступ (`read/create/update/delete.any`)
  - `manager` - все, кроме удаления (`read/create/update.any`)
  - `user` - просмотр всех, создание, изменение/удаление только своих (`read.any`, `create.any`, `update.own`, `delete.own`)
  - `guest` - только просмотр (`read.any`)
- Для инициализации базовых ролей и прав: `python manage.py seed_rbac`.