from config.dbconfig import pg_config
import psycopg2


class ExchangeDAO:

    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getAllExchange(self):
        cursor = self.conn.cursor()
        query = """select tid, uid, wid, pid, date, qty, total, type from transactions where type='exchange-sender'
                   or type='exchange-receiver' order by tid;"""
        cursor.execute(query)
        transactions = cursor.fetchall()
        return transactions

    def getExchangeById(self, extid):
        cursor = self.conn.cursor()
        query = """select extid, sendertid, receivertid from extrans
                   where extid = %s;"""
        cursor.execute(query, (extid,))
        extid = cursor.fetchone()[0]
        return extid

    def getExchangeAttr(self, rid, wid):
        cursor = self.conn.cursor()
        query = "select rstock, rcapacity from racks natural inner join warehouses where wid = %s and rid = %s;"
        cursor.execute(query, (wid, rid,))
        result = cursor.fetchone()
        return result

    def getTransactionByExtid(self, extid):
        cursor = self.conn.cursor()
        query = """select tid, uid, wid, pid, date, qty, total, type from transactions as T, extrans as E
                   where extid = %s and (E.sendertid=T.tid or E.receivertid=T.tid) order by tid;"""
        cursor.execute(query, (extid,))
        transactions = cursor.fetchall()
        return transactions

    def insertExchange(self, sendertid, receivertid):
        cursor = self.conn.cursor()
        query = "insert into extrans(sendertid, receivertid) values (%s, %s) returning extid;"
        cursor.execute(query, (sendertid, receivertid,))
        transaction = cursor.fetchone()
        self.conn.commit()
        return transaction[0]

    def updateExchangeById(self, extid, date, qty):
        transactions=[]
        cursor = self.conn.cursor()
        query = """update transactions set date = TO_DATE(%s,'MM/DD/YYYY'), qty = %s
                   where tid = (select tid from transactions as T, extrans as E where extid = %s and E.sendertid=T.tid)
                   returning tid, uid, wid, pid, to_char(date, 'MM/DD/YYYY'), qty, total, type;"""
        cursor.execute(query, (date, qty, extid,))
        transactions.append(cursor.fetchone())
        self.conn.commit()
        query = """update transactions set date = TO_DATE(%s,'MM/DD/YYYY'), qty = %s
                           where tid = (select tid from transactions as T, extrans as E where extid = %s and E.receivertid=T.tid)
                           returning tid, uid, wid, pid, to_char(date, 'MM/DD/YYYY'), qty, total, type;"""
        cursor.execute(query, (date, qty, extid,))
        transactions.append(cursor.fetchone())
        self.conn.commit()
        return transactions