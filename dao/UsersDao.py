import psycopg2
from dbconfig import pg_config


class UsersDao:
    def __init__(self):
        connection_url = ("host=%s dbname=%s user=%s password=%s" %
                          (pg_config['host'],
                           pg_config['dbname'],
                           pg_config['user'],
                           pg_config['password']))
        self.conn = psycopg2.connect(connection_url)

    def get_all_users(self):
        cursor = self.conn.cursor()
        result = []
        query = "SELECT * FROM users"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def get_top3_transactioners(self):
        cursor = self.conn.cursor()
        result = []
        query = ('''
                SELECT DISTINCT uid, uname, ulastname, uemail, upassword,
                                uphone, ucountry, ucity, wid, total_transactions
                FROM users
                NATURAL INNER JOIN (SELECT uid, count(uid) as total_transactions
                                    FROM transactions
                                    GROUP BY uid
                                    ) as user_count
                ORDER BY total_transactions desc
                LIMIT 3;
                ''')
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
