from flask import jsonify
from dao.globalstatistics import GlobalStatisticsDAO

class GlobalStatisticsHandler:

    def build_warehouse_dic(cls, row):
        result = {}
        result['wid'] = row[0]
        result['rack_count'] = row[1]
        return result

    def getTopWarehousesMostRacks(self):
        dao = GlobalStatisticsDAO()
        top_warehouses = dao.getTopWarehousesMostRacks()

        if not top_warehouses:
            return jsonify(Error="No warehouses found with most racks"), 404

        else:
            result = []
            for warehouse in top_warehouses:
                warehouse_info = self.build_warehouse_dic(warehouse)
                result.append(warehouse_info)

            return jsonify(TopWarehouses=result)

    def getTopWarehousesMostIncoming(self):
        dao = GlobalStatisticsDAO()
        top_warehouses = dao.getTopWarehousesMostIncoming()

        if not top_warehouses:
            return jsonify(Error="No warehouses found with most incoming transactions"), 404

        else:
            result = []
            for warehouse in top_warehouses:
                warehouse_info = self.build_warehouse_dic(warehouse)
                result.append(warehouse_info)

            return jsonify(TopWarehouses=result)