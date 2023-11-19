from config.dbconfig import pg_config
import psycopg2

class GlobalStatisticsDAO:

    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getTopWarehousesMostRacks(self):

        query = """select w.wid, count(r.rid) as rack_count
                    from warehouses as w join racks as r on w.wid = r.wid
                    group by w.wid
                    order by rack_count desc
                    limit 10;
                """

        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    def getTopWarehousesMostIncoming(self):

        query = """ select w.wid, count(i.inid) as incoming_count
                    from warehouses as w join intran as i on w.wid = i.wid
                    group by w.wid
                    order by incoming_count desc
                    limit 5;
                """

        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result
