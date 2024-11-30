import requests, json
from pprint import pprint as pp
from bs4 import BeautifulSoup as BS
from flask import jsonify

class parser(object):
	"""docstring for parser"""
	def __init__(self, url):
		self.url = url

		r = requests.get(self.url)
		self.html = BS(r.text, 'html.parser')

	def find(self, *class_list):

		res = self.html
		for i in class_list:
			res = res.find(class_=i)

		text = res.text    if res else res
		return text


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


def wildberriesPageParser(url):
	headers = {
		'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
		'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'priority': 'u=1, i',
		'referer': 'https://www.wildberries.ru/',
		'sec-fetch-dest': 'image',
		'sec-fetch-mode': 'no-cors',
		'sec-fetch-site': 'cross-site',
		'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'
	}

	response = requests.get(url=url, headers=headers)
	return response.json()
	'''
	# Проверяем успешность запроса
	if response.status_code == 200:
		data = response.json()
		
		# Извлекаем необходимые данные из JSON
		product_info = {
			'article': data.get('id'),
			'title': data.get('name'),
			'link': url,
			'price': data['sizes'][0]['price']['total'] / 100 if data['sizes'] else None,
			'product_rating': data.get('reviewRating'),
			'feedbacks_count': data.get('feedbacks'),
			'product_count': data.get('totalQuantity'),
			'brand_name': data.get('brand'),
			'brand_id': data.get('brandId'),
			'seller_name': data.get('supplier'),
			'seller_id': data.get('supplierId'),
			'seller_rating': data.get('supplierRating')
		}
		
		# Преобразуем данные в JSON-строку для удобного отображения
		json_string = json.dumps(product_info, indent=2, ensure_ascii=False)
		return json_string
	else:
		return f"Ошибка: Не удалось получить данные с сайта. Код ошибки: {response.status_code}"
	'''

def main2():
	prs = parser('https://www.wildberries.ru/catalog/173077624/detail.aspx')
	
	status = prs.find('', 'mix-block__photo-zoom photo-zoom','photo-zoom__img-plug img-plug', 'photo-zoom__img-plug img-plug', 'zoom-image-container','photo-zoom__preview j-image-canvas')
	status.strip()

	print(status)


def main1():
	# Пример использования
	url = "https://www.wildberries.ru/catalog/173077624/detail.aspx"
	product_data = wildberriesPageParser(url)
	print(product_data)


def main():
	# Пример вызова функции
	products = wildberriesHardParser('паста splat', 10)
	print(products)



if __name__ == '__main__':
	main2()