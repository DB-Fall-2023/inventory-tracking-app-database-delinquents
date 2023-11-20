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

    def getOutgoingAttr(self, rid, wid):
        cursor = self.conn.cursor()
        query = "select wbudget, rstock, pprice, wsellingmult from racks natural inner join warehouses natural inner join parts where wid = %s and rid = %s;"
        cursor.execute(query, (wid, rid,))
        result = cursor.fetchone()
        return result

    def insertOutgoing(self, tid, cid):
        cursor = self.conn.cursor()
        query = "insert into outtrans(tid, cid) values (%s, %s) returning outtid;"
        cursor.execute(query, (tid, cid,))
        transaction = cursor.fetchone()
        self.conn.commit()
        return transaction[0]

    def updateWBudgetSub(self, total, wid):
        cursor = self.conn.cursor()
        query = "update warehouses set wbudget = wbudget - %s where wid = %s"
        cursor.execute(query, (total, wid,))
        self.conn.commit()

    def searchbyid(self, outid):
        cursor = self.conn.cursor()
        query = "select tid, outtid, cid, uid, wid, pid, date, qty, total, type from outtrans as ot natural inner join transactions as t where ot.outtid = %s"
        cursor.execute(query, (outid,))
        result = cursor.fetchone()
        return result

    def searchAll(self):
        cursor = self.conn.cursor()
        query = "select tid, outtid, cid, uid, wid, pid, date, qty, total, type from outtrans natural inner join transactions"
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
    def updateWBudget(self, total, wid):
        cursor = self.conn.cursor()
        query = "update warehouses set wbudget = wbudget + %s where wid = %s"
        cursor.execute(query, (total, wid,))
        self.conn.commit()
        return wid