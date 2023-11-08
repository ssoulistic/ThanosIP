import requests
import sys
from tqdm import tqdm
import json
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule 

with open('/home/teamlab/ThanosIP/Crawler/etc/teniron.json', 'r') as file:
    teniron = json.load(file)
url = teniron["Nerd"]["url"]["ip"]["look"]
key = teniron["Nerd"]["key"]

# MariaDB 연결 설정
db_class=dbModule.Database('laBelup')

# db.executeMany로 상위 100개의 IP 주소를 가져온다.
result=db_class.executeMany('select ip,count(ip) from bad_ip_list where ip not like "%%/%%" group by ip order by count(ip) desc;',100) # not like : 서브넷 미 포함, like: 서브넷 포함

option=["full","rep","fmt"]

try:
    for i in tqdm(result, desc="progress"):

        if '/' in i["ip"]:
            ip, sub = i["ip"].split('/')
        else:
            ip = i["ip"]  
        
                        
        query=f'{url}/ip/{ip}/{option[0]}'
      
        res_raw = requests.get(query,headers={"Authorization":f'token {key}'})
        
        # 데이터 추출
        data = json.loads(res_raw.text)
        
        try:
            rep = data['rep']
        except KeyError:
            rep = -1
        
        try:
            fmp = data['fmp']['general']
        except KeyError:
            fmp = -1
        
        try:
            name = data['asn'][0]['name']
        except KeyError:
            name = None
        
        try:
            last_update = data['asn'][0]['org']['ts_last_update']
        except KeyError:
            last_update = None
        
        try:
            ipblock = data['ipblock']['_id']
        except KeyError:
            ipblock = None
        
        try:
            city = data['geo']['city']
            country = data['geo']['ctry']
        except KeyError:
            city = None
            country = None
        
        
      
        # DB에 저장
        query = f'INSERT INTO Nerd_Crawl (ip,rep,fmp,name,last_update,ipblock,city,country) VALUES ("{i["ip"]}", {rep}, {fmp}, "{name}", "{last_update}", "{ipblock}", "{city}", "{country}")'
        db_class.execute(query)
        
except Exception as e:
    print(f"Error: {e}")

# MariaDB 연결 종료
db_class.commit()

                                
        
