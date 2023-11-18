from flask import jsonify
from dao.localstatistics import LSDAO
from dao.user import User_Dao

class LSHandler():

    def build_rack_dic(cls, row):
        result = {}
        result['rid'] = row[0]
        result['rstock'] = row[1]
        result['pname'] = row[2]
        result['ptype'] = row[3]
        result['totalprice'] = row[4]
        return result
    
    def build_supplier_dic(cls, row):
        result = {}
        result['sid'] = row[0]
        result['sname'] = row[1]
        result['scity'] = row[2]
        result['scountry'] = row[3]
        result['sphone'] = row[4]
        result['totalsupplied'] = row[5]
        return result
    
    def build_days_dic(cls, row):
        result = {}
        result['intdate'] = row[0]
        result['totalamount'] = row[1]
        return result      
    
            
    def getFiveExpensiveRacksbyID(self, wid, form):
        uid = form['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error = "User not works in Warehouse"), 404
        racks = dao.getFiveExpensiveRacksbyID(wid)
        if not racks:
            return jsonify(Error = "Rack Not Found"), 404
        else:
            result = []
            for r in racks:
                rack = self.build_rack_dic(r)
                result.append(rack)
            return jsonify(Racks = result)        


    def getTopSupplierbyID(self, wid, form):
        uid = form['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error = "User not works in Warehouse"), 404
        supplier = dao.getTopSupplierbyID(wid)
        if not supplier:
            return jsonify(Error = "Supplier Not Found"), 404
        else:
            result = []
            for s in supplier:
                supp = self.build_supplier_dic(s)
                result.append(supp)
            return jsonify(Suppliers = result)
        

    def getDaysLeastcostbyID(self, wid, form):
        uid = form['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error = "User not works in Warehouse"), 404
        days = dao.getDaysLeastcostbyID(wid)
        if not days:
            return jsonify(Error = "Supplier Not Found"), 404
        else:
            result = []
            for d in days:
                day = self.build_days_dic(d)
                result.append(day)
            return jsonify(LeastCost_Days = result)


    def build_user_dic(self, user):
        result = {}

        return result

    def getTopUsersMostExchangesbyID(self, wid, form):
        uid = form['uid']
        dao = LSDAO()
        daoU = User_Dao()

        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error="User not works in Warehouse"), 404
        top_users = dao.getTopUsersMostExchanges(wid)
        if not top_users:
            return jsonify(Error="No users found with most exchanges"), 404
        else:
            result = []
            for user in top_users:
                user_info = self.build_user_dic(user)
                result.append(user_info)

            return jsonify(TopUsers=result)

