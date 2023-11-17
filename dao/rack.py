from config.dbconfig import pg_config
import psycopg2


class Rack_Dao:
    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getallracks(self):
        cursor = self.conn.cursor()
        result = []
        query = "select * from racks"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def insertrack(self, capacity, stock, pid, wid):
        cursor = self.conn.cursor()
        query = "insert into racks(rcapacity, rstock, pid, wid) values (%s, %s, %s, %s) returning rid"
        cursor.execute(query, (capacity, stock, pid, wid,))
        rid = cursor.fetchone()[0]
        self.conn.commit()
        return rid

    def searchbyid(self, rid):
        cursor = self.conn.cursor()
        query = "select * from racks where rid = %s"
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        return result

    def updatebyid(self, rid, capacity, stock):
        cursor = self.conn.cursor()
        query = "update racks set rcapacity = %s, rstock = %s where rid = %s"
        cursor.execute(query, (capacity, stock, rid,))
        count = cursor.rowcount
        self.conn.commit()
        return count
    
    def searchrackbywidandpid(self, wid, pid):
        cursor = self.conn.cursor()
        query = "select r.rid from racks as r join warehouses as w on r.wid = w.wid join parts as p on r.pid = p.pid where p.pid = %s and w.wid = %s"
        cursor.execute(query, (pid, wid,))
        result = cursor.fetchone()
        return result
    
    def updateRackStock(self, qty, rid):
        cursor = self.conn.cursor()
        query = "update racks set  rstock = rstock + %s where rid = %s"
        cursor.execute(query, (qty, rid,))
        self.conn.commit()

