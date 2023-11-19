from flask import jsonify
from dao.supplies import Supplies_Dao
from dao.part import Part_Dao
from dao.supplier import Supplier_Dao

class Supplies_Handler():

    def maptodict(self, t):
        result = {'sid': t[0], 'pid': t[1], 'stock': t[2]}
        return result

    def getallsupplies(self):
        dao = Supplies_Dao()
        tuples = dao.getallsupplies()
        result = []
        for t in tuples:
            result.append(self.maptodict(t))
        return jsonify(result)

    def insertsupplies(self, data):
        sid = data['sid']
        pid = data['pid']
        stock = data['stock']
        stock = int(stock)
        if sid and pid and stock >= 0:
            dao, daos, daop = Supplies_Dao(), Supplier_Dao(), Part_Dao()
            if not daos.searchbyid(sid):
                return jsonify(Error="Supplier Not Found"), 404
            if not daop.searchbyid(pid):
                return jsonify(Error="Parts Not Found"), 404
            if dao.searchbysidandpid(pid, sid):
                return jsonify(Error="This Supplies Exist"), 400
            dao.insertSupplies(pid, sid, stock)
            return jsonify(Supplies= self.maptodict([sid, pid, stock])), 200
        else:
            return jsonify(Error="Bad Attributes given"), 400
        
    def updatebysidandpid(self, data):
        sid = data['sid']
        pid = data['pid']
        stock = data['stock']
        stock = int(stock)
        if sid and pid and stock >= 0:
            dao = Supplies_Dao()
            if not dao.searchbysidandpid(pid, sid):
                return jsonify("Not Found"), 404
            result = dao.updatebysidandpid(pid, sid, stock)
            if result:
                return jsonify(data), 200
        else:
            return jsonify(Error="Bad Attributes given"), 400

    def deletebysidandpid(self, data):
        sid = data['sid']
        pid = data['pid']
        dao = Supplies_Dao()
        if not dao.searchbysidandpid(pid, sid):
            return jsonify("Not Found"), 404
        result = dao.deletebysidandpid(pid, sid)
        return jsonify("OK"), 200