import requests
from datetime import datetime
from tqdm import tqdm
import sys, os
sys.path.append('/home/teamlab/ThanosIP/Module/')
import IPmaster
import dbModule

shred_inst=IPmaster.ip_shredder()

url = 'https://nerd.cesnet.cz/nerd/data/bad_ips.txt'
response = requests.get(url)

if response.status_code == 200:  # '200'은 HTTP 상태 코드 중 하나로, 'OK'를 나타냄
	current_datetime = datetime.now() # 현재 날짜와 시간을 포맷팅하여 파일 이름에 넣기
	ip_list=shred_inst.ip_extractor(str(response.content))
	table_name="bad_ip_list" # 사용할 Table 이름
	DB_name="laBelup" # 사용할 Database 이름
	db_class = dbModule.Database(DB_name) # db 인스턴스
	crawled_ip_list = tqdm(ip_list)
	
	db_class.execute(f"SELECT ip FROM {table_name}") 
	
	print(ipInDB,"ipInDB")
	print(crawled_ip_list,"ip_list")
	for i in tqdm(ip_list):
		insert_data=f'"{i}","{url}","{current_datetime}"'
		print(i,"first i")
		if i in ipInDB:
			sql = f"INSERT INTO {table_name} VALUES({insert_data})" 
			print(i,"if_i")
		else:
			sql = f"UPDATE {DB_name} SET from = {url}, update_time = {current_datetime}"
			print(i,"else_if")
		db_class.execute(sql) # db에 sql문 작성
		db_class.commit() #sql문 실행 

else:
    print(f"파일을 다운로드하는 중에 오류가 발생했습니다. 응답 코드: {response.status_code}")
