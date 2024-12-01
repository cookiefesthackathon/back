from flask import Flask, jsonify, request
from flask_cors import CORS

from databaseTools import DataBase
from smallTools import save_logs
import config

from parsingTools import wildberriesHardParser as WHP
from parsingTools import wildberriesImgParser as WIP
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
    query = request.args.get('query')

    if query:
        save_logs('search по', query)

        res = WHP(query, config.SEARCHLIMIT)
        return jsonify(res), 200
    else:
        return jsonify({"ok": False}), 400


@app.route('/sortsearch', methods=['GET'])
def sortsearch():
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
    try:
        data = request.get_json()
        mail = data.get('mail')
        password = data.get('password')
        name = data.get('name')
        surname = data.get('surname')
        patname = data.get('patname')
        save_logs("create", mail, password, name, surname, patname)

        usr_id = db.createUser(mail, password, name, surname, patname)
        return jsonify({"ok": True, "id":usr_id}), 201

    except:
        return jsonify({"ok": False}), 400

@app.route('/auh', methods=['GET'])
def authentication():
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
    user_id = request.args.get('user_id')
    if not user_id: return jsonify({"ok": False}), 400

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
    artic = request.args.get('artic')
    res = WPP(artic)
    return res, 200


if __name__ == '__main__':
    if config.OPEN_NETWORK_API:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(debug=True)