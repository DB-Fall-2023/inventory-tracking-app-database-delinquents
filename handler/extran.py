from flask import jsonify
from dao.extran import ExchangeDAO
from dao.part import Part_Dao
from dao.user import User_Dao
from dao.rack import Rack_Dao
from dao.transactions import Transaction_Dao
from handler.transactions import Transaction_Handler

class ExtranHandler():

    def build_attr_extran(self, exid, sendertid, receivertid):
        result = {}
        result['exid'] = exid
        result['sendertid'] = sendertid
        result['receivertid'] = receivertid
        return result

    def build_exchange_attr(self, row):
        result = {}
        result['tid'] = row[0]
        result['uid'] = row[1]
        result['wid'] = row[2]
        result['pid'] = row[3]
        result['date'] = row[4]
        result['qty'] = row[5]
        result['total'] = row[6]
        result['type'] = row[7]
        return result

    def getAllExchange(self):
        dao = ExchangeDAO()
        transactions = dao.getAllExchange()
        exchange=[]
        for t in transactions:
            transaction=self.build_exchange_attr(t)
            exchange.append(transaction)
        return jsonify(Exchange=exchange)

    def getExchangeById(self, extid):
        dao = ExchangeDAO()
        transactions = dao.getTransactionByExtid(extid)
        if not transactions:
            return jsonify(Error="Exchange Transaction Not Found"), 404
        exchange=[]
        for t in transactions:
            transaction=self.build_exchange_attr(t)
            exchange.append(transaction)
        return jsonify(Exchange=exchange)

    def updateExchangeById(self, extid, data):
        dao, daoR = ExchangeDAO(), Rack_Dao()
        if not dao.getExchangeById(extid):
            return jsonify(Error="Exchange Transaction not found."), 404
        if len(data) != 2:
            return jsonify(Error="Malformed update request"), 400
        date, qty = data['date:MM/DD/YYYY'], data['qty']
        transactions = dao.getTransactionByExtid(extid)
        if not transactions:
            return jsonify(Error="Transactions Not Found."), 404
        if date and qty and qty>0:
            oldQty = transactions[0][5]
            if not oldQty==qty:
                ridsender = daoR.searchrackbywidandpid(transactions[0][2], transactions[0][3])[0]
                rid2receiver = daoR.searchrackbywidandpid(transactions[1][2], transactions[1][3])[0]
                attrSender = dao.getExchangeAttr(ridsender, transactions[0][2])
                attrReceiver = dao.getExchangeAttr(rid2receiver, transactions[1][2])
                if not (attrSender and attrReceiver):
                    return jsonify(Error="Rack Not Found"), 404
                qtyDifference = abs(qty-oldQty)
                rstockSen, rcapacitySen, rstockRec, rcapacityRec = attrSender[0], attrSender[1], attrReceiver[0], attrReceiver[1]
                if qty < oldQty and rstockSen+qty <= rcapacitySen and rstockRec-qty >= 0:
                    daoR.updateRackStock(qtyDifference, ridsender, "sum")
                    daoR.updateRackStock(qtyDifference, rid2receiver, "subtract")
                elif qty > oldQty and rstockSen-qty >= 0 and rstockRec+qty <= rcapacityRec:
                    daoR.updateRackStock(qtyDifference, ridsender, "subtract")
                    daoR.updateRackStock(qtyDifference, rid2receiver, "sum")
                else:
                    return jsonify(Error="New qty Conflicts with the Rack Stock or Capacity of the Sender or Receiver Warehouse"), 400
            trans = dao.updateExchangeById(extid, date, qty)
            sender = self.build_exchange_attr(trans[0])
            receiver = self.build_exchange_attr(trans[1])
            exchange = self.build_attr_extran(extid, sender['tid'], receiver['tid'])
            return jsonify(Exchange=exchange, Transaction1=sender, Transaction2=receiver), 200
        return jsonify(Error="Unexpected attributes in update request"), 400


    def insertExchange(self, data):
        if len(data) != 6:
            return jsonify(Error = "Malformed post request"), 400
        usenderid = data['usenderid']
        ureceiverid = data['ureceiverid']
        wsenderid = data['wsenderid']
        wreceiverid = data['wreceiverid']
        pid = data['pid']
        qty = int(data['qty'])
        daoU, daoP, daoR, daoT  = User_Dao(), Part_Dao(), Rack_Dao(), Transaction_Dao()
        if usenderid and ureceiverid and wsenderid and wreceiverid and pid and qty:
            if wsenderid==wreceiverid or usenderid==ureceiverid:
                return jsonify(Error="Invalid Transaction. Same Warehouse")
            if not (daoU.verifyUserworksWid(usenderid, wsenderid) and daoU.verifyUserworksWid(ureceiverid, wreceiverid)):
                return jsonify(Error="User or Warehouse Not Found"), 404
            if not daoP.searchbyid(pid):
                return jsonify(Error="Part Not Found"), 404
            ridsender = daoR.searchrackbywidandpid(wsenderid, pid)[0]
            rid2receiver = daoR.searchrackbywidandpid(wreceiverid, pid)[0]
            if not (ridsender and rid2receiver):
                return jsonify(Error="Rack Not Found"), 404
            dao = ExchangeDAO()
            attrSender = dao.getExchangeAttr(ridsender, wsenderid)
            attrReceiver = dao.getExchangeAttr(rid2receiver, wreceiverid)
            if attrSender and attrReceiver:
                rstockSen, rstockRec, rcapacityRec = attrSender[0], attrReceiver[0], attrReceiver[1]
                if rstockSen >= qty:
                    if (rcapacityRec-rstockRec) >= qty:
                        tids, datesen = daoT.insertTransaction(usenderid, wsenderid, pid, qty, 0.0, 'exchange-sender')
                        tidr, daterec = daoT.insertTransaction(ureceiverid, wreceiverid, pid, qty, 0.0, 'exchange-receiver')
                        tSen = Transaction_Handler().build_attr_tran(tids, usenderid, wsenderid, pid, datesen, qty, 0.0, 'exchange-sender')
                        tRec = Transaction_Handler().build_attr_tran(tidr, ureceiverid, wreceiverid, pid, daterec, qty, 0.0, 'exchange-receiver')
                        extid = dao.insertExchange(tids, tidr)
                        extran = self.build_attr_extran(extid,tids,tidr)
                        daoR.updateRackStock(qty, ridsender, "subtract")
                        daoR.updateRackStock(qty, rid2receiver, "sum")
                        return jsonify(Transaction1=tSen, Transaction2=tRec, Exchange=extran), 200
                    else:
                        return jsonify(Error="Receiver does not have enough space"), 400
                else:
                    return jsonify(Error="Sender does not have enough stock"), 400
        else:
            return jsonify(Error="Unexpected attributes in insert request"), 400