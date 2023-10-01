import pymysql
from variableFile import SERVER, DBPORT, teampw

# dbkeys=open("./variableFile.py",'r',encoding='utf-8')
# db_meta=variableFile.load(dbkeys)

# SERVER,PORT = db_meta["SERVER"]["DBPORT"].split("/")
# USERNAME = 'team'
# PASSWORD = db_meta["teampw"]

DBSERVER = 'localhost'
PORT = DBPORT
USERNAME = 'team'
PASSWORD = teampw

class Database():
    def __init__(self,DATABASE):
        self.db = pymysql.connect(host=DBSERVER,
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

    def fetchall(self):
        self.cursor.fetchall()