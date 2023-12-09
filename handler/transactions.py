from flask import jsonify
from dao.transactions import Transaction_Dao
from dao.warehouse import Warehouse_Dao


class Transaction_Handler:
    def maptodict(self, t):
        result = {'tid': t[0], 'uid': t[1], 'wid': t[2], 'pid': t[3],
                  'date': t[4], 'qty': t[5], 'total': t[6], 'type': t[7]}
        return result

    def build_attr_tran(self, tid, uid, wid, pid, date, qty, total, type):
        result = {'tid': tid, 'uid': uid, 'wid': wid, 'pid': pid, 'date': date, 'qty': qty, 'total': total,
                  'type': type}
        return result

    def getalltransactions(self):
        dao = Transaction_Dao()
        tuples = dao.getalltransactions()
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(result)

    def searchbyid(self, pid):
        pass

    def inserttransaction(self, data):
        pass

    def getalltransactionswarehouse(self, wid):
        dao = Transaction_Dao()
        tuples = dao.getalltransactionswarehouse(wid)
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(transactions=result)
