import requests
from datetime import datetime
from tqdm import tqdm
import sys, os
sys.path.append('/home/teamlab/ThanosIP/Module/')
import IPmaster
import dbModule
import json
import hashlib

shred_inst=IPmaster.ip_shredder()
error_log=[]

# url등 필요한 설정 옵션 불러오기.
with open("/home/teamlab/ThanosIP/Crawler/etc/teniron.json") as file:
	options=json.load(file) # url, 필요시 key 받아오기.
	ip_list = options.keys()
	exclude=["MariaDB","AwsEC2","AbuseAPI","Criminalip","VirusTotal"] #제외할사이트 지정

# 사이트 순회 다운로드 
	for name in ip_list: 
		if name not in exclude:
			url=options[name]["url"]["ip"]["down"]

# 다운로드 url이 존재할 시(사전조사)
			if url:
				response = requests.get(url)
				if response.status_code == 200:  # 통신 ok시
					current_datetime = datetime.now() # 날짜
					if name=="Spamhaus":
						modify_check=str(response.content).split(';')
						for m in modify_check:
							if 'Last-Modified' in m.strip():
								file_hash=hashlib.sha256(m.strip().encode('utf-8')).hexdigest() # Spamhaus만 modify이 매번 달라짐
					else:
						file_hash=hashlib.sha256(response.content).hexdigest() #file 변조 확인 hash값 
					ip_list=shred_inst.ip_extractor(str(response.content)) # ip 추출
					table_name="bad_ip_list" # 저장할 Table 이름
					itable_name="file_history"
					DB_name="laBelup" # 사용할 Database 이름
					db_class = dbModule.Database(DB_name) # db 인스턴스
					try:
						sql=f"SELECT hash from {itable_name} WHERE site_id='{name}'"
						db_hash=db_class.executeAll(sql)
						db_class.commit()
					except Exception as ex:
						error_log.append("DBerror\n"+str(ex))
					# hash 존재 여부 확인
					if not db_hash:
						try:
							new_sql = f"INSERT INTO {itable_name} VALUES('{name}','{url}',NULL, NULL)"
							db_class.execute(new_sql)
							db_class.commit()
						except Exception as ex:
							error_log.append("DBerror\n"+str(ex))
					else:
						db_hash=db_hash[0]['hash']
					# 변경점 확인시 
					if db_hash!=file_hash:
						for i in tqdm(ip_list,desc=name):
							try:
								insert_data=f'"{i}","{name}","{current_datetime}"'
								sql = f"INSERT INTO {table_name}(ip,site_id,update_time) VALUES({insert_data})" 
								db_class.execute(sql) # db에 sql문 작성
								db_class.commit() #sql문 실행 
							except Exception as ex:
								error_log.append("DBerror\n"+str(ex))
						try:
							end_sql = f"UPDATE {itable_name} SET hash='{file_hash}',hash_update_time='{current_datetime}' WHERE site_id='{name}'"
							db_class.execute(end_sql)
							db_class.commit()
						except Exception as ex:
							error_log.append("DBerror\n"+str(ex))
				else:
				    error_log.append(f"{name} *** 파일을 다운로드하는 중에 오류가 발생했습니다. 응답 코드: {response.status_code}")

# error 로그 존재시 기록하기
if error_log:
	with open(f"/home/teamlab/ThanosIP/Crawler/data/internal_logs/errlog_{current_datetime}.txt","w") as errfile:
		for e in error_log:
			errfile.write(e+"\n")
	message="**Partial Success** Some error occured during execution please check errlog."
else:
	message="***Success*** Successfully saved data to our database"

with open(f"/home/teamlab/ThanosIP/Crawler/data/internal_logs/scooper_log.txt","a") as sclog:
	sclog.write(f'[{current_datetime}] {message}\n')



