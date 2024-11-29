import requests
from bs4 import BeautifulSoup as BS


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

def main():
	prs = parser('https://status.epicgames.com')
	status = prs.find('component-inner-container', 'component-status')
	status.strip()

	print(status)

def main2():
	prs = parser('https://www.perplexity.ai')
	text = prs.find('font-regular').strip()

	print(status)

def main3():
	prs = parser('https://gpt-open.ru/programmist')
	text = prs.find('prem-block-one').strip()

	print(text)




if __name__ == '__main__':
	main()