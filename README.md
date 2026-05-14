## Эндпоинты

### Аутентификация

- `POST /users/login/` - получить пару `access` и `refresh`
- `POST /users/token/refresh/` - получить новый `access` по `refresh`
- `POST /users/logout/` - добавить `refresh` в blacklist

Используется JWT-аутентификация `djangorestframework-simplejwt`.

- `access` + `refresh` token
- Для logout используется blacklist refresh-токенов через `rest_framework_simplejwt.token_blacklist`.

### login

`POST /users/login/` выдает пару токенов: `access` и `refresh`.

Пример запроса:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Пример ответа:

```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

### logout

Logout работает с `refresh token` (не требует валидного `access token`)

Запрос `POST /users/logout/: body: refresh token` > валидация `RefreshToken(refresh)` > `token.blacklist()`


Пример запроса:

```
{
  "refresh": "<refresh_token>"
}
```

### Пользователи

- `POST /users/register/` - регистрация пользователя
- `GET /users/list/` - список пользователей
- `GET /users/<pk>/detail/` - получить пользователя
- `PUT/PATCH /users/<pk>/update/` - обновить пользователя
- `DELETE /users/<pk>/delete/` - деактивировать пользователя

## Примечания

- Для работы blacklist должны быть применены миграции: `python manage.py migrate`
- После logout повторное использование того же `refresh` token вернет ошибку валидации
- Защищенные эндпоинты по умолчанию требуют JWT в заголовке `Authorization: Bearer <access_token>`

