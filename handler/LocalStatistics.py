from flask import jsonify
from dao.localstatistics import LSDAO
from dao.user import User_Dao

class LSHandler():

    def build_warehouse_profit(self, warehouses_profit):
        result = []
        for WP in warehouses_profit:
            D = {}
            D['wid'] = WP[0]
            D['wname'] = WP[1]
            D['year'] = WP[2]
            D['costs'] = WP[3]
            D['sales'] = WP[4]
            D['profit'] = WP[5]
            result.append(D)
        return result

    def getWarehouseProfitByYear(self, wid, data):
        if len(data) != 1:
            return jsonify(Error="Malformed post request"), 400
        uid = data['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error="User not works in Warehouse"), 404
        result = dao.getWarehouseProfitByYear(wid)
        return jsonify(WarehouseProfit = self.build_warehouse_profit(result)), 200

    def build_rack_dict_Top5RackUnder25Pct(self, racks):
        result = []
        for R in racks:
            D = {}
            D['rid'] = R[0]
            D['wid'] = R[1]
            D['pid'] = R[2]
            D['rcapacity'] = R[3]
            D['rstock'] = R[4]
            D['qtypct'] = R[5]
            result.append(D)
        return result

    def getTop5RackUnder25Pct(self, wid, data):
        if len(data) != 1:
            return jsonify(Error="Malformed post request"), 400
        uid = data['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error="User not works in Warehouse"), 404
        top5Racks = dao.getTop5RackUnder25Pct(wid)
        return jsonify(Top5RackUnder25Pct = self.build_rack_dict_Top5RackUnder25Pct(top5Racks)), 200

    def build_rack_dict_Bottom3PartsByType(self, racks):
        result = []
        for R in racks:
            D = {}
            D['pid'] = R[0]
            D['pname'] = R[1]
            D['ptype'] = R[2]
            D['pprice'] = R[3]
            result.append(D)
        return result

    def getBottom3PartsByType(self, wid, data):
        if len(data) != 1:
            return jsonify(Error="Malformed post request"), 400
        uid = data['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error="User not works in Warehouse"), 404
        bottom3Parts = dao.getBottom3PartsByType(wid)
        return jsonify(Bottom3PartsByType = self.build_rack_dict_Bottom3PartsByType(bottom3Parts)), 200

    def build_rack_dic(self, row):
        result = {'rid': row[0], 'rstock': row[1],
                  'pname': row[2], 'ptype': row[3], 'totalprice': row[4]}
        return result

    def build_supplier_dic(self, row):
        result = {'sid': row[0], 'sname': row[1], 'scity': row[2],
                  'scountry': row[3], 'sphone': row[4], 'totalsupplied': row[5]}
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
            return jsonify(Error="User not works in Warehouse"), 404
        racks = dao.getFiveExpensiveRacksbyID(wid)
        if not racks:
            return jsonify(Error="Rack Not Found"), 404
        else:
            result = []
            for r in racks:
                rack = self.build_rack_dic(r)
                result.append(rack)
            return jsonify(Racks=result)

    def getTopSupplierbyID(self, wid, form):
        uid = form['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error="User not works in Warehouse"), 404
        supplier = dao.getTopSupplierbyID(wid)
        if not supplier:
            return jsonify(Error="Supplier Not Found"), 404
        else:
            result = []
            for s in supplier:
                supp = self.build_supplier_dic(s)
                result.append(supp)
            return jsonify(Suppliers=result)

    def getDaysLeastcostbyID(self, wid, form):
        uid = form['uid']
        dao = LSDAO()
        daoU = User_Dao()
        if not daoU.verifyUserworksWid(uid, wid):
            return jsonify(Error="User not works in Warehouse"), 404
        days = dao.getDaysLeastcostbyID(wid)
        if not days:
            return jsonify(Error="Supplier Not Found"), 404
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

