from flask import jsonify
from dao.rack import Rack_Dao


class Racket_Handler:
    def maptodict(self, t):
        result = {'id': t[0], 'capacity': t[1], 'stock': t[2]}
        return result

    def build_rack_attributes(self, rid, capacity, stock):
        result = {'rid': rid, 'rcapacity': capacity, 'rstock': stock}
        return result

    def getallracks(self):
        dao = Rack_Dao()
        tuples = dao.getallracks()
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(result)

    def insertrack(self, data):
        capacity = data['Capacity']
        stock = data['Stock']
        if capacity and stock:
            dao = Rack_Dao()
            rid = dao.insertrack(capacity, stock)
            result = self.build_rack_attributes(rid, capacity, stock)
            return jsonify(result), 201
        else:
            return jsonify("Unexpected attribute values."), 400

    def searchbyid(self, rid):
        dao = Rack_Dao()
        result = dao.searchbyid(rid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def updatebyid(self, rid, data):
        capacity = data['Capacity']
        stock = data['Stock']
        if capacity and stock:
            dao = Rack_Dao()
            flag = dao.updatebyid(rid, capacity, stock)
            if flag:
                return jsonify(data), 200
            else:
                return jsonify("Not found"), 201
        else:
            return jsonify("Unexpected attribute values."), 400
