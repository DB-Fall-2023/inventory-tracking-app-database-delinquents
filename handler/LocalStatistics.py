from flask import jsonify
from dao.localstatistics import LSDAO
from dao.user import User_Dao


class LSHandler:

    def build_rack_dic(self, row):
        result = {'rid': row[0], 'rstock': row[1],
                  'pname': row[2], 'ptype': row[3], 'totalprice': row[4]}
        return result

    def build_supplier_dic(self, row):
        result = {'sid': row[0], 'sname': row[1], 'scity': row[2],
                  'scountry': row[3], 'sphone': row[4], 'totalsupplied': row[5]}
        return result

    def build_days_dic(self, row):
        result = {'intdate': row[0], 'totalamount': row[1]}
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
            return jsonify(LeastCost_Days=result)
