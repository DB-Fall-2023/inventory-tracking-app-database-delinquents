from config.dbconfig import pg_config
import psycopg2


class User_Dao:
    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getallusers(self):
        cursor = self.conn.cursor()
        result = []
        query = "select * from users"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def insertuser(self, name, lastname, email, password, phone, country, city):
        cursor = self.conn.cursor()
        query = ("insert into users(uname, ulastname, uemail, upassword, uphone, ucountry, ucity) "
                 "values (%s, %s, %s, %s, %s, %s, %s) returning uid")
        cursor.execute(query, (name, lastname, email, password, phone, country, city,))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid

    def searchbyid(self, uid):
        cursor = self.conn.cursor()
        query = "select * from users where uid = %s"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def deletebyid(self, uid):
        cursor = self.conn.cursor()
        query = "delete from users where uid = %s"
        cursor.execute(query, (uid,))
        # count = cursor.rowcount
        self.conn.commit()
        return uid

    def updatebyid(self, uid, name, lastname, email, password, phone, country, city):
        cursor = self.conn.cursor()
        query = ("update users set uname = %s, ulastname = %s, uemail = %s, upassword = %s, uphone = %s, "
                 "ucountry = %s, ucity = %s where uid = %s")
        cursor.execute(query, (name, lastname, email, password, phone, country, city, uid))
        count = cursor.rowcount
        self.conn.commit()
        return count
