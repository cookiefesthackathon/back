# backend server staff
запускать на сервере API_server.py и monitoring.py
IP хз. потом скажу

# API 

## Поиск
http://IP:5000/search?query="шторы" GET

параметры:
    query - текст запроса

ВОЗВРАТ 200
```json
[
  {
    "article": 156631671,
    "title": "Шторы портьеры Блэкаут комплект 150х250 (2 шт.)",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_du_pCtFa4XrjZEdE02sn9NstrQOFlU0OhSGGSv_1c1nh31pP_qaHaKLyvg&s",
    "link": "https://www.wildberries.ru/catalog/156631671/detail.aspx",
    "price": 1383.0,
    "bad_price": 9473.0,
    "product_rating": 4.8,
    "feedbacks_count": 41227,
    "product_count": 3525,
    "brand_name": "ВОЛНЫ ШТОР",
    "brand_id": 310820117,
    "seller_name": "ВОЛНЫ ШТОР",
    "seller_id": 213308,
    "seller_rating": 4.8
  },
  {
    "article": 197824382,
    "title": "Портьеры шторы блэкаут комплект 150*250 (2 шт.) светло-серые",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3Z-449zMP-y0U-dLvxNwOWSA4fzeX9D1DNnkoz3t95Yix06W-XwyvLFg9JQ&s",
    "link": "https://www.wildberries.ru/catalog/197824382/detail.aspx",
    "price": 1405.0,
    "bad_price": 9171.0,
    "product_rating": 4.8,
    "feedbacks_count": 10870,
    "product_count": 834,
    "brand_name": "Линии и Тени",
    "brand_id": 310963043,
    "seller_name": "Линии и Тени",
    "seller_id": 1383112,
    "seller_rating": 4.8
  }
]
```
ИЛИ 400
```json
{
    "ok": "False"
}
```

## sort поиск
http://IP:5000/sortsearch?query=Шторы&filter=price&reverse=false GET
(всё без кавычек)

параметры:
    query - текст запроса
    reverse - сортировать ли в обратном направлении?
    filter - любое поле (в кавычках) по которому будет происходить сортировка 
(article, title, img, link, price, bad_price, product_rating, feedbacks_count, product_count, brand_name, brand_id, seller_name, seller_id, seller_rating)

ВОЗВРАТ 200
```json
[
    {
        "article": 199203129,
        "title": "Шторы Мрамор двухцветные с прихватами",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSY8xKxPWDvLlKi09OPLkl76TId8qJ46BSiKug9ARSNknNbBIXOECA-kRnLwy8&s",
        "link": "https://www.wildberries.ru/catalog/199203129/detail.aspx",
        "price": 2721.0,
        "bad_price": 12000.0,
        "product_rating": 4.9,
        "feedbacks_count": 1183,
        "product_count": 176,
        "brand_name": "Твой декор",
        "brand_id": 70434,
        "seller_name": "Твой декор",
        "seller_id": 48879,
        "seller_rating": 4.8
    },
    {
        "article": 112539874,
        "title": "Шторы бархат 150 на 260 в гостиную и спальню",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxBOUXTnZ1I7tHEM1cKcyUZD28e0oTzVoJPGnX5dkPCGUUbcd54FAH7h_obgM&s",
        "link": "https://www.wildberries.ru/catalog/112539874/detail.aspx",
        "price": 1681.0,
        "bad_price": 5358.0,
        "product_rating": 4.7,
        "feedbacks_count": 15753,
        "product_count": 828,
        "brand_name": "Mesmer",
        "brand_id": 59770,
        "seller_name": "Mesmer",
        "seller_id": 329104,
        "seller_rating": 4.8
    },
    {
        "article": 207210490,
        "title": "Комплект штор Мрамор 400х250 см",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXQ0nEuW8W3zwxlyyqo7vWicBTstDSOAkg-oxr-jmTyQYHU1NVCPr8bS6f0A&s",
        "link": "https://www.wildberries.ru/catalog/207210490/detail.aspx",
        "price": 1576.0,
        "bad_price": 8000.0,
        "product_rating": 4.6,
        "feedbacks_count": 176,
        "product_count": 38,
        "brand_name": "Вальгрин Home",
        "brand_id": 311639987,
        "seller_name": "ИП \"Выговская Анна Леонидовна\"",
        "seller_id": 139533,
        "seller_rating": 4.8
    },
    {
        "article": 159787876,
        "title": "Шторы портьеры блэкаут 150х250 комплект (2шт.)",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDm0Bc7aXb-XIN44HQ0Ps2zWJvjdV3cFopAmbAdFXzuZUSt2v5IZBF0Gvy4gQ&s",
        "link": "https://www.wildberries.ru/catalog/159787876/detail.aspx",
        "price": 1451.0,
        "bad_price": 9945.0,
        "product_rating": 4.8,
        "feedbacks_count": 41227,
        "product_count": 1347,
        "brand_name": "ВОЛНЫ ШТОР",
        "brand_id": 310820117,
        "seller_name": "ВОЛНЫ ШТОР",
        "seller_id": 213308,
        "seller_rating": 4.8
    }
]
```
ИЛИ 400
```json
{
    "ok": "False"
}
```

## создать пользователя
http://IP:5000/users POST
ЗаПАРОС
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
    "ok": true,
    "id": "185826"
}
```
ИЛИ 400
```json
{
    "ok": false
}
```



## залогиниться
http://IP:5000/auh?password=securepassword123&mail=fdfdf@example.com GET

ВОЗВРАТ 200
```json
{
    "ok": true,
    "usr_id": 3131323
}
```
ИЛИ 200
```json
{
    "ok": false,
    "usr_id": 3131323
}
```

## добавить в избранное
http://IP:5000/favorites?user_id=250261&artic=173077624 POST

ВОЗВРАТ
```json
{
    "data": "518505",
    "ok": true
}
```

## взять избранное пользователя
http://IP:5000/favorites?user_id=250261

ВОЗВРАТ
```json
[
    {
        "article": "95666887", 
        "title": "Зубная паста отбеливающая PROFI WHITE 100 'RDA'", 
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7Js63GUjj4u8SA1tEWFwDCatg_-2PyDAGPxH-ZFjBnt3ygkyDQyd3aph97lw&s",
        "link": "https://www.wildberries.ru/catalog/95666887/detail.aspx", 
        "price": 328.0, 
        "bad_price": 716.0, 
        "product_rating": 4.8, 
        "feedbacks_count": 3541,
        "product_count": 2174, 
        "brand_name": "PRESIDENT", 
        "brand_id": 6574,
        "seller_name": "PRESIDENT", 
        "seller_id": 940884, 
        "seller_rating": 4.9
    },
    {
        "article": 207210490,
        "title": "Комплект штор Мрамор 400х250 см",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXQ0nEuW8W3zwxlyyqo7vWicBTstDSOAkg-oxr-jmTyQYHU1NVCPr8bS6f0A&s",
        "link": "https://www.wildberries.ru/catalog/207210490/detail.aspx",
        "price": 1576.0,
        "bad_price": 8000.0,
        "product_rating": 4.6,
        "feedbacks_count": 176,
        "product_count": 38,
        "brand_name": "Вальгрин Home",
        "brand_id": 311639987,
        "seller_name": "ИП \"Выговская Анна Леонидовна\"",
        "seller_id": 139533,
        "seller_rating": 4.8
    },
]
```

## удалить из избранного
http://IP:5000/favorites?user_id=250261&artic=109832438 DELETE

ВОЗВРАТ 204
```json
{
    "ok": true
}
```
ИЛИ 500
```json
{
    "ok": false
}
```

## карточка по артикулу
http://127.0.0.1:5000/product?artic=207210490 GET
ВОЗВРАТ 200
```json
{
    "article": 207210490,
    "title": "Комплект штор Мрамор 400х250 см",
    "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXQ0nEuW8W3zwxlyyqo7vWicBTstDSOAkg-oxr-jmTyQYHU1NVCPr8bS6f0A&s",
    "link": "https://www.wildberries.ru/catalog/207210490/detail.aspx",
    "price": 1576.0,
    "bad_price": 8000.0,
    "product_rating": 4.6,
    "feedbacks_count": 176,
    "product_count": 38,
    "brand_name": "Вальгрин Home",
    "brand_id": 311639987,
    "seller_name": "ИП \"Выговская Анна Леонидовна\"",
    "seller_id": 139533,
    "seller_rating": 4.8
}
```




