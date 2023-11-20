from config.dbconfig import pg_config
import psycopg2


class OutgoingDAO():

    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)


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

    def updateWBudget(self, total, wid):
        cursor = self.conn.cursor()
        query = "update warehouses set wbudget = wbudget + %s where wid = %s"
        cursor.execute(query, (total, wid,))
        self.conn.commit()
        return wid