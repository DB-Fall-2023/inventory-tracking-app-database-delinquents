# from flask import Flask, jsonify, request
# from flask_cors import CORS, cross_origin

# app = Flask(__name__)

# #apply CORS
# CORS(app)

# @app.route('/')
# def greeting():
#     return 'Hello, this is the parts DB app'

# if __name__ == '__main__':
#     app.run()

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1 style='color:green'>Hello World!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
