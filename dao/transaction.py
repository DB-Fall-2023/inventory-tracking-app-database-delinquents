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
        query = "select * from transactions"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

