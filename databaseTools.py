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

def path(text):
	path_to_file = os.path.abspath(__file__)
	filename = os.path.basename(path_to_file)
	
	return path_to_file[:-len(filename)] + text


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

	def execute(self, text, params):
		self._open()
		res = self.cursor.execute(text, params)
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

	def createID(self):
		while True:
			random_number = randint(0, 999999)
			formatted_number = f'{random_number:06}'

			if not self.fetchOne(f"SELECT * FROM {config.TABLE_USERS_NAME} WHERE {config.COLUMN_USERS_NAME} = ?", (formatted_number,)):
				return formatted_number

	def createUser(self, mail, password, name, surname, patname):
		usr_id = self.createID()
		self.execute(f"INSERT INTO {config.TABLE_USERS_NAME} VALUES(?, ?, ?, ?, ?, ?, ?)", (usr_id, mail, password, name, surname, patname, '[]'))

	def authentication(self, mail, password):
		db_password = self.fetchOne(f"SELECT {config.COLUMN_PASSWORD_NAME} FROM {config.TABLE_USERS_NAME} WHERE {config.COLUMN_MAIL_NAME} = ?", (mail,))
		
		# если db_password не пустой и если пароль совпадает True иначе False
		if db_password and db_password[0] == password:
			return True
		else:
			save_logs("неправильный логин или пароль")
			return False

	def addToFavorites(self, )




'''
добавить в избранное
удаление элементов из избранного
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