from flask import jsonify
from dao.user import User_Dao
from dao.warehouse import Warehouse_Dao


class User_Handler:
    def maptodict(self, t):
        result = {'id': t[0], 'name': t[1], 'lastname': t[2], 'email': t[3],
                  'password': t[4], 'phone': t[5], 'country': t[6], 'city': t[7], 'wid': t[8]}
        return result

    def build_user_attributes(self, uid, name, lastname, email, password, phone, country, city, wid):
        result = {'uid': uid, 'uname': name, 'ulastname': lastname, 'uemail': email,
                  'upassword': password, 'uphone': phone, 'ucountry': country, 'ucity': city, 'wid': wid}
        return result

    def getallusers(self):
        dao = User_Dao()
        tuples = dao.getallusers()
        result = []
        for e in tuples:
            result.append(self.maptodict(e))
        return jsonify(result)

    def insertuser(self, data):
        if len(data) != 8:
            return jsonify(Error = "Malformed post request"), 400
        name = data['uname']
        lastname = data['ulastname']
        email = data['uemail']
        password = data['upassword']
        phone = data['uphone']
        country = data['ucountry']
        city = data['ucity']
        wid = data['wid']
        daow = Warehouse_Dao()
        if not daow.searchbyid(wid):
            return jsonify(Error="Warehouse Not Found"), 404
        if name and lastname and email and password and phone and country and city:
            dao = User_Dao()
            uid = dao.insertuser(name, lastname, email, password, phone, country, city, wid)
            result = self.build_user_attributes(uid, name, lastname, email, password, phone, country, city, wid)
            return jsonify(result), 201
        else:
            return jsonify("Unexpected attribute values."), 400

    def searchbyid(self, uid):
        dao = User_Dao()
        result = dao.searchbyid(uid)
        if result:
            return jsonify(self.maptodict(result))
        else:
            return jsonify("Not Found"), 404

    def deletebyid(self, uid):
        dao = User_Dao()
        if not dao.searchbyid(uid):
            return jsonify("Not Found"), 404
        result = dao.deletebyid(uid)
        if result == "Error":
            return jsonify("User is referenced"), 400
        return jsonify("OK"), 200

    def updatebyid(self, uid, data):
        if len(data) != 7:
            return jsonify(Error = "Malformed post request"), 400
        name = data['Name']
        lastname = data['LastName']
        email = data['Email']
        password = data['Password']
        phone = data['Phone']
        country = data['Country']
        city = data['City']
        if (uid or uid==0) and name and lastname and email and password and phone and country and city:
            dao = User_Dao()
            flag = dao.updatebyid(uid, name, lastname, email, password, phone, country, city)
            if flag:
                return jsonify(data), 200
            else:
                return jsonify("Not found"), 201
        else:
            return jsonify("Unexpected attribute values."), 400
        

    def verifyUser(self, data):
        wid = data['wid']
        uid = data['uid']
        if User_Dao().verifyUserworksWid(uid, wid):
            return jsonify(True)
        else:
            return jsonify(False)