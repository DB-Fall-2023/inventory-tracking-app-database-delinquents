from flask import jsonify
from dao.part import Part_Dao


class Part_Handler:
    def maptodict(self, t):
        result = {'id': t[0], 'name': t[1], 'type': t[2], 'price': t[3]}
        return result

    def build_part_attributes(self, pid, name, tipo, price):
        result = {'pid': pid, 'pname': name, 'ptype': tipo, 'pprice': price}
        return result

    def getallparts(self):
        dao = Part_Dao()
        tuples = dao.getallparts()
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(result)

    def insertpart(self, data):
        name = data['Name']
        tipo = data['Type']
        price = data['Price']
        if name and tipo and price:
            dao = Part_Dao()
            pid = dao.insertpart(name, tipo, price)
            result = self.build_part_attributes(pid, name, tipo, price)
            return jsonify(result), 201
        else:
            return jsonify("Unexpected attribute values."), 400

    def searchbyid(self, pid):
        dao = Part_Dao()
        result = dao.searchbyid(pid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def deletebyid(self, pid):
        dao = Part_Dao()
        if not dao.searchbyid(pid):
            return jsonify("Not Found"), 404
        result = dao.deletebyid(pid)
        return jsonify("OK"), 200

    def updatebyid(self, pid, data):
        name = data['Name']
        tipo = data['Type']
        price = data['Price']
        if pid and name and tipo and price:
            dao = Part_Dao()
            flag = dao.updatebyid(pid, name, tipo, price)
            if flag:
                return jsonify(data), 200
            else:
                return jsonify("Not found"), 201
        else:
            return jsonify("Unexpected attribute values."), 400
