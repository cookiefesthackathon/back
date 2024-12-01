from flask import Flask, jsonify, request
from flask_cors import CORS

from databaseTools import DataBase
from smallTools import save_logs
import config

from parsingTools import wildberriesHardParser as WHP
from parsingTools import wildberriesPageParser as WPP
from parsingTools import wildberriesSortParser as WSP


app = Flask(__name__)
CORS(app)
db = DataBase(config.TABLE_PATH)

'''
правила нейминга от тимофея
переменные - snake_case
константы - UPPER_CASE
классы - PascalCase
функции - camelCase
фикс метки - FIXME
'''


@app.route('/search', methods=['GET'])
def search():
	'''
	выполняет поиск
	пример: http://IP:5000/search?query="шторы"
	штатный возврат - список с данными в виде json
	'''
	query = request.args.get('query')

	if query:
		save_logs('search по', query)

		res = WHP(query, config.SEARCHLIMIT)
		return jsonify(res), 200
	else:
		return jsonify({"ok": False}), 400


@app.route('/sortsearch', methods=['GET'])
def sortsearch():
	'''
	выполняет поиск и сортирует содержимое по любому указанному полю по ключу
	пример: http://IP:5000/sortsearch?query=Шторы&filter=price&reverse=false
	штатный возврат - отсортированный список с данными в виде json 
	'''
	try:
		query = request.args.get('query')
		filt = request.args.get('filter')
		reverse = request.args.get('reverse')
		save_logs(query, filt, reverse)

		res = WSP(query, filt, config.SEARCHLIMIT, reverse)

		return res, 200

	except:
		return jsonify({"ok": False}), 400


@app.route('/users', methods=['POST'])
def createUser():
	'''
	создание пользователя путём добавления одной записи заполняя передаваемыми данными
	пример: http://IP:5000/users
	штатный возврат - json со статусом ok (True/False) и usr_id с id созданного пользователя
	'''
	#try:
	data = request.get_json()
	mail = data.get('mail')
	password = data.get('password')
	name = data.get('name')
	surname = data.get('surname')
	patname = data.get('patname')
	save_logs("create", mail, password, name, surname, patname)

	usr_id = db.createUser(mail, password, name, surname, patname)
	return jsonify({"ok": True, "id": usr_id}), 201

	#except:
		#return jsonify({"ok": False}), 400


@app.route('/auh', methods=['GET'])
def authentication():
	'''
	авторизирует пользователя по mail и password
	пример: http://IP:5000/auh?password=securepassword123&mail=fdfdf@example.com
	штатный возврат - json со статусом ok (True/False) и usr_id с id пользователя
	'''
	mail = request.args.get('mail')
	password = request.args.get('password')

	save_logs(mail, password)

	state, usr_id = db.authentication(mail, password)

	if state:
		return jsonify({"ok": True, 'user_id': usr_id}), 200
	else:
		return jsonify({"ok": False, 'user_id': usr_id}), 200


@app.route('/favorites', methods=['GET', 'POST', 'DELETE'])
def handleFavorites():
	'''
	операции удаления, добавления, запроса данных в таблице favorites в базе данных
	примеры: 
		DELETE http://IP:5000/favorites?user_id=250261&artic=109832438
		POST http://IP:5000/favorites?user_id=250261&artic=173077624
		GET http://IP:5000/favorites?user_id=250261
	штатные возвраты - json со статусом ok (True/False) 
		+ "data": "518505" при POST
		+ список с данными в виде json при GET
	'''
	user_id = request.args.get('user_id')
	if not user_id: return jsonify({"ok": False}), 400

	# sorry for hardcode
	if request.method == 'DELETE':
		artic = request.args.get('artic')
		save_logs('DELETE', user_id, artic)

		if not artic: return jsonify({"ok": False}), 400

		try:
			res = db.delFromFavorites(user_id, artic)
			return jsonify({"ok": True}), 204
		except:
			return jsonify({"ok": False}), 500

	elif request.method == 'POST':
		artic = request.args.get('artic')
		save_logs('POST', user_id, artic)
		if not artic: return jsonify({"ok": False}), 400

		try:
			res = db.addToFavorites(user_id, artic)
			return jsonify({"ok": True, "data": res}), 201
		except:
			return jsonify({"ok": False}), 500

	elif request.method == 'GET':
		save_logs('GET', user_id)
		try:
			res = db.getFromFavorites(user_id)
			return res, 200
		except:
			return jsonify({"ok": False}), 500


@app.route('/product', methods=['GET'])
def getProd():
	'''
	выдаёт данные о товаре по артикулу
	пример: http://127.0.0.1:5000/product?artic=207210490
	штатный возврат - список с данными в виде json
	'''
	artic = request.args.get('artic')
	res = WPP(artic)
	return res, 200


if __name__ == '__main__':
	if config.OPEN_NETWORK_API:
		app.run(host='0.0.0.0', port=5000, debug=True)
	else:
		app.run(debug=True)
