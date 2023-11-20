from flask import jsonify
from dao.part import Part_Dao
from dao.customer import Customer_Dao
from dao.warehouse import Warehouse_Dao
from dao.user import User_Dao
from dao.rack import Rack_Dao
from dao.transactions import Transaction_Dao
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