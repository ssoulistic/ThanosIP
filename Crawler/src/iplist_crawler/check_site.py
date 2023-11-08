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
	#exclude=["MariaDB","AwsEC2","AbuseAPI","Criminalip","VirusTotal"] #제외할사이트 지정
	include=["Spamhaus","Talos","Nerd"]
# 사이트 순회 다운로드 
	for name in ip_list: 
		if name in include:
			url=options[name]["url"]["ip"]["down"]

# 다운로드 url이 존재할 시(사전조사)
			if url:
				response = requests.get(url)
				if response.status_code == 200:  # 통신 ok시
					current_datetime = datetime.now() # 날짜
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
						db_hash=db_hash[0]['hash']
					except Exception as e:
						print(e)

					with open(f"/home/teamlab/ThanosIP/Crawler/data/internal_logs/checker_log.txt","a") as sclog:
						sclog.write(f'{current_datetime}\n{name}\nfile_hash:{file_hash}\ndb_hash : {db_hash} \n{response.content}\n')



