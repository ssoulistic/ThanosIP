import requests
from datetime import datetime
from tqdm import tqdm
import sys,os
sys.path.append('/home/teamlab/ThanosIP/Module/')
import IPmaster
import dbModule

shred_inst=IPmaster.ip_shredder()

url = 'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt'
response = requests.get(url)

if response.status_code == 200:  # '200'은 HTTP 상태 코드 중 하나로, 'OK'를 나타냄
    current_datetime = datetime.now() # 현재 날짜와 시간을 포맷팅하여 파일 이름에 넣기
     ip_list=shred_inst.ip_extractor(str(response.content))
     table_name="bad_ip_list" # 사용할 Table 이름
     DB_name="laBelup" # 사용할 Database 이름
     db_class = dbModule.Database(DB_name) # db 인스턴스
     for i in tqdm(ip_list):
         insert_data=f'"{i}","{url}","{current_datetime}"'
         sql = f"INSERT INTO {table_name} VALUES({insert_data})"
         db_class.execute(sql) # db에 sql문 작성
         db_class.commit() #sql문 실행i 
else:
    print(f"파일을 다운로드하는 중에 오류가 발생했습니다. 응답 코드: {response.status_code}")
