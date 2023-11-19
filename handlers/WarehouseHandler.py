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
    def build_wdeliverers_dict(self, row):
        result = {}
        result['wid'] = row[0]
        result['wname'] = row[1]
        result['wcountry'] = row[2]
        result['wcity'] = row[3]
        result['wbudget'] = row[4]
        result['wsellingmult'] = row[5]
        result['total_deliveries'] = row[6]
        return result

    def build_woutgoing_dict(self, row):
        result = {}
        result['wid'] = row[0]
        result['wname'] = row[1]
        result['wcountry'] = row[2]
        result['wcity'] = row[3]
        result['wbudget'] = row[4]
        result['wsellingmult'] = row[5]
        result['outgoing_transactions'] = row[6]
        return result

    def build_top_cities_dict(self, row):
        result = {}
        result['wcity'] = row[0]
        result['total_transactions'] = row[1]
        return result
    def get_all_warehouses(self):
        dao = WarehouseDao()
        warehouse_list = dao.get_all_warehouses()
        result = []
        for row in warehouse_list:
            result.append(self.build_warehouse_dict(row))
        return jsonify(result)

    def get_top_deliverers(self):
        dao = WarehouseDao()
        warehouse_list = dao.get_top5_deliverers()
        result = []
        for row in warehouse_list:
            result.append(self.build_wdeliverers_dict(row))
        return jsonify(result)

    def get_least_outgoing_warehouses(self):
        dao = WarehouseDao()
        warehouse_list = dao.get_top3_least_outgoing()
        result = []
        for row in warehouse_list:
            result.append(self.build_woutgoing_dict(row))
        return jsonify(result)

    def get_top3_cities_transactions(self):
        dao = WarehouseDao()
        warehouse_list = dao.get_top3_cities_transactions()
        result = []
        for row in warehouse_list:
            result.append(self.build_top_cities_dict(row))
        return jsonify(result)




