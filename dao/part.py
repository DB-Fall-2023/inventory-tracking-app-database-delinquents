from config.dbconfig import pg_config
import psycopg2


class Part_Dao:

    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getallparts(self):
        cursor = self.conn.cursor()
        result = []
        query = "select * from parts"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def insertpart(self, name, tipo, price):
        cursor = self.conn.cursor()
        query = "insert into parts(pname, ptype, pprice) values (%s, %s, %s) returning pid"
        cursor.execute(query, (name, tipo, price,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid

    def searchbyid(self, pid):
        cursor = self.conn.cursor()
        query = "select pid, pname, ptype, pprice from parts where pid = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result

    def deletebyid(self, pid):
        cursor = self.conn.cursor()
        query = "delete from parts where pid = %s"
        cursor.execute(query, (pid,))
        count = cursor.rowcount
        self.conn.commit()
        return count

    def updatebyid(self, pid, name, tipo, price):
        cursor = self.conn.cursor()
        query = "update parts set pname = %s, ptype = %s, pprice = %s where pid = %s"
        cursor.execute(query, (name, tipo, price, pid,))
        count = cursor.rowcount
        self.conn.commit()
        return count
