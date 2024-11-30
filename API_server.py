from flask import Flask, jsonify, request
from databaseTools import DataBase
import config
from parsingTools import wildberriesHardParser as finder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = DataBase(config.TABLE_PATH)

@app.route('/users', methods=['POST'])
def createUser():
    # Получаем JSON данные из запроса
    data = request.get_json()

    # Извлекаем параметры из JSON
    mail = data.get('mail')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')
    patname = data.get('patname')

    usr_id = db.createUser(mail, password, name, surname, patname)

    return jsonify({"ok": True, "id":usr_id}), 201

@app.route('/auh', methods=['GET'])
def authentication():
    # Получаем JSON данные из запроса
    data = request.get_json()

    # Извлекаем параметры из JSON
    mail = data.get('mail')
    password = data.get('password')

    if db.authentication(mail, password):
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"ok": False}), 200


@app.route('/favorites', methods=['DELETE'])
def delFromFavorites():
    # Получаем JSON данные из запроса
    data = request.get_json()

    # Извлекаем параметры из JSON
    fav_id = data.get('id')

    if db.delFromFavorites(fav_id):
        return jsonify({"ok": True}), 204
    else:
        return jsonify({"ok": False, "id": fav_id}), 404

'''
@app.route('/search?query=<query>', methods=['GET'])
def search(query):
    res = finder(query, config.SEARCHLIMIT)
    return jsonify(res), 200
'''
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    res = finder(query, config.SEARCHLIMIT)
    return jsonify(res), 200

# FIXME
@app.route('/product/<int:artic>', methods=['GET'])
def get_prod(artic):
    res = и()
    return jsonify(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)