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

    def getWarehouseProfitByYear(self, wid):
        cursor = self.conn.cursor()
        query = """select wid, wname, to_char(date, ' YYYY') AS year, sum(qty*pprice) as costs, 
                   sum(qty*pprice+qty*pprice*wsellingmult) as sales, sum(qty*pprice+qty*pprice*wsellingmult) - sum(qty*pprice) as grossProfit
                   from parts natural inner join outtrans natural inner join transactions natural inner join warehouses 
                   where wid=%s and outtrans.tid=transactions.tid group by wid, wname, year order by year;"""
        cursor.execute(query, (wid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTop5RackUnder25Pct(self, wid):
        cursor = self.conn.cursor()
        query = """select rid, wid, pid, rcapacity, rstock, round(1.0*rstock/rcapacity, 2) as qtypct from racks
                   where wid=%s group by rid having round(1.0*rstock/rcapacity, 2) < 0.25 order by qtypct desc limit 5"""
        cursor.execute(query, (wid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBottom3PartsByType(self, wid):
        cursor = self.conn.cursor()
        query = "select pid, pname, ptype, pprice from parts natural inner join racks where wid=%s order by ptype limit 3;"
        cursor.execute(query, (wid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

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
        query = """select s.sid, s.sname, s.scity, s.scountry, s.sphone, count(it.inid) as totalsupplied
                   from warehouses as w join transactions as i on w.wid = i.wid
                        join intrans as it on it.tid = i.tid
                        join suppliers as s on it.sid = s.sid
                   where i.wid = 1
                   group by s.sid, s.sname, s.scity, s.scountry, s.sphone
                   order by totalsupplied desc
                   limit 3
                """
        cursor.execute(query, (wid,))
        result = cursor.fetchall()
        return result

    def getDaysLeastcostbyID(self, wid):
        cursor = self.conn.cursor()
        query = """select i.date, sum(total) as TotalPrice
                    from warehouses as w join transactions as i on w.wid = i.wid
                    where i.wid = 1 and i.type = 'incoming'
                    group by date
                    order by TotalPrice
                    limit 3
                """
        cursor.execute(query, (wid,))
        result = cursor.fetchall()
        return result

    def getTopUsersMostExchanges(self, wid):
        query = """select uid, count(*) as exchangeCount
                    from transactions
                    where type = 'exchange-receiver'
                    group by uid
                    order by exchangeCount desc
                    limit 3
                        """
        cursor = self.conn.cursor()
        cursor.execute(query, (wid,))
        result = cursor.fetchall()
        return result

