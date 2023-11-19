from flask import jsonify
from dao.transaction import Transaction_Dao

class Transaction_Handler:
    def maptodict(self, t):
        result = {'id': t[0], 'total': t[1], 'date': t[2], 'qty': t[3]}
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
