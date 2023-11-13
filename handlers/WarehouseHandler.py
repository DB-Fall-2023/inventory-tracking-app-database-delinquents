from dao.WarehouseDao import WarehouseDao
from flask import jsonify

class WarehouseHandler:
    def build_warehouse_dict(self, row):
        result = {}
        result['wid'] = row[0]
        result['wname'] = row[1]
        result['wcountry'] = row[2]
        result['wcity'] = row[3]
        result['wbudget'] = row[4]
        result['wsellingmult'] = row[5]
        return result

    def get_all_warehouses(self):
        dao = WarehouseDao()
        warehouse_list = dao.get_all_warehouses()
        result = []
        for row in warehouse_list:
            result.append(self.build_warehouse_dict(row))
        return jsonify(result)


