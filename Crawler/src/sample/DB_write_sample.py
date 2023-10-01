import Crawler.src.module.dbModule as dbModule

table_name="test_table" # 사용할 Table 이름
# insert_data='"123.123.123.123",1,NULL,"KR","never.comx",33' # DB에 기록할 데이터 (크롤링한 데이터 중 필요한 것)
ip=1
reputation_score=1
xxx="NULL"
country="KR"
insert_data='"{ip}",{reputation_score},{xxx},"{country}"'
DB_name="testlab" # 사용할 Database 이름
db_class = dbModule.Database(DB_name) # db 인스턴스
sql = f"INSERT INTO {table_name} VALUES({insert_data})" # SQL 쿼리문 => select,insert 모두 가능한데 지금은 입력만
sql = "SELECT * from test_table"
db_class.execute(sql) # db에 sql문 작성
db_class.commit() #sql문 실행


# try:
#     conn = mariadb.connect(user=USERNAME,password=PASSWORD,host=SERVER,port=PORT,database=DATABASE)
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)
