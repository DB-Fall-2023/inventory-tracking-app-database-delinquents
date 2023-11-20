from config.dbconfig import pg_config
import psycopg2


class Customer_Dao:
    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getAllcustomer(self):
        cursor = self.conn.cursor()
        result = []
        query = "select cid, cname, clastname, cphone, ccity, ccountry from customers"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def insertCustomer(self, name, lastname, phone, city, country):
        cursor = self.conn.cursor()
        query = ("insert into customers(cname, clastname, cphone, ccity, ccountry) "
                 "values (%s, %s, %s, %s, %s) returning cid")
        cursor.execute(query, (name, lastname, phone, city, country,))
        cid = cursor.fetchone()[0]
        self.conn.commit()
        return cid

    def searchbyid(self, cid):
        cursor = self.conn.cursor()
        query = "select cid, cname, clastname, cphone, ccity, ccountry from customers where cid = %s"
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        return result

    def updatebyid(self, cid, name, lastname, phone, city, country):
        cursor = self.conn.cursor()
        query = ("update customers set cname = %s, clastname = %s, cphone = %s, ccity = %s, ccountry = %s "
                 "where cid = %s")
        cursor.execute(query, (name, lastname, phone, city, country, cid,))
        count = cursor.rowcount()
        self.conn.commit()
        return count
