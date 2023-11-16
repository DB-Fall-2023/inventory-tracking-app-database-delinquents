from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from handler.part import Part_Handler
from handler.rack import Racket_Handler
from handler.supplier import Supplier_Handler
from handler.transaction import Transaction_Handler
from handler.user import User_Handler
from handler.warehouse import Warehouse_Handler

app = Flask(__name__)

# apply CORS
CORS(app)


@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents')
def getin():
    return '<div style="font-size: 80px;">Hello word, this is the database-delinquents DB app</div>'


# ---------------------------------------------------------------------
# USER
@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/user',
           methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return User_Handler().getallusers()
    elif request.method == 'POST':
        data = request.json
        return User_Handler().insertuser(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/user/<int:uid>',
           methods=['GET', 'PUT', 'DELETE'])
def iduser(uid):
    if request.method == 'GET':
        return User_Handler().searchbyid(uid)
    elif request.method == 'DELETE':
        return User_Handler().deletebyid(uid)
    elif request.method == 'PUT':
        data = request.json
        return User_Handler().updatebyid(uid, data)
    else:
        return jsonify("Not supported"), 405


# ---------------------------------------------------------------------
# WAREHOUSE
@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/warehouse',
           methods=['GET', 'POST'])
def warehouses():
    if request.method == 'GET':
        return Warehouse_Handler().getallwarehouses()
    elif request.method == 'POST':
        data = request.json
        return Warehouse_Handler().insertwarehouse(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/warehouse/<int:wid>',
           methods=['GET', 'PUT', 'DELETE'])
def idwarehouse(wid):
    if request.method == 'GET':
        return Warehouse_Handler().searchbyid(wid)
    # elif request.method == 'DELETE':
    #     return Warehouse_Handler().deletebyid(wid)
    elif request.method == 'PUT':
        data = request.json
        return Warehouse_Handler().updatebyid(wid, data)
    else:
        return jsonify("Not supported"), 405


# ---------------------------------------------------------------------
# RACK
@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/rack',
           methods=['GET', 'POST'])
def racks():
    if request.method == 'GET':
        return Racket_Handler().getallracks()
    elif request.method == 'POST':
        data = request.json
        return Racket_Handler().insertrack(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/rack/<int:rid>',
           methods=['GET', 'PUT', 'DELETE'])
def idrack(rid):
    if request.method == 'GET':
        return Racket_Handler().searchbyid(rid)
    elif request.method == 'PUT':
        data = request.json
        return Racket_Handler().updatebyid(rid, data)
    else:
        return jsonify("Not supported"), 405


# ---------------------------------------------------------------------
# PART
@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/part',
           methods=['GET', 'POST'])
def parts():
    if request.method == 'GET':
        return Part_Handler().getallparts()
    elif request.method == 'POST':
        data = request.json
        return Part_Handler().insertpart(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/part/<int:pid>',
           methods=['GET', 'PUT', 'DELETE'])
def idpart(pid):
    if request.method == 'GET':
        return Part_Handler().searchbyid(pid)
    elif request.method == 'DELETE':
        return Part_Handler().deletebyid(pid)
    elif request.method == 'PUT':
        data = request.json
        return Part_Handler().updatebyid(pid, data)
    else:
        return jsonify("Not supported"), 405


# ---------------------------------------------------------------------
# SUPPLIER
@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/supplier',
           methods=['GET', 'POST'])
def suppliers():
    if request.method == 'GET':
        return Supplier_Handler().getallsuppliers()
    elif request.method == 'POST':
        data = request.json
        return Supplier_Handler().insertsupplier(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/supplier/<int:sid>',
           methods=['GET', 'PUT', 'DELETE'])
def idsupplier(sid):
    if request.method == 'GET':
        return Supplier_Handler().searchbyid(sid)
    elif request.method == 'PUT':
        data = request.json
        return Supplier_Handler().updatebyid(sid, data)
    else:
        return jsonify("Not supported"), 405


# ---------------------------------------------------------------------
# TRANSACTION
@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/transaction',
           methods=['GET', 'POST'])
def transactions():
    if request.method == 'GET':
        return Transaction_Handler().getalltransactions()
    elif request.method == 'POST':
        data = request.json
        return Transaction_Handler().inserttransaction(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/ec2-44-220-7-157.compute-1.amazonaws.com/database-delinquents/transaction/<int:pid>',
           methods=['GET', 'PUT', 'DELETE'])
def idtransaction(pid):
    if request.method == 'GET':
        return Transaction_Handler().searchbyid(pid)
    else:
        return jsonify("Not supported"), 405


# ---------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
