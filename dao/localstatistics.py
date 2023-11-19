from config.dbconfig import pg_config
import psycopg2


class LSDAO:

    def __init__(self):
        connection_url = ('host = %s dbname = %s user = %s password = %s'
                          % (pg_config['host'],
                             pg_config['dbname'],
                             pg_config['user'],
                             pg_config['password']))

        self.conn = psycopg2.connect(connection_url)

    def getFiveExpensiveRacksbyID(self, wid):
        cursor = self.conn.cursor()
        query = """select r.rid, r.rstock, p.pname, p.ptype, 
                    Cast(((r.rstock * p.pprice) + ((r.rstock * p.pprice) * w.wsellingmult)) as int) as TotalPrice
                    from warehouses as w join racks as r on w.wid = r.wid join parts as p On r.pid = p.pid
                    where r.wid = %s        
                    order by TotalPrice desc limit 5
                """
        cursor.execute(query, (wid,))
        result = cursor.fetchall()
        return result

    def getTopSupplierbyID(self, wid):
        cursor = self.conn.cursor()
        query = """select s.sid, s.sname, s.scity, s.scountry, s.sphone, count(i.inid) as totalsupplied
                   from warehouses as w join intran as i on w.wid = i.wid join suppliers as s on i.sid = s.sid
                   where i.wid = %s
                   group by s.sid, s.sname, s.scity, s.scountry, s.sphone
                   order by totalsupplied desc
                   limit 3
                """
        cursor.execute(query, (wid,))
        result = cursor.fetchall()
        return result

    def getDaysLeastcostbyID(self, wid):
        cursor = self.conn.cursor()
        query = """select i.intdate, sum(inttotal) as TotalPrice
                    from warehouses as w join intran as i on w.wid = i.wid
                    where i.wid = %s
                    group by intdate
                    order by TotalPrice
                    limit 3
                """
        cursor.execute(query, (wid,))
        result = cursor.fetchall()
        return result
