from config.dbconfig import pg_config
import psycopg2

class inTranDAO():

    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getInAttributes(self, pid, wid):
        cursor = self.conn.cursor()
        query = """select w.wbudget, r.rstock, r.rcapacity, p.pprice
                    from parts as p join racks r on r.pid = p.pid join warehouses as w on r.wid = w.wid
                    where w.wid = %s and p.pid = %s
                """
        cursor.execute(query, (wid, pid,))
        result = cursor.fetchall()
        return result
    
    def insertINT(self, tid, sid, rid):
        cursor = self.conn.cursor()
        query = "insert into intrans(rid, sid, tid) values (%s, %s, %s) returning inid;"
        cursor.execute(query, (rid, sid, tid,))
        transaction = cursor.fetchone()
        self.conn.commit()
        return transaction[0]
    
    def updateWBudgetSub(self, inttotal, wid):
        cursor = self.conn.cursor()
        query = "update warehouses set wbudget = wbudget + %s where wid = %s"
        cursor.execute(query, (inttotal, wid,))
        self.conn.commit()

    def searchbyid(self, inid):
        cursor = self.conn.cursor()
        query = "select * from intrans as it natural inner join transactions as t where it.inid = %s"
        cursor.execute(query, (inid,))
        result = cursor.fetchone()
        return result
    
    def searchAll(self):
        cursor = self.conn.cursor()
        query = "select * from intrans as it natural inner join transactions as t"
        cursor.execute(query)
        result = cursor.fetchall()
        return result