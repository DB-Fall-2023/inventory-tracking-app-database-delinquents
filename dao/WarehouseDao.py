import psycopg2
from dbconfig import pg_config


class WarehouseDao:
    def __init__(self):
        connection_url = ("host=%s dbname=%s user=%s password=%s" %
                          (pg_config['host'],
                           pg_config['dbname'],
                           pg_config['user'],
                           pg_config['password']))
        self.conn = psycopg2.connect(connection_url)

    def get_all_warehouses(self):
        cursor = self.conn.cursor()
        result = []
        query = "SELECT * FROM warehouses"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def get_top5_deliverers(self):
        cursor = self.conn.cursor()
        result = []
        query = ('''
                SELECT DISTINCT wid, wname, wcountry, wcity, wbudget, wsellingmult, total_deliveries
                FROM warehouses
                NATURAL INNER JOIN (SELECT wid, count(wid) as total_deliveries
                                    FROM transactions
                                    WHERE type = 'sender'
                                    GROUP BY wid
                                    ORDER BY total_deliveries desc
                                    ) as delivers
                LIMIT 5;
                ''')
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def get_top3_least_outgoing(self):
        cursor = self.conn.cursor()
        result = []
        query = ('''
                        SELECT DISTINCT wid, wname, wcountry, wcity, wbudget, wsellingmult, outgoing_count
                        FROM warehouses
                        NATURAL INNER JOIN (SELECT wID, count(wID) as outgoing_count
                                            FROM transactions
                                            WHERE type = 'outgoing'
                                            GROUP BY wID
                                            ) as outCount
                        ORDER BY outgoing_count
                        LIMIT 3;
                ''')
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def get_top3_cities_transactions(self):
        cursor = self.conn.cursor()
        result = []
        query = ('''
                        SELECT DISTINCT wcity, count(wcity) as total_transactions
                        FROM transactions
                        NATURAL INNER JOIN warehouses
                        GROUP BY wcity
                        ORDER BY total_transactions desc
                        LIMIT 3
                ''')
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result