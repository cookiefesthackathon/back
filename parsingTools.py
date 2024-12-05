import requests, json, config
from bs4 import BeautifulSoup as BS
from flask import jsonify
from pprint import pprint as pp
from smallTools import save_logs
from smallTools import stopWatch as sw

'''
правила нейминга от тимофея
переменные - snake_case
константы - UPPER_CASE
классы - PascalCase
функции - camelCase
фикс метки - FIXME
'''

def wildberriesImgParserRESERV(article_number):

	query = f"артикул {article_number}"
	search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
	
	response = requests.get(search_url, headers=headers)
	soup = BS(response.text, 'html.parser')
	
	images = soup.find_all('img')
	
	if len(images) > 1:
		return images[1]['src']
	else:
		return "https://cartopen.ru/image/cache/catalog/no-image-1300x760.jpg"


# картинка по артикулу
def wildberriesImgParser(article_number):
	query = f"site:wildberries.ru {article_number} pic"
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
	if len(images) > 1:
		return images[1]['src']
	else:
		#return wildberriesImgParserRESERV(article_number)
		return "https://cartopen.ru/image/cache/catalog/no-image-1300x760.jpg"

# картинка по артикулу
def wildberriesBESTImgParser(artic: int):
	artic = int(artic)
	b = artic // 100000  # Аналог ~~ (быстрое округление вниз)
	ranges = [143, 287, 431, 719, 1007, 1061, 1115, 1169, 1313, 1601, 1655, 1919, 2045, 2189, 2405, 2621, 2837, 3053, 3269, 3485]
	
	# Найти индекс первого элемента в ranges, который больше или равен b
	a_index = next((i + 1 for i, limit in enumerate(ranges) if b <= limit), 21)
	
	# Преобразовать в строку с ведущими нулями
	a = str(a_index).zfill(2)
	
	# Сформировать URL
	return f"https://basket-{a}.wbbasket.ru/vol{b}/part{artic // 1000}/{artic}/images/c516x688/1.webp"


# поисковый парсер
def wildberriesHardParser(query, limit=0):
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

	data = data['data']['products'][:limit] if limit else data['data']['products']
	products = []
	for item in data:
		artic = item.get('id')
		s = sw()
		img = wildberriesBESTImgParser(artic)
		print(sw(s))

		product_info = {
			'article': artic,  # Артикул продукта
			'title': item.get('name'),
			'img': img,
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
	return json.dumps(products, indent = 2, ensure_ascii = False)

# поиск и сортировка
def wildberriesSortParser(query, filt, limit, reverse = False):
	#print(type(query), type(filt), type(limit), type(reverse))

	# безлимитный поиск, потом сортировка, потом обрезка до лимита
	res = wildberriesHardParser(query, config.SEARCHLIMIT)
	res = json.loads(res)

	sorted_res = sorted(res, key=lambda x: x[filt], reverse=bool(reverse)) # lambda потому что key может быть только функцией

	limit_res = sorted_res[:limit] if limit else sorted_res # также даёт выбор делать лимит или выдать всё

	return json.dumps(limit_res, indent = 2, ensure_ascii = False)

# одна страница
def wildberriesPageParser(artic):
	if not artic: return None

	img = wildberriesBESTImgParser(artic)
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
		'referer': link,
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'cross-site',
		'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
		'x-captcha-id': 'Catalog 1|1|1734120259|AA==|269c20cba1c94d90a7ed8c564686620f|rFYRMRLHrQDu5VCWBVQTmr6uthZRfSyWGyEw2jRhBLk'
  	}

	resp = requests.get(url=url, headers=headers)
	data = resp.json()
	#return data

	helpfull_data = data['data']['products'][0]

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

	return json.dumps(product_info, ensure_ascii=False)

# много страниц
def wildberriesPagesParser(tovars): # [articule, articule, articule]
	data = [wildberriesPageParser(i) for i in tovars]
	return json.dumps(data, indent=2, ensure_ascii=False)


def test1():
	products = wildberriesHardParser('шторы', 3)
	print(products)
def test2():
	#res = wildberriesPageParser('162731640')
	res = wildberriesPageParser('95666887')
	pp(res)
def test3():
	res = wildberriesBESTImgParser("165558475")
	pp(res)
def test4():
	res = wildberriesSortParser('Шторы', 'price', 30, False)
	pp(res)

if __name__ == '__main__':
	test3()
