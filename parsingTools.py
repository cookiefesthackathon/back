import requests, json
from pprint import pprint as pp
from bs4 import BeautifulSoup as BS
from flask import jsonify


def wildberriesHardParser(query, n):
	url = f'https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-1257786&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false'
	
	headers = {
		'accept': '*/*',
		'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'origin': 'https://www.wildberries.ru',
		'priority': 'u=1, i',
		'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=buheirb',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'cross-site',
		'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
		'x-queryid': 'qid1039998608173290817220241129192303'
	}

	resp = requests.get(url=url, headers=headers)
	#return resp.json()

	data = resp.json()

	products = []
	for item in data['data']['products'][:n]:

		product_info = {
			'article': item.get('id'),  # Артикул продукта
			'title': item.get('name'),
			'link': f"https://www.wildberries.ru/catalog/{item.get('id')}/detail.aspx",
			'price': item['sizes'][0]['price']['total'] / 100,  # Цена в копейках

			'product_rating': item.get('reviewRating'),
            'feedbacks_count': item.get('feedbacks'),  # Количество отзывов
            'product_count': item.get('totalQuantity'),  # наличие товара
            'brand_name': item.get('brand'),
            'brand_id': item.get('brandId'),

            'seller_name': item.get('supplier'),
            'seller_id': item.get('supplierId'),
			'seller_rating': item.get('supplierRating')  # Рейтинг продавца

        }
		products.append(product_info)

	# Преобразование списка словарей в JSON-строку
	json_string = json.dumps(products, indent=2, ensure_ascii=False)
	return json_string



def main():
	# Пример вызова функции
	products = wildberriesHardParser('паста splat', 10)
	print(products)



if __name__ == '__main__':
	main()