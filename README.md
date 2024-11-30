# backend server staff
запускать на сервере API_server.py и monitoring.py
IP хз. потом скажу


# API

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

## поиск
http://IP:5000/search/<str:query> GET

ВОЗВРАТ 200
```json
[
  {
    "article": 162731640,
    "title": "Зубная паста Ультракомплекс и Биокальций, 100мл, 2шт",
    "link": "https://www.wildberries.ru/catalog/162731640/detail.aspx",
    "price": 352.0,
    "product_rating": 4.9,
    "feedbacks_count": 323055,
    "product_count": 6845,
    "brand_name": "SPLAT",
    "brand_id": 6810,
    "seller_name": "Официальный магазин SPLAT BIOMIO",
    "seller_id": 107681,
    "seller_rating": 4.9
  },
  {
    "article": 173078066,
    "title": "Зубная паста БИОКАЛЬЦИЙ набор, уход за зубами, 2 шт",
    "link": "https://www.wildberries.ru/catalog/173078066/detail.aspx",
    "price": 336.0,
    "product_rating": 4.9,
    "feedbacks_count": 323055,
    "product_count": 15678,
    "brand_name": "SPLAT",
    "brand_id": 6810,
    "seller_name": "Официальный магазин SPLAT BIOMIO",
    "seller_id": 107681,
    "seller_rating": 4.9
  }
]
```
