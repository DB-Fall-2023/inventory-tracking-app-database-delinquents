from config.dbconfig import pg_config
import psycopg2


class Supplier_Dao:
    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getallsuppliers(self):
        cursor = self.conn.cursor()
        result = []
        query = "select * from suppliers"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def insertsupplier(self, name, lastname, phone, city, country):
        cursor = self.conn.cursor()
        query = ("insert into suppliers(sname, slastname, sphone, scity, scountry) "
                 "values (%s, %s, %s, %s, %s) returning sid")
        cursor.execute(query, (name, lastname, phone, city, country,))
        sid = cursor.fetchone()[0]
        self.conn.commit()
        return sid

    def searchbyid(self, sid):
        cursor = self.conn.cursor()
        query = "select * from suppliers where sid = %s"
        cursor.execute(query, (sid,))
        result = cursor.fetchone()
        return result

    def updatebyid(self, sid, name, lastname, phone, city, country):
        cursor = self.conn.cursor()
        query = ("update suppliers set sname = %s, slastname = %s, sphone = %s, scity = %s, scountry = %s "
                 "where sid = %s")
        cursor.execute(query, (name, lastname, phone, city, country, sid,))
        count = cursor.rowcount
        self.conn.commit()
        return count
    
    def verifySupplierSuppliesPart(self, sid, pid):
        cursor = self.conn.cursor()
        query = """select *
                    from suppliers as s join supplies as su on su.sid = s.sid
                    where  su.pid = %s and s.sid = %s"""
        cursor.execute(query, (pid, sid,))
        result = cursor.fetchone()
        return result

    def deletebyid(self, sid):
        cursor = self.conn.cursor()
        query = "delete from suppliers where sid = %s"
        try:
            cursor.execute(query, (sid,))
            count = cursor.rowcount
            self.conn.commit()
            return count
        except:
            return "Error"
        
    def searchParts(self, sid):
        cursor = self.conn.cursor()
        query = """select pid, pname, ptype, pprice, stock
                    from suppliers natural inner join supplies natural inner join parts
                    where sid = %s"""
        cursor.execute(query, (sid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

