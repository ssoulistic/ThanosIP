import pymysql
import json

dbkeys=open("/home/teamlab/ThanosIP/Crawler/etc/teniron.json",'r',encoding='utf-8')
db_meta=json.load(dbkeys)

SERVER,PORT = db_meta["MariaDB"]["server"].split("/")
USERNAME = 'team'
PASSWORD = db_meta["MariaDB"]["password"]

class Database():
    def __init__(self,DATABASE):
        self.db = pymysql.connect(host=SERVER,
                                  user=USERNAME,
                                  password=PASSWORD,
                                  db=DATABASE,
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    # query를 단순 실행
    def execute(self, query, args={}):
        self.cursor.execute(query, args)  

    # query를 실행 후 결과값 하나만 가져옴 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    # query를 실행 후 결과값 지정한 수 만큼  가져옴 
    def executeMany(self, query, many,args={}):
        self.cursor.execute(query,args)
        row=self.cursor.fetchmany(many)
        return row
    
    # query를 실행 후 결과값 모두  가져옴 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()
