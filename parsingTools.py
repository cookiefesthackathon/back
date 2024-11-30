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


def wildberriesPageParser(product_url):
	    curl 'https://www.wildberries.ru/catalog/173077624/detail.aspx'
'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
'cache-control: max-age=0'
'cookie: captchaid=1734117768|6f0f3fe7f48b4db5b7c2f79aea31b409|3szWgO|a0zqWRbktWyo3AiHbJO1D8bWTFmYZqo61rxs5Gtoj9w; _wbauid=10399986081732908172; _cp=1'
'priority: u=0, i'
'sec-fetch-dest: document'
'sec-fetch-mode: navigate'
'sec-fetch-site: same-origin'
'sec-fetch-user: ?1'
'upgrade-insecure-requests: 1'
'user-agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'

	 
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

	resp = requests.get(url=product_url, headers=headers)
	#return resp.json()


def soup(url):
    try:
        # Отправляем GET-запрос на указанный URL
        response = requests.get(url)
        # Проверяем, успешен ли запрос (статус код 200)
        response.raise_for_status()
        
        # Создаем объект BeautifulSoup для парсинга HTML-контента
        soup = BS(response.text, 'html.parser')
        
        # Возвращаем отформатированный HTML-код страницы
        return soup.prettify()
    
    except requests.exceptions.RequestException as e:
        # Обрабатываем возможные ошибки запроса
        print(f"Произошла ошибка при запросе: {e}")
        return None


def mainSoup():
	# Пример использования функции
	url = "https://www.wildberries.ru/catalog/173077624/detail.aspx"
	html_content = soup(url)
	if html_content:
	    print(html_content)



def main1():
	# Пример использования
	url = "https://www.wildberries.ru/catalog/173077624/detail.aspx"
	img = wildberriesPageParser(url)
	print(img)


def main():
	# Пример вызова функции
	products = wildberriesHardParser('паста splat', 10)
	print(products)



if __name__ == '__main__':
	mainSoup()