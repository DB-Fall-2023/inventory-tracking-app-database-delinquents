from flask import jsonify
from dao.localstatistics import LSDAO
from dao.intran import inTranDAO
from dao.part import Part_Dao
from dao.supplier import Supplier_Dao
from dao.warehouse import Warehouse_Dao
from dao.user import User_Dao
from dao.rack import Rack_Dao
from dao.supplies import Supplies_Dao
from dao.transactions import Transaction_Dao

class inTranHandler():

    def buildAttr_tran(self, inid, sid, rid, tid, uid, wid, pid, qty, inttotal, date, typ):
        result = {}
        result['tid'] = tid
        result['inid'] = inid
        result['rid'] = rid
        result['pid'] = pid
        result['sid'] = sid
        result['wid'] = wid
        result['uid'] = uid
        result['type'] = typ
        result['inttotal'] = inttotal
        result['intqty'] = qty
        result['intdate'] = date
        return result

    def maptodict(self, it):
        result = {'tid': it[0], 
                  'inid': it[1], 
                  'rid': it[2], 
                  'sid': it[3],
                  'uid': it[4], 
                  'wid': it[5], 
                  'pid': it[6], 
                  'date': it[7],
                  'qty': it[8], 
                  'total': it[9], 
                  'type': it[10]}
        return result

    def insertInTransaction(self, form):
        if len(form) != 5:
            return jsonify(Error = "Malformed post request"), 400
        else:
            pid = form['pid']
            sid = form['sid']
            wid = form['wid']
            qty= form['qty']
            uid = form['uid']
            daoU, daoP, daoW, daoS, daoR, daoT  = User_Dao(), Part_Dao(), Warehouse_Dao(), Supplier_Dao(), Rack_Dao(), Transaction_Dao()
            if not daoU.verifyUserworksWid(uid, wid):
                return jsonify(Error = "User Does Not Work in Warehouse or Doesn't Exist"), 404
            if not daoP.searchbyid(pid):
                return jsonify(Error = "Part Not Found"), 404
            if not daoW.searchbyid(wid):
                return jsonify(Error = "Warehouse Not Found"), 404
            if not daoS.searchbyid(sid):
                return jsonify(Error = "Supplier Not Found"), 404
            rid = daoR.searchrackbywidandpid(wid, pid)[0]
            if not rid:
                rid = daoR.insertrack(100, 0, pid, wid)   
            if not daoS.verifySupplierSuppliesPart(sid, pid):
                 return jsonify(Error = "Supplier Not Found or Doesn't Supply The Part"), 404 
            oldstock = Supplies_Dao().getStock(sid, pid)
            if oldstock - qty < 0:
                Supplies_Dao().addStock(sid, pid)     
            if pid and sid and wid and qty and uid:
                dao = inTranDAO() 
                attr = dao.getInAttributes(pid, wid)
                if attr:
                    wbudget, rstock, rcapacity, pprice = attr[0][0], attr[0][1], attr[0][2], attr[0][3]
                    inttotal = (float(qty) * pprice)
                    if wbudget >= inttotal:
                        if rcapacity >= (float(rstock) + float(qty)):
                            tid, date= daoT.insertTransaction(uid, wid, pid, qty, inttotal, 'incoming')
                            inid = dao.insertINT(tid, sid, rid)
                            result = self.buildAttr_tran(inid, sid, rid, tid, uid, wid, pid, qty, inttotal, date, 'incoming')
                            dao.updateWBudgetSub((-inttotal), wid)
                            daoR.updateRackStock(qty, rid)
                            Supplies_Dao().updateStock(sid, pid, qty)
                            return jsonify(Transaction = result), 200
                        else:
                            return jsonify(Error="Rack doesnt have enough space"), 400
                    else:
                        return jsonify(Error="Warehouse not having enough budget"), 400
            else:
                return jsonify("Unexpected attribute values."), 400
                    
    def getIncomingbyid(self, inid):
        dao = inTranDAO()
        result = dao.searchbyid(inid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def getAllInTran(self):
        dao = inTranDAO()
        results = dao.searchAll()
        if results:
            result = []
            for it in results:
                result.append(self.maptodict(it))
            return jsonify(Incomings = result)
        else:
            return jsonify(Error = "Transactions Not Found"), 404
        
    def updateIncomingbyid(self, inid, data):
        if len(data) != 3:
            return jsonify(Error = "Malformed post request"), 400
        qty = data['qty']
        date = data['date']
        uid = data['uid']
        daoU, daoP, daoW, daoS, daoR, daoT  = User_Dao(), Part_Dao(), Warehouse_Dao(), Supplier_Dao(), Rack_Dao(), Transaction_Dao()
        dao = inTranDAO()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error = "User Does Not Work in Warehouse or Doesn't Exist"), 404
        if qty > 0 and date and inid:
            tran = self.maptodict(dao.searchbyid(inid))
            if not tran:
                return jsonify(Error = "Transaction Not Found"), 404
            tid, oldtotal, oldqty, rid, wid, sid, pid = tran['tid'],tran['total'], tran['qty'],tran['rid'],tran['wid'],tran['sid'],tran['pid']
            attr = dao.getInAttributes(pid, wid)
            if attr:
                wbudget, rstock, rcapacity, pprice = attr[0][0], attr[0][1], attr[0][2], attr[0][3]
            inttotal = (float(qty) * pprice)
            oldstock = Supplies_Dao().getStock(sid, pid)
            addqty = qty - oldqty
            minusBudget = inttotal - oldtotal
            if oldqty > qty:
                removeqty = oldqty - qty
                dao.updateWBudgetSub((minusBudget), wid)
                daoR.updateRackStock((-removeqty), rid)
                Supplies_Dao().updateStock(sid, pid, removeqty)
                #Update transaction with new qty, price and date
                result = 0
                return jsonify(Transaction = result), 200
            if oldstock - addqty < 0:
                stockp = 100
                Supplies_Dao().updateStock(sid, pid, stockp)
            if wbudget >= inttotal:
                if rcapacity >= (float(rstock) + float(qty)):
                    #update transaction with new qty, price and date
                    dao.updateWBudgetSub((-minusBudget), wid)
                    daoR.updateRackStock(addqty, rid)
                    Supplies_Dao().updateStock(sid, pid, (-addqty))
                    result = 0
                    return jsonify(Transaction = result), 200
                else:
                    return jsonify(Error="Rack doesnt have enough space"), 400
            else:
                return jsonify(Error="Warehouse not having enough budget"), 400
        else:
            return jsonify("Unexpected attribute values."), 400