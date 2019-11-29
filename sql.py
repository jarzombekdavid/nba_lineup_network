import pymysql
import os

class SqlHandler:
    def __init__(self):
        self.connect()

    def connect(self):
        self.con = pymysql.connect(
            user=os.getenv('DIGITAL_OCEAN_USER'),
            password=os.getenv('DIGITAL_OCEAN_PW'),
            host=os.getenv('DIGITAL_OCEAN_SERVER'),
            db='nba')
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)

    def query_batch(self, query, batchsize=50000):
        self.cur.execute(query)
        while True:
            data = self.cur.fetchmany(batchsize)
            if not data:
                break
            else:
                yield data

    def query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        try:
            self.cur.close()
            self.con.close()
        except:
            pass