# backend server staff
запускать на сервере API_server.py и monitoring.py

IP хз. потом скажу

## создать пользователя
http://IP:5000/users POST

RAW JSON
```json
{
    "mail": "fdfdf@example.com",
    "password": "securepassword123",
    "name": "Иван",
    "surname": "Иванов",
    "patname": "Иванович"
}
```
ВОЗВРАТ 201
```json
{
    "message": "User created successfully!"
}
```


## залогиниться
http://IP:5000/auh GET

RAW JSON

ЗАПРОС
```json
{
    "mail": "fdfdf@example.com",
    "password": "securepassword123"
}
```

ВОЗВРАТ 200
```json
{
    "ok": true
}
```
ИЛИ 200
```json
{
    "ok": false
}
```

## удалить из избранного
http://IP:5000/favorites DELETE

ЗАПРОС
```json
{
    "id": "34342341"
}
```
ВОЗВРАТ 204
```json
{
    "message": "success"
}
```
ИЛИ 404
```json
{
    "message": "not found favorite '34342341'"
}
```

