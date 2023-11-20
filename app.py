from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from handlers.UsersHandler import UsersHandler
from handlers.WarehouseHandler import WarehouseHandler

app = Flask(__name__)

# apply CORS
CORS(app)


@app.route('/')
def greeting():
    return 'Hello, this is the parts DB app'


if __name__ == '__main__':
    app.run(debug=True)
