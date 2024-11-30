import sqlite3, smallTools, config, random
from smallTools import save_logs
from random import randint

'''
правила нейминга от тимофея
переменные - snake_case
константы - UPPER_CASE
классы - PascalCase
функции - camelCase
фикс метки - FIXME
'''

class DataBase(object):
	"""docstring for DataBase"""
	def __init__(self, path):
		self.path = path
		#self.user_count = len(self.fetchOne(f"SELECT COUNT(*) FROM {config.TABLE_USERS_NAME}"))

	def _open(self, path_input=None):
		path = path_input or self.path

		save_logs(path)
		self.db = sqlite3.connect(path) # Открытие
		self.cursor = self.db.cursor() # инициализация курсора

	def close(self):
		self.db.commit()# обновление в базе данных
		self.db.close() # закрытие базы данных

	def execute(self, text, params=None): # режим ANTIinjection если params
		self._open()

		if params:
			res = self.cursor.execute(text, params)
		else:
			res = self.cursor.execute(text)

		self.close()
		return res

	def fetchOne(self, text, params=None): # режим ANTIinjection если params
		self._open()
		if params:
			self.cursor.execute(text, params)
			res = self.cursor.fetchone()
		else:
			self.cursor.execute(text)
			res = self.cursor.fetchone()
		self.close()
		return res

	def fetchAll(self, text, params=None): # режим ANTIinjection если params
		self._open()
		if params:
			self.cursor.execute(text, params)
			res = self.cursor.fetchall()
		else:
			self.cursor.execute(text)
			res = self.cursor.fetchall()
		self.close()
		return res

	def createID(self, table, column):
		while True:
			random_number = randint(0, 999999)
			formatted_number = f'{random_number:06}'

			if not self.fetchOne(f"SELECT * FROM {config.TABLE_USERS_NAME} WHERE {config.COLUMN_USERS_NAME} = ?", (formatted_number,)):
				return formatted_number

	def createFavID(self):
		while True:
			random_number = randint(0, 999999)
			formatted_number = f'{random_number:06}'

			if not self.fetchOne(f"SELECT * FROM {config.TABLE_USERS_NAME} WHERE {config.COLUMN_USERS_NAME} = ?", (formatted_number,)):
				return formatted_number	


	def createUser(self, mail, password, name, surname, patname):
		usr_id = self.createID(config.TABLE_USERS_NAME, config.COLUMN_USERS_NAME)

		self.execute(f"INSERT INTO {config.TABLE_USERS_NAME} VALUES(?, ?, ?, ?, ?, ?, ?)", (usr_id, mail, password, name, surname, patname, 'False'))

	def authentication(self, mail, password):
		db_password = self.fetchOne(f"SELECT {config.COLUMN_PASSWORD_NAME} FROM {config.TABLE_USERS_NAME} WHERE {config.COLUMN_MAIL_NAME} = ?", (mail,))
		
		# если db_password не пустой и если пароль совпадает True иначе False
		if db_password and db_password[0] == password:
			return True
		else:
			save_logs("неправильный логин или пароль")
			return False

	# FIXME (добавить в api)
	def addToFavorites(self, user_id, artic, url=None):
		tovar_id = self.createID(config.TABLE_TOVAR_NAME, config.COLUMN_TOVID_NAME)
		url = f"https://www.wildberries.ru/catalog/{tovar_id}/detail.aspx" if not url else url
		self.execute(f"INSERT INTO {config.TABLE_TOVAR_NAME} VALUES(?, ?, ?)", (tovar_id, artic, url))

		fav_id = self.createID(config.TABLE_FAV_NAME, config.COLUMN_FAVID_NAME)	
		self.execute(f"INSERT INTO {config.TABLE_FAV_NAME} VALUES(?, ?, ?)", (fav_id, user_id, tovar_id))

	# FIXME (добавить в api????)
	def getUserFavoritesUrl(self, user_id):
		# Получаем все записи из таблицы favorite с заданным user_id
		favorite_records = self.fetchAll("SELECT tovar_id FROM favorite WHERE user_id = ?", (n,))

		# Извлекаем articule и url для каждого tovar_id из таблицы tovar
		res = []
		for record in favorite_records:
			tovar_id = record[0]
			tovar_data = self.fetchOne("SELECT articule, url FROM tovar WHERE tovar_id = ?", (tovar_id,))
			if tovar_data:
				res.append(tovar_data)

		return res # [(articule, url), (articule, url), (articule, url)]

	def getUserFavoritesJson(self, user_id):
		tovars = getUserFavoritesUrl(user_id)









	def delFromFavorites(self, fav_id):
		try:
			res = self.execute(f'DELETE FROM {config.TABLE_FAV_NAME} WHERE {config.COLUMN_FAVID_NAME} = ?', fav_id)
			save_logs(res)
			return True
		except:
			return False




'''
добавить в избранное
вывод изранного

??
хранение пароля в зашифрованном виде?
удаление пользователей?
'''


def main():
	db = DataBase(config.TABLE_PATH)
	#save_logs(db.user_count)
	#db.createUser('pohta@gmail.com', '123456', 'Dasha', 'Dashovna', 'Dashok')
	print(db.authentication('pohta@gmail.com', '123456'))


if __name__ == '__main__':
	main()