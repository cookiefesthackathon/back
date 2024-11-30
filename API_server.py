from flask import Flask, jsonify, request
from flask_cors import CORS

from databaseTools import DataBase
import config

from parsingTools import wildberriesHardParser as WHP
from parsingTools import wildberriesImgParser as WIP
from parsingTools import wildberriesPageParser as WPP

app = Flask(__name__)
CORS(app)
db = DataBase(config.TABLE_PATH)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    res = WHP(query, config.SEARCHLIMIT)
    return jsonify(res), 200

@app.route('/users', methods=['POST'])
def createUser():
    try:
        data = request.get_json()
        mail = data.get('mail')
        password = data.get('password')
        name = data.get('name')
        surname = data.get('surname')
        patname = data.get('patname')

        usr_id = db.createUser(mail, password, name, surname, patname)
        return jsonify({"ok": True, "id":usr_id}), 201

    except:
        return jsonify({"ok": False}), 500

@app.route('/auh', methods=['GET'])
def authentication():
    mail = request.args.get('mail')
    password = request.args.get('password')

    if db.authentication(mail, password):
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"ok": False}), 200

@app.route('/favorites', methods=['GET', 'POST', 'DELETE'])
def handleFavorites():
    user_id = request.args.get('user_id')
    try:
        artic = request.args.get('artic')
    except:
        artic = None # если вызывают GET и artic не указывают

    if request.method == 'DELETE':
        try:
            
            res = db.delFromFavorites(user_id, artic):
            if res:
                return jsonify({"ok": True, "data":res}), 204
            else:
                return jsonify({"ok": False, "data":res}), 406

        except:
            return jsonify({"ok": False}), 500

    elif request.method == 'POST':
        try:
            res = db.addToFavorites(user_id, artic):
            return jsonify({"ok": True, "data": res}), 201 #FIXME data?
        except:
            return jsonify({"ok": False, "id": fav_id}), 500

    elif request.method == 'GET':
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
    app.run(host='0.0.0.0', port=5000, debug=True)