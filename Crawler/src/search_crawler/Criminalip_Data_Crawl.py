import requests
import sys
from tqdm import tqdm
import json
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule 

with open('/home/teamlab/ThanosIP/Crawler/etc/teniron.json', 'r') as file:
    teniron = json.load(file)
key = teniron["Criminalip"]["key"]


# MariaDB 연결 설정
db_class=dbModule.Database('laBelup')

# db.executeMany로 상위 100개의 IP 주소를 가져온다.
result=db_class.executeMany('select ip,count(ip) from bad_ip_list where ip not like "%%/%%" group by ip order by count(ip) desc;',100) # not like : 서브넷 미 포함, like: 서브넷 포함

try:
    for i in tqdm(result, desc="progress"):
        
        if '/' in i["ip"]:
            ip, sub = i["ip"].split('/')
        else:
            ip = i["ip"]  
         
        
        url = "https://api.criminalip.io/v1/ip/data?ip={}".format(ip)
        payload = {}
        headers = {
            "x-api-key": "{}".format(key)
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.json()
        # 데이터 추출
        ip = result["ip"]
        score = result["score"]
        inbound_score = score["inbound"]
        outbound_score = score["outbound"]
        search_count = result["user_search_count"]
        if "whois" in result and "data" in result["whois"] and result["whois"]["data"]:
          country_code = result["whois"]["data"][0]["org_country_code"]
        else:
          country_code = None  # 또는 적절한 기본값 설정

         # 데이터베이스에서 해당 IP 주소를 조회
        existing_data = db_class.execute('SELECT * FROM Criminalip_Crawl WHERE ip = %s', (ip,))
    
        if existing_data:
        # 이미 존재하는 경우, 업데이트 수행
          query = f'UPDATE Criminalip_Crawl SET inbound_score = "{inbound_score}", outbound_score = "{outbound_score}", search_count = "{search_count}", country_code = "{country_code}" WHERE ip = "{i["ip"]}"'
        else:
        # 존재하지 않는 경우, 삽입 수행
          query = f'INSERT INTO Criminalip_Crawl(ip, inbound_score, outbound_score, search_count, country_code) VALUES ("{i["ip"]}", "{inbound_score}", "{outbound_score}", "{search_count}", "{country_code}")'
          db_class.execute(query)

except Exception as e:
    print(f"Error: {e}")

# MariaDB 연결 종료
db_class.commit()

