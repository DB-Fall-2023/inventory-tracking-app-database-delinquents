from flask import jsonify
from dao.customer import Customer_Dao


class Customer_Handler:
    def maptodict(self, t):
        result = {'id': t[0], 'name': t[1], 'lastname': t[2],
                  'phone': t[3], 'city': t[4], 'country': t[5]}
        return result

    def build_customer_attributes(self, cid, name, lastname, phone, city, country):
        result = {'cid': cid, 'cname': name, 'clastname': lastname,
                  'cphone': phone, 'ccity': city, 'ccountry': country}
        return result

    def getAllcustomer(self):
        dao = Customer_Dao()
        tuples = dao.getAllcustomer()
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(result)

    def insertCustomer(self, data):
        name = data['Name']
        lastname = data['LastName']
        phone = data['Phone']
        city = data['City']
        country = data['Country']
        if name and lastname and phone and city and country:
            dao = Customer_Dao()
            cid = dao.insertCustomer(name, lastname, phone, city, country)
            result = self.build_customer_attributes(cid, name, lastname, phone, city, country)
            return jsonify(result), 201
        else:
            return jsonify("Unexpected attribute values."), 400

    def searchbyid(self, cid):
        dao = Customer_Dao()
        result = dao.searchbyid(cid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def updatebyid(self, cid, data):
        name = data['Name']
        lastname = data['LastName']
        phone = data['Phone']
        city = data['City']
        country = data['Country']
        if cid and name and lastname and phone and city and country:
            dao = Customer_Dao()
            flag, customer= dao.updatebyid(cid, name, lastname, phone, city, country)
            if flag:
                return jsonify(self.maptodict(dao.searchbyid(cid))), 200
            else:
                return jsonify("Not found"), 201
        else:
            return jsonify("Unexpected attribute values."), 400
