from flask import jsonify
from dao.warehouse import Warehouse_Dao


class Warehouse_Handler:
    def maptodict(self, t):
        result = {'id': t[0], 'name': t[1], 'country': t[2],
                  'city': t[3], 'budget': t[4], 'sellingmult': t[5]}
        return result

    def build_warehouse_attributes(self, wid, name, country, city, budget, sellingmult):
        result = {'wid': wid, 'wname': name, 'wcountry': country,
                  'wcity': city, 'wbudget': budget, 'wsellingmult': sellingmult}
        return result

    def getallwarehouses(self):
        dao = Warehouse_Dao()
        tuples = dao.getallwarehouses()
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(result)

    def insertwarehouse(self, data):
        name = data['Name']
        country = data['Country']
        city = data['City']
        budget = data['Budget']
        sellingmult = data['SellingMult']
        if name and country and city and budget and sellingmult:
            dao = Warehouse_Dao()
            wid = dao.insertwarehouse(name, country, city, budget, sellingmult)
            result = self.build_warehouse_attributes(wid, name, country, city, budget, sellingmult)
            return jsonify(result), 201
        else:
            return jsonify("Unexpected attribute values."), 400

    def searchbyid(self, wid):
        dao = Warehouse_Dao()
        result = dao.searchbyid(wid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def deletebyid(self, wid):
        dao = Warehouse_Dao()
        if not dao.searchbyid(wid):
            return jsonify("Not Found"), 404
        result = dao.deletebyid(wid)
        if result == "Error":
            return jsonify("Warehouse is referenced"), 400
        return jsonify("OK"), 200

    def updatebyid(self, wid, data):
        name = data['Name']
        country = data['Country']
        city = data['City']
        budget = data['Budget']
        sellingmult = data['SellingMult']
        if wid and name and country and city and budget and sellingmult:
            dao = Warehouse_Dao()
            flag = dao.updatebyid(wid, name, country, city, budget, sellingmult)
            if flag:
                return jsonify(data), 200
            else:
                return jsonify("Not found"), 201
        else:
            return jsonify("Unexpected attribute values."), 400
