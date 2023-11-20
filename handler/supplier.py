from flask import jsonify
from dao.supplier import Supplier_Dao


class Supplier_Handler:
    def maptodict(self, t):
        result = {'id': t[0], 'name': t[1], 'lastname': t[2],
                  'phone': t[3], 'city': t[4], 'country': t[5]}
        return result

    def build_supplier_attributes(self, sid, name, lastname, phone, city, country):
        result = {'sid': sid, 'sname': name, 'slastname': lastname,
                  'sphone': phone, 'scity': city, 'scountry': country}
        return result

    def getallsuppliers(self):
        dao = Supplier_Dao()
        tuples = dao.getallsuppliers()
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(result)

    def insertsupplier(self, data):
        name = data['sname']
        lastname = data['slastname']
        phone = data['sphone']
        city = data['scity']
        country = data['scountry']
        print(name, lastname, phone, city, country)
        if name and lastname and phone and city and country:
            dao = Supplier_Dao()
            sid = dao.insertsupplier(name, lastname, phone, city, country)
            result = self.build_supplier_attributes(sid, name, lastname, phone, city, country)
            return jsonify(result), 201
        else:
            return jsonify("Unexpected attribute values."), 400

    def searchbyid(self, sid):
        dao = Supplier_Dao()
        result = dao.searchbyid(sid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def updatebyid(self, sid, data):
        name = data['Name']
        lastname = data['LastName']
        phone = data['Phone']
        city = data['City']
        country = data['Country']
        if sid and name and lastname and phone and city and country:
            dao = Supplier_Dao()
            flag = dao.updatebyid(sid, name, lastname, phone, city, country)
            if flag:
                return jsonify(data), 200
            else:
                return jsonify("Not found"), 201
        else:
            return jsonify("Unexpected attribute values."), 400

    def deletebyid(self, sid):
        dao = Supplier_Dao()
        if not dao.searchbyid(sid):
            return jsonify("Not Found"), 404
        result = dao.deletebyid(sid)
        if result == "Error":
            return jsonify("Supplier is referenced"), 400
        return jsonify("OK"), 200
