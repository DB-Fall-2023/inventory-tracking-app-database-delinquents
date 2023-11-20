from config.dbconfig import pg_config
import psycopg2


class Warehouse_Dao:
    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getallwarehouses(self):
        cursor = self.conn.cursor()
        result = []
        query = "select * from warehouses"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def insertwarehouse(self, name, country, city, budget, sellingmult):
        cursor = self.conn.cursor()
        query = ("insert into warehouses(wname, wcountry, wcity, wbudget, wsellingmult) "
                 "values (%s, %s, %s, %s, %s) returning wid")
        cursor.execute(query, (name, country, city, budget, sellingmult,))
        wid = cursor.fetchone()[0]
        self.conn.commit()
        return wid

    def searchbyid(self, wid):
        cursor = self.conn.cursor()
        query = "select * from warehouses where wid = %s"
        cursor.execute(query, (wid,))
        result = cursor.fetchone()
        return result

    def deletebyid(self, wid):
        cursor = self.conn.cursor()
        query = "delete from warehouses where wid = %s"
        try:
            cursor.execute(query, (wid,))
            count = cursor.rowcount
            self.conn.commit()
            return count
        except:
            return "Error"

    def updatebyid(self, wid, name, country, city, budget, sellingmult):
        cursor = self.conn.cursor()
        query = ("update warehouses set wname = %s, wcountry = %s, wcity = %s, wbudget = %s, "
                 "wsellingmult = %s where wid = %s")
        cursor.execute(query, (name, country, city, budget, sellingmult, wid,))
        count = cursor.rowcount
        self.conn.commit()
        return count
