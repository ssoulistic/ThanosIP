import pymysql
import json

dbkeys=open("./etc/teniron.json",'r',encoding='utf-8')
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
 
    def execute(self, query, args={}):
        self.cursor.execute(query, args)  
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()