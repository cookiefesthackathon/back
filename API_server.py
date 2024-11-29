from flask import Flask, jsonify, request
from databaseTools import DataBase
import config
from parsingTools import wildberriesHardParser as finder

app = Flask(__name__)
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

    db.createUser(mail, password, name, surname, patname)

    return jsonify({"message": "User created successfully!"}), 201

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

    if db.delFromFavorites(fav_id)
        return jsonify({"message": "success"}), 204
    else:
        return jsonify({"message": f"not found favorite '{fav_id}'"}), 404


@app.route('/<str:query>', methods=['GET'])
def search(products):
    res = finder(query, config.SEARCHLIMIT)
    return jsonify(res), 200





'''
# 1. Получение всех продуктов (GET)
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# 2. Получение одного продукта по ID (GET)
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

# 3. Создание нового продукта (POST)
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"]
    }
    products.append(new_product)
    return jsonify(new_product), 201

# 4. Обновление продукта (PUT)
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    product.update(data)
    return jsonify(product)

# 5. Удаление продукта (DELETE)
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return '', 204
'''


if __name__ == '__main__':
    app.run(debug=True)