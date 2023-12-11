from config.dbconfig import pg_config
import psycopg2


class Transaction_Dao:
    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getalltransactions(self):
        cursor = self.conn.cursor()
        result = []
        query = "select tid, uid, wid, pid, date, qty, total, type from transactions"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
    
    def insertTransaction(self, uid, wid, pid, qty, total, type):
        cursor = self.conn.cursor()
        query = """insert into transactions(uid, wid, pid, date, qty, total, type) 
                   values (%s, %s, %s, (current_date at time zone 'UTC' at time zone 'America/Puerto_Rico')::date, %s, %s, %s)
                   returning tid, to_char(date, 'YYYY/MM/DD');"""
        cursor.execute(query, (uid, wid, pid, qty, total, type,))
        transaction = cursor.fetchone()
        self.conn.commit()
        return transaction[0], transaction[1]

    def getalltransactionswarehouse(self, wid):
        cursor = self.conn.cursor()
        result = []
        query = "select tid, uid, wid, pid, date, qty, total, type from transactions where wid = %s order by date desc"
        cursor.execute(query, (wid,))
        for row in cursor:
            result.append(row)
        return result

    def searchbyid(self, pid):
        cursor = self.conn.cursor()
        query = "select * from transaction where pid = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result


