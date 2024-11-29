import requests
from pprint import pprint
from bs4 import BeautifulSoup as BS


class simpleParser(object):
	"""docstring for simpleParser"""
	def __init__(self, url):
		self.url = url

		r = requests.get(self.url)
		self.html = BS(r.text, 'html.parser')

	def find(self, *class_list):

		res = self.html
		for i in class_list:
			res = res.find(class_=i)

		return res.text if res else res

def wildberriesParser(query, n):
    url = f'https://www.wildberries.ru/catalog/search.aspx?search={query}'
    response = requests.get(url)
    soup = BS(response.text, 'html.parser')
    products = []

    # Поиск карточек товаров
    for product in soup.find_all('div', class_='product-card')[:n]:
        title = product.find('span', class_='goods-name').text.strip()
        link = 'https://www.wildberries.ru' + product.find('a', class_='referrer').get('href')
        image = product.find('img').get('src')
        seller = product.find('a', class_='seller-name').text.strip()
        rating = product.find('span', class_='rating').text.strip() if product.find('span', class_='rating') else 'Нет'
        price = product.find('ins', class_='lower-price').text.strip()

        # Добавление продукта в список
        products.append({
            'title': title,
            'link': link,
            'image': image,
            'seller': seller,
            'rating': rating,
            'price': price
        })

    return products

def wildberriesHardParser(query, n):
	#url = 'https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-1257786&query=buheirb&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false'
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

	return resp.json()


def main():
	# Пример вызова функции
	products = wildberriesHardParser('паста splat', 5)
	pprint(products)

def main3():
	products = wildberriesParser('паста splat', 5)
	print(products)


def main2():
	prs = simpleParser('https://status.epicgames.com')
	status = prs.find('component-inner-container', 'component-status')
	status.strip()

	print(status)



if __name__ == '__main__':
	main()