import sys
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule

table_name="bad_ip_list" # 사용할 Table 이름
DB_name="laBelup" # 사용할 Database 이름

db_class = dbModule.Database(DB_name) # db 인스턴스
#sql = "SELECT ip from {table_name}"
name='Talos'
#sql = f"SELECT hash from file_history WHERE site_id='{name}'"

sql = f"SELECT * from file_history"

try:
	#x=db_class.executeOne(sql) # db에 sql문 작성
	x=db_class.executeMany(sql,3)
	for i in x:
		print(i)
	db_class.commit() #sql문 실행
	# print(x['hash'])
except  Exception as e:
	print(e)
	
