import sqlite3, stopWatch



def path(text):
    path_to_file = os.path.abspath(__file__)
    filename = os.path.basename(path_to_file)
    
    return path_to_file[:-len(filename)] + text



class DataBase(object):
	"""docstring for DataBase"""
	def __init__(self, path):
		self.path = path

	def _open(self):
		self.db = sqlite3.connect(smallTools.path(self.path)) # Открытие
		self.cursor = self.db.cursor() # инициализация курсора

	def close(self):
		self.db.commit()# обновление в базе данных
		self.db.close() # закрытие базы данных
			
	def createUser(self, usr_id, usr_name, usr_first_name):

		self._open()
		usr_name = f'@{usr_name}'
		sys_mess = str(smallTools.system_message(usr_first_name))

		self.cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", (int(usr_id), usr_name, str(usr_first_name), smallTools.time(), sys_mess))

		self.close()

	'''
	def checkId(self, usr_id):
		self._open()
		self.cursor.execute("SELECT id FROM users WHERE id = ?", ([usr_id]))
		res = self.cursor.fetchone()[0]
		self.close()

		return True if res else False
	'''

	def execute(self, filters):
		self._open()
		res = self.cursor.execute(filters)
		self.close()
		return res


	def fetchOne(self, filters):
		self._open()
		self.cursor.execute(filters)
		res = self.cursor.fetchone()
		self.close()

		return res
	
def main():
	pass

if __name__ == '__main__':
	main()