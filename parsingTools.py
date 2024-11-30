import requests, json
from bs4 import BeautifulSoup as BS
from flask import jsonify
from pprint import pprint as pp

# картинка по артикулу
def wildberriesImgParser(article_number):
	query = f"site:wildberries.ru type:image артикул {article_number}"
	# Создаем URL для поиска
	search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
	
	# Заголовки для обхода защиты Google от ботов
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
	}
	
	# Выполняем запрос
	response = requests.get(search_url, headers=headers)
	
	# Парсим HTML с помощью BeautifulSoup
	soup = BS(response.text, 'html.parser')
	
	# Находим все теги <img>
	images = soup.find_all('img')
	
	# Возвращаем ссылку на первое изображение
	if images:
		return images[1]['src']
		#return [i['src'] for i in images]
	else:
		return None

# поисковый парсер
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
	data = resp.json()
	
	#return data

	products = []
	for item in data['data']['products'][:n]:
		artic = item.get('id')

		product_info = {
			'article': artic,  # Артикул продукта
			'title': item.get('name'),
			'img': wildberriesImgParser(artic),
			'link': f"https://www.wildberries.ru/catalog/{item.get('id')}/detail.aspx",
			'price': item['sizes'][0]['price']['total'] / 100,  # Цена в копейках
			'bad_price': item['sizes'][0]['price']['basic'] / 100,  # Цена в копейках

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
	return json.dumps(products, indent=2, ensure_ascii=False)

# одна страница
def wildberriesPageParser(artic):
	img = wildberriesImgParser(artic)
	link = f"https://www.wildberries.ru/catalog/{artic}/detail.aspx"

	#curl 'https://basket-11.wbbasket.ru/vol1627/part162731/162731640/info/ru/card.json'
	#curl 'https://basket-15.wbbasket.ru/vol2274/part227473/227473700/info/ru/card.json'
	#? url = f'https://basket-11.wbbasket.ru/vol{artic[:4]}/part{artic[:6]}/{artic}/info/ru/card.json'

	url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-366541&spp=30&ab_testing=false&nm={artic};'
	headers = {
		'accept': '*/*',
		'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'origin': 'https://www.wildberries.ru',
		'priority': 'u=1, i',
		'referer': 'https://www.wildberries.ru/catalog/227473700/detail.aspx',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'cross-site',
		'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
		'x-captcha-id': 'Catalog 1|1|1734120259|AA==|269c20cba1c94d90a7ed8c564686620f|rFYRMRLHrQDu5VCWBVQTmr6uthZRfSyWGyEw2jRhBLk'
  	}

	resp = requests.get(url=url, headers=headers)
	data = resp.json()
	#return data

	helpfull_data = data['data']['products']

	product_info = {
		'article': artic,
		'title': helpfull_data.get('name'),
		'img': img,
		'link': link,
		'price': helpfull_data['sizes'][0]['price']['total'] / 100,
		'bad_price': helpfull_data['sizes'][0]['price']['basic'] / 100,

		'product_rating': helpfull_data.get('reviewRating'),
		'feedbacks_count': helpfull_data.get('feedbacks'),
		'product_count': helpfull_data.get('totalQuantity'),
		'brand_name': helpfull_data.get('brand'),
		'brand_id': helpfull_data.get('brandId'),

		'seller_name': helpfull_data.get('supplier'),
		'seller_id': helpfull_data.get('supplierId'),
		'seller_rating': helpfull_data.get('supplierRating')
	}

	return json.dumps(product_info)

# много страниц
def wildberriesPagesParser(tovars): # [articule, articule, articule]
	data = [wildberriesPageParser(i) for i in tovars]
	return json.dumps(data, indent=2)


def test1():
	products = wildberriesHardParser('паста splat', 10)
	pp(products)

def test2():
	#res = wildberriesPageParser('162731640')
	res = wildberriesPageParser('227473700')
	pp(res)

def test3():
	res = wildberriesImgParser("165558475")
	pp(res)

if __name__ == '__main__':
	test2()