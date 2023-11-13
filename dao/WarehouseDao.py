import psycopg2
import urllib.parse as urlparse
import os


class WarehouseDao:
    def __init__(self):
        url = urlparse.urlparse(os.environ.get(
                                    'postgres://vbcewagvstcdvk'
                                    ':3a15bce8eee8d652287e34b0b4f3fe6321980a5e397f2d7078dc0c48ae988a84@ec2-44-220-7'
                                    '-157.compute-1.amazonaws.com:5432/d75kdlr9cl6ro8'))
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def get_all_warehouses(self):
        cursor = self.conn.cursor()
        result = []
        query = "SELECT * FROM warehouses"
        cursor.execute(query)
        for row in cursor:
            print(row)
            result.append(row)
        return result

    # top warehouse that delivers the most exchanges
    # def get_top_warehouse(self):
    #     cursor = self.conn.cursor()
    #     result = []
