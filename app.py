from flask import Flask
from flask_cors import CORS

from handler.UsersHandler import UsersHandler
from handler.WarehouseHandler import WarehouseHandler

app = Flask(__name__)

# apply CORS
CORS(app)


@app.route('/')
def greeting():
    return 'Hello, this is the parts DB app'


if __name__ == '__main__':
    app.run(debug=True)
