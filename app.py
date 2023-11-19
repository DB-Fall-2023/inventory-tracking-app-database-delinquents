from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from handlers.UsersHandler import UsersHandler
from handlers.WarehouseHandler import WarehouseHandler

app = Flask(__name__)

#apply CORS
CORS(app)

@app.route('/')
def greeting():
    return 'Hello, this is the parts DB app'

@app.route("/warehouse/all")
def getAllWarehouses():
    return WarehouseHandler().get_all_warehouses()

@app.route("/most/deliver")
def top_warehouse_deliverer():
    return WarehouseHandler().get_top_deliverers()

@app.route("/most/transactions")
def top_users_transactions():
    return UsersHandler().get_top3_transactioners()

@app.route("/least/outgoing")
def least_warehouse_outgoing():
    return WarehouseHandler().get_least_outgoing_warehouses()

@app.route("/most/city")
def top3_cities_transactions():
    return WarehouseHandler().get_top3_cities_transactions()


if __name__ == '__main__':
    app.run(debug=True)
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<h1 style='color:green'>Hello World!</h1>"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
