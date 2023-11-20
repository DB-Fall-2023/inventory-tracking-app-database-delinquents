from config.dbconfig import pg_config
import psycopg2


class Supplies_Dao:
    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getallsupplies(self):
        cursor = self.conn.cursor()
        result = []
        query = "select * from supplies"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def deletebysidandpid(self, pid, sid):
        cursor = self.conn.cursor()
        query = "delete from supplies where sid = %s and pid = %s"
        cursor.execute(query, (sid, pid,))
        count = cursor.rowcount
        self.conn.commit()
        return count

    def searchbysidandpid(self, pid, sid):
        cursor = self.conn.cursor()
        query = "select * from supplies where sid = %s and pid = %s"
        cursor.execute(query, (sid, pid,))
        result = cursor.fetchone()
        return result

    def updatebysidandpid(self, pid, sid, stock):
        cursor = self.conn.cursor()
        query = "update supplies set stock = %s where sid = %s and pid = %s"
        cursor.execute(query, (stock, sid, pid,))
        count = cursor.rowcount
        self.conn.commit()
        return count

    def insertSupplies(self, pid, sid, stock):
        cursor = self.conn.cursor()
        query = "insert into supplies(sid, pid, stock) values (%s, %s, %s);"
        cursor.execute(query, (sid, pid, stock,))
        self.conn.commit()

    def getStock(self, sid, pid):
        cursor = self.conn.cursor()
        query = """select stock from supplies
                    where sid = %s and pid = %s"""
        cursor.execute(query, (sid, pid,))
        result = cursor.fetchone()[0]
        return result
    
    def updateStock(self, sid, pid, stock, operation):
        cursor = self.conn.cursor()
        if operation == "sum":
            query = "update supplies set stock = stock + %s where sid = %s and pid = %s"
        elif operation == "subtract":
            query = "update supplies set stock = stock - %s where sid = %s and pid = %s"
        cursor.execute(query, (stock, sid, pid,))
        self.conn.commit()


