import sqlite3, smallTools, config, random
from smallTools import save_logs
from random import randint
from parsingTools import wildberriesPagesParser as WPSP

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

			if not self.fetchOne(f"SELECT * FROM {table} WHERE {column} = ?", (formatted_number,)):
				return formatted_number


	def createUser(self, mail, password, name, surname, patname):
		usr_id = self.createID(config.TABLE_USERS_NAME, config.COLUMN_USERID_NAME)

		self.execute(f"INSERT INTO {config.TABLE_USERS_NAME} VALUES(?, ?, ?, ?, ?, ?, ?)", (usr_id, mail, password, name, surname, patname, 'False'))

		return str(usr_id)

	def authentication(self, mail, password):
		db_password = self.fetchOne(f"SELECT {config.COLUMN_PASSWORD_NAME} FROM {config.TABLE_USERS_NAME} WHERE {config.COLUMN_MAIL_NAME} = ?", (mail,))
		
		# если db_password не пустой и если пароль совпадает True иначе False
		if db_password and db_password[0] == password:
			return True
		else:
			save_logs("неправильный логин или пароль")
			return False

	# FIXME (добавить в api????) (или оставить её сервисной...)
	def _getUserFavoritesUrls(self, user_id):
		# Получаем все articule из таблицы favorite с заданным user_id
		res = self.fetchAll(f"SELECT articule FROM {config.TABLE_FAV_NAME} WHERE {config.COLUMN_USERID_NAME} = ?", (user_id,))
		print(res)
		return res # [articule, articule, articule]

	def getFromFavorites(self, user_id):
		tovars = self._getUserFavoritesUrls(user_id)
		return WPSP(tovars)

	def addToFavorites(self, user_id, artic):
		fav_id = self.createID(config.TABLE_FAV_NAME, config.COLUMN_FAVID_NAME)
		self.execute(f"INSERT INTO {config.TABLE_FAV_NAME} VALUES(?, ?, ?)", (fav_id, artic, user_id))
		return fav_id

	def delFromFavorites(self, user_id, artic):
        res = self.execute(f"DELETE FROM {config.TABLE_FAV_NAME} WHERE {config.COLUMN_USERID_NAME} = ? AND {config.COLUMN_ARTICULE_NAME} = ?", (user_id, artic))
        return res
        




def main():
	db = DataBase(config.TABLE_PATH)
	#save_logs(db.user_count)
	#db.createUser('pohta@gmail.com', '123456', 'Dasha', 'Dashovna', 'Dashok')
	print(db.authentication('pohta@gmail.com', '123456'))


if __name__ == '__main__':
	main()