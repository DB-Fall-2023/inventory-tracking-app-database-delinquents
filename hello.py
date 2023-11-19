from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from handler.part import Part_Handler
from handler.rack import Racket_Handler
from handler.supplier import Supplier_Handler
from handler.transactions import Transaction_Handler
from handler.user import User_Handler
from handler.warehouse import Warehouse_Handler
from handler.LocalStatistics import LSHandler
from handler.intran import inTranHandler
from handler.supplies import Supplies_Handler
from handler.extran import ExtranHandler

app = Flask(__name__)

# apply CORS
CORS(app)


@app.route('/database-delinquents')
def getin():
    return '<div style="font-size: 80px;">Hello word, this is the database-delinquents DB app</div>'


# ---------------------------------------------------------------------
# USER
@app.route('/database-delinquents/user',
           methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return User_Handler().getallusers()
    elif request.method == 'POST':
        data = request.json
        return User_Handler().insertuser(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/database-delinquents/user/<int:uid>',
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
@app.route('/database-delinquents/warehouse',
           methods=['GET', 'POST'])
def warehouses():
    if request.method == 'GET':
        return Warehouse_Handler().getallwarehouses()
    elif request.method == 'POST':
        data = request.json
        return Warehouse_Handler().insertwarehouse(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/database-delinquents/warehouse/<int:wid>',
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
@app.route('/database-delinquents/rack',
           methods=['GET', 'POST'])
def racks():
    if request.method == 'GET':
        return Racket_Handler().getallracks()
    elif request.method == 'POST':
        data = request.json
        return Racket_Handler().insertrack(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/database-delinquents/rack/<int:rid>',
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
@app.route('/database-delinquents/part',
           methods=['GET', 'POST'])
def parts():
    if request.method == 'GET':
        return Part_Handler().getallparts()
    elif request.method == 'POST':
        data = request.json
        return Part_Handler().insertpart(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/database-delinquents/part/<int:pid>',
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
@app.route('/database-delinquents/supplier',
           methods=['GET', 'POST'])
def suppliers():
    if request.method == 'GET':
        return Supplier_Handler().getallsuppliers()
    elif request.method == 'POST':
        data = request.json
        return Supplier_Handler().insertsupplier(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/database-delinquents/supplier/<int:sid>',
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
# SUPPLIES

@app.route('/database-delinquents/supplies', methods=['GET', 'POST', 'PUT', 'DELETE'])
def supplies():
    if request.method == 'GET':
        return Supplies_Handler().getallsupplies()
    elif request.method == 'POST':
        data = request.form
        return Supplies_Handler().insertsupplies(data)
    elif request.method == 'PUT':
        data = request.form
        return Supplies_Handler().updatebysidandpid(data)
    elif request.method == 'DELETE':
        data = request.form
        print(data)
        return Supplies_Handler().deletebysidandpid(data)
    else:
        return jsonify("Not supported"), 405


# ---------------------------------------------------------------------
# TRANSACTION
@app.route('/database-delinquents/transaction',
           methods=['GET', 'POST'])
def transactions():
    if request.method == 'GET':
        return Transaction_Handler().getalltransactions()
    elif request.method == 'POST':
        data = request.json
        return Transaction_Handler().inserttransaction(data)
    else:
        return jsonify("Not supported"), 405


@app.route('/database-delinquents/transaction/<int:pid>',
           methods=['GET', 'PUT', 'DELETE'])
def idtransaction(pid):
    if request.method == 'GET':
        return Transaction_Handler().searchbyid(pid)
    else:
        return jsonify("Not supported"), 405
    
# ---------------------------------------------------------------------
# INCOMING TRANSACTION

@app.route('/database-delinquents/incomingTransactions', methods=['POST', 'GET'])
def InTransactions():
    #qty = quantity of parts to be bought
    if request.method == 'POST':
        return inTranHandler().insertInTransaction(request.form)
    if request.method == "GET":
        return inTranHandler().getAllInTran()
    else:
        return jsonify(Error = "Method not Allowed"), 405

@app.route('/database-delinquents/incomingTRansaction/<int:inid>', methods=['GET', 'PUT'])
def idInTran(inid):
    if request.method == "GET":
        return inTranHandler().getIncomingbyid(inid)
    else:
        return jsonify("Not supported"), 405

# ---------------------------------------------------------------------
# EXCHANGE TRANSACTION

@app.route('/database-delinquents/exchange', methods=['GET', 'POST'])
def exchange():
    if request.method == 'GET':
        return ExtranHandler().getAllExchange()
    if request.method == 'POST':
        return ExtranHandler().insertExchange(request.json)
    else:
        return jsonify(Error = "Method not Allowed"), 405

@app.route('/database-delinquents/exchange/<int:extid>', methods=['GET', 'PUT'])
def exchangeById(extid):
    if request.method == 'GET':
        return ExtranHandler().getExchangeById(extid)
    if request.method == 'PUT':
        return ExtranHandler().updateExchangeById(extid, request.json)
    else:
        return jsonify(Error = "Method not Allowed"), 405

# ---------------------------------------------------------------------
# LOCAL STATISTIC
@app.route('/database-delinquents/warehouse/<int:wid>/profit', methods=['POST'])
def getWarehouseProfitByYear(wid):
    if request.method == 'POST':
        return LSHandler().getWarehouseProfitByYear(wid, request.json)
    return jsonify(Error="Method not allowed."), 405

@app.route('/database-delinquents/warehouse/<int:wid>/rack/lowstock', methods=['POST'])
def getTop5RackUnder25Pct(wid):
    if request.method == 'POST':
        return LSHandler().getTop5RackUnder25Pct(wid, request.json)
    return jsonify(Error="Method not allowed."), 405

@app.route('/database-delinquents/warehouse/<int:wid>/rack/material', methods=['POST'])
def getBottom3PartsByType(wid):
    if request.method == 'POST':
        return LSHandler().getBottom3PartsByType(wid, request.json)
    return jsonify(Error="Method not allowed."), 405

@app.route('/database-delinquents/warehouse/<int:wid>/rack/expensive', methods=['POST'])
def getExpensiveRacksbyID(wid):
    if request.method == 'POST':
        return LSHandler().getFiveExpensiveRacksbyID(wid, request.form)
    else:
        return jsonify(Error="Method not allowed."), 405
    
@app.route('/database-delinquents/warehouse/<int:wid>/transaction/supplier', methods=['POST'])
def getTopSuppliersbyID(wid):
    if request.method == 'POST':
        return LSHandler().getTopSupplierbyID(wid, request.form)
    else:
        return jsonify(Error="Method not allowed."), 405
    
@app.route('/database-delinquents/warehouse/<int:wid>/transaction/leastcost', methods=['POST'])
def getDaysLeastcostbyID(wid):
    if request.method == 'POST':
        return LSHandler().getDaysLeastcostbyID(wid, request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


# ---------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
