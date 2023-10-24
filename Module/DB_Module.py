import pymysql
import json

dbkeys=open("/home/teamlab/ThanosIP/Crawler/etc/teniron.json",'r',encoding='utf-8')
db_meta=json.load(dbkeys)

SERVER,PORT = db_meta["MariaDB"]["server"].split("/")
USERNAME = 'team'
PASSWORD = db_meta["MariaDB"]["password"]

def dataB():
    db = pymysql.connect(
        host=SERVER,
        user=USERNAME,
        password=PASSWORD,
        database="laBelup",
        charset="utf8"
    )
    return db

