from flask import jsonify
from dao.localstatistics import LSDAO
from dao.intran import inTranDAO
from dao.outtran import outtranDAO
from dao.part import Part_Dao
from dao.supplier import Supplier_Dao
from dao.part import Part_Dao
from dao.customer import Customer_Dao
from dao.warehouse import Warehouse_Dao
from dao.user import User_Dao
from dao.rack import Rack_Dao
from dao.transactions import Transaction_Dao

class outtranHandler():

    def buildAttr_tran(self, outid, cid, tid, uid, wid, pid, qty, inttotal, date, typ):
        result = {}
        result['tid'] = tid
        result['outid'] = outid
        result['cid'] = cid
        result['pid'] = pid
        result['wid'] = wid
        result['uid'] = uid
        result['type'] = typ
        result['inttotal'] = inttotal
        result['intqty'] = qty
        result['intdate'] = date
        return result

    def maptodict(self, it):
        result = {'tid': it[0],
                  'outid': it[1],
                  'cid': it[2],
                  'uid': it[3],
                  'wid': it[4],
                  'pid': it[5],
                  'date': it[6],
                  'qty': it[7],
                  'total': it[8],
                  'type': it[9]}
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
                            dao.updateWBudgetSub(inttotal, wid)
                            daoR.updateRackStock(qty, rid)
                            return jsonify(Transaction = result), 200
                        else:
                            return jsonify(Error="Rack doesnt have enough space"), 400
                    else:
                        return jsonify(Error="Warehouse not having enough budget"), 400

    def getIncomingbyid(self, inid):
        dao = inTranDAO()
        result = dao.searchbyid(inid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def getAllOutTran(self):
        dao = outtranDAO()
        results = dao.searchAll()
        if results:
            result = []
            for row in results:
                result.append(self.maptodict(row))
            return jsonify(Outgoings=result)
        else:
            return jsonify(Error="Transactions Not Found"), 404

    def updateOutgoingbyid(self, outid, data):
        if len(data) != 3:
            return jsonify(Error = "Malformed post request"), 400
        qty = data['qty']
        date = data['date:MM/DD/YYYY']
        uid = data['uid']
        daoU, daoP, daoW, daoS, daoR, daoT  = User_Dao(), Part_Dao(), Warehouse_Dao(), Supplier_Dao(), Rack_Dao(), Transaction_Dao()
        dao = outtranDAO()
        if qty > 0 and date and uid:
            print(dao.searchbyid(outid))
            oldTransaction = self.maptodict(dao.searchbyid(outid))

            if not oldTransaction:
                return jsonify(Error = "Transaction Not Found"), 404
            if not daoU.verifyUserworksWid(uid, oldTransaction['wid']):
                return jsonify(Error = "User Does Not Work in Warehouse or Doesn't Exist"), 404
            attributes = dao.getOutAttributes(oldTransaction['pid'], oldTransaction['wid'])
            if not attributes:
                    return jsonify(Error = "Attributes Not Found"), 404
            wbudget, rstock, rcapacity, pprice = attributes[0][0], attributes[0][1], attributes[0][2], attributes[0][3]
            total = (float(qty)*pprice)
            partsToGive = abs(qty - oldTransaction['qty'])
            moneyToGive = abs(oldTransaction['total'] - total)
            if qty > oldTransaction['qty']: #This means the costumer is asking for more parts. (Check if the rack has the parts to give) (Give money to warehouse)
                if rstock < partsToGive:
                    return jsonify(Error= "Rack Not Having Enough Parts"), 400
                date = dao.updateOutgoing(oldTransaction['tid'], qty, date, total)
                daoR.updateRackStock(partsToGive, daoR.searchrackbywidandpid(oldTransaction['wid'], oldTransaction['pid']), 'subtract')
                dao.updateWBudgetSub(moneyToGive, oldTransaction['wid'])
                result = self.buildAttr_tran(oldTransaction['outid'], oldTransaction['cid'], oldTransaction['tid'], uid, oldTransaction['wid'], oldTransaction['pid'], qty, float(qty)*pprice, date, 'incoming')
                return jsonify(Transanction = result), 200
            elif qty < oldTransaction['qty']: #This means the costumer is giving back parts. (Warehouse having enough money to give back) (Give parts to rack)
                if wbudget < moneyToGive:
                    return jsonify(Error= "Warehouse Not Having Enough Money"), 400
                date = dao.updateOutgoing(oldTransaction['tid'], qty, date, total)
                daoR.updateRackStock(partsToGive, daoR.searchrackbywidandpid(oldTransaction['wid'], oldTransaction['pid']), 'sum')
                dao.updateWBudgetSub((-moneyToGive), oldTransaction['wid'])
                result = self.buildAttr_tran(oldTransaction['outid'], oldTransaction['cid'], oldTransaction['tid'], uid, oldTransaction['wid'], oldTransaction['pid'], qty, float(qty)*pprice, date, 'incoming')
                return jsonify(Transanction = result), 200
            else:
                date = dao.updateOutgoing(oldTransaction['tid'], qty, date, total)
                result = self.buildAttr_tran(oldTransaction['outid'], oldTransaction['cid'], oldTransaction['tid'], uid, oldTransaction['wid'], oldTransaction['pid'], qty, float(qty)*pprice, date, 'incoming')
                return jsonify(Transanction = result), 200
        else:
            return jsonify("Unexpected attribute values."), 400
from dao.outtran import OutgoingDAO
from handler.transactions import Transaction_Handler



class OutgoingHandler():

    def build_attr_outtran(self, outtid, tid, cid):
        result = {}
        result['outtid'] = outtid
        result['tid'] = tid
        result['cid'] = cid
        return result

    def insertOutgoing(self, data):
        if len(data) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            uid = data['uid']
            wid = data['wid']
            pid = data['pid']
            cid = data['cid']
            qty = data['qty']
            dao, daoU, daoP, daoW, daoC, daoR, daoT = OutgoingDAO(), User_Dao(), Part_Dao(), Warehouse_Dao(), Customer_Dao(), Rack_Dao(), Transaction_Dao()
            if uid and wid and pid and cid and qty:
                if not daoU.verifyUserworksWid(uid, wid):
                    return jsonify(Error="User or Warehouse Not Found"), 404
                if not daoP.searchbyid(pid):
                    return jsonify(Error="Part Not Found"), 404
                if not daoC.searchbyid(cid):
                    return jsonify(Error="Customer Not Found"), 404
                rid = daoR.searchrackbywidandpid(wid, pid)[0]
                if not rid:
                    return jsonify(Error="Rack Not Found"), 404
                attr = dao.getOutgoingAttr(rid, wid)
                if attr:
                    wbudget, rstock, pprice, wsellingmult = attr[0], attr[1], attr[2], attr[3]
                    qty = float(data['qty'])
                    if qty < 1:
                        return jsonify(Error="Qty lower than 1"), 400
                    if qty > rstock:
                        return jsonify(Error="Rack does not have enough Parts"), 400
                    total = qty * pprice + qty * pprice * wsellingmult
                    tid, date = daoT.insertTransaction(uid, wid, pid, int(qty), total, 'outgoing')
                    trans = Transaction_Handler().build_attr_tran(tid, uid, wid, pid, date, qty, total, 'outgoing')
                    outtid = dao.insertOutgoing(tid, cid)
                    outtran = self.build_attr_outtran(outtid,tid,cid)
                    dao.updateWBudget(total, wid)
                    daoR.updateRackStock(qty, rid, "subtract")
                    return jsonify(Outgoing=outtran, Transaction=trans), 200
            else:
                return jsonify(Error="Unexpected attributes in insert request"), 400