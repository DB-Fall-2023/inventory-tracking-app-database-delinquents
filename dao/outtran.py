from config.dbconfig import pg_config
import psycopg2


class outtranDAO():

    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getOutAttributes(self, pid, wid):
        cursor = self.conn.cursor()
        query = """select w.wbudget, r.rstock, r.rcapacity, p.pprice
                    from parts as p join racks r on r.pid = p.pid join warehouses as w on r.wid = w.wid
                    where w.wid = %s and p.pid = %s
                """
        cursor.execute(query, (wid, pid,))
        result = cursor.fetchall()
        return result

    def insertOuttran(self, tid, sid, rid):
        cursor = self.conn.cursor()
        query = "insert into intrans(rid, sid, tid) values (%s, %s, %s) returning inid;"
        cursor.execute(query, (rid, sid, tid,))
        transaction = cursor.fetchone()
        self.conn.commit()
        return transaction[0]

    def updateWBudgetSub(self, inttotal, wid):
        cursor = self.conn.cursor()
        query = "update warehouses set wbudget = wbudget - %s where wid = %s"
        cursor.execute(query, (inttotal, wid,))
        self.conn.commit()

    def searchbyid(self, outid):
        cursor = self.conn.cursor()
        query = "select * from outtrans as ot natural inner join transactions as t where ot.outtid = %s"
        cursor.execute(query, (outid,))
        result = cursor.fetchone()
        return result

    def searchAll(self):
        cursor = self.conn.cursor()
        query = "select * from outtrans natural inner join transactions"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    def updateOutgoing(self, tid, qty, date, total):
        cursor = self.conn.cursor()
        query = """update transactions set date = TO_DATE(%s,'MM/DD/YYYY'), qty = %s, total = %s
                where tid = %s
                returning to_char(date, 'MM/DD/YYYY');"""
        cursor.execute(query, (date, qty, total, tid,))
        self.conn.commit()
        return cursor.fetchone()