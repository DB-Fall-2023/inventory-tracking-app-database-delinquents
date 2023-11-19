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
            rid = daoR.searchrackbywidandpid(wid, pid)
            if not rid:
                rid = daoR.insertrack(100, 0, pid, wid)  
            if not daoS.verifySupplierSuppliesPart(sid, pid):
                 return jsonify(Error = "Supplier Not Found or Doesn't Supply The Part"), 404 
            oldstock = Supplies_Dao().getStock(sid, pid)
            if oldstock - qty < 0:
                Supplies_Dao().updateStock(sid, pid, 100, 'sum')     
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
                            daoR.updateRackStock(qty, rid, 'sum')
                            Supplies_Dao().updateStock(sid, pid, qty, 'subtract')
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
        date = data['date:MM/DD/YYYY']
        uid = data['uid']
        daoU, daoP, daoW, daoS, daoR, daoT  = User_Dao(), Part_Dao(), Warehouse_Dao(), Supplier_Dao(), Rack_Dao(), Transaction_Dao()
        dao = inTranDAO()
        if qty > 0 and date and uid:
            oldTransaction = self.maptodict(dao.searchbyid(inid))
            if not oldTransaction:
                return jsonify(Error = "Transaction Not Found"), 404
            if not daoU.verifyUserworksWid(uid, oldTransaction['wid']):
                return jsonify(Error = "User Does Not Work in Warehouse or Doesn't Exist"), 404
            attributes = dao.getInAttributes(oldTransaction['pid'], oldTransaction['wid'])
            if not attributes:
                    return jsonify(Error = "Attributes Not Found"), 404
            wbudget, rstock, rcapacity, pprice = attributes[0][0], attributes[0][1], attributes[0][2], attributes[0][3]
            total = (float(qty)*pprice)
            partsToGive = abs(qty - oldTransaction['qty'])
            moneyToGive = abs(oldTransaction['total'] - total)
            if qty < oldTransaction['qty']: #When the new quantity of parts is less than the original (Give back parts to supplies, give money back to warehouse)
                if rstock <= qty:
                    return jsonify(Error = "Rack Not Have Enough Parts"), 400
                dao.updateWBudgetSub(moneyToGive, oldTransaction['wid'])
                daoR.updateRackStock(partsToGive, oldTransaction['rid'], 'subtract')
                Supplies_Dao().updateStock(oldTransaction['sid'], oldTransaction['pid'], partsToGive, 'sum')
                date = dao.updateIncoming(oldTransaction['tid'], qty, date, total)
                result = self.buildAttr_tran(oldTransaction['inid'], oldTransaction['sid'], oldTransaction['rid'], oldTransaction['tid'], uid, oldTransaction['wid'], oldTransaction['pid'], qty, float(qty)*pprice, date, 'incoming')
                return jsonify(Transanction = result), 200
            elif qty > oldTransaction['qty']: #When the new quantity of parts is more than the original (Take parts from supplies, take money from warehouse)
                if Supplies_Dao().getStock(oldTransaction['sid'], oldTransaction['pid']) <= qty:
                    Supplies_Dao().updateStock(oldTransaction['sid'], oldTransaction['pid'], 100, 'sum') 
                if rstock + qty + oldTransaction['qty'] > rcapacity:
                    return jsonify(Error = "Rack Doesn't have Space Left"), 400
                if wbudget < total:
                    return jsonify(Error = "Warehouse Doesn't Have Enough Budget"), 400
                dao.updateWBudgetSub((-moneyToGive), oldTransaction['wid'])
                daoR.updateRackStock(partsToGive, oldTransaction['rid'], 'sum')
                Supplies_Dao().updateStock(oldTransaction['sid'], oldTransaction['pid'], partsToGive, 'subtract')
                date = dao.updateIncoming(oldTransaction['tid'], qty, date, total)
                result = self.buildAttr_tran(oldTransaction['inid'], oldTransaction['sid'], oldTransaction['rid'], oldTransaction['tid'], uid, oldTransaction['wid'], oldTransaction['pid'], qty, float(qty)*pprice, date, 'incoming')
                return jsonify(Transanction = result), 200
            else: #Only change the date
                date = dao.updateIncoming(oldTransaction['tid'], qty, date, total)
                result = self.buildAttr_tran(oldTransaction['inid'], oldTransaction['sid'], oldTransaction['rid'], oldTransaction['tid'], uid, oldTransaction['wid'], oldTransaction['pid'], qty, float(qty)*pprice, date, 'incoming')
                return jsonify(Transanction = result), 200