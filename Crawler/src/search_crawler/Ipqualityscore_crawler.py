import requests
import sys
from tqdm import tqdm
import json
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule 

with open('/home/teamlab/ThanosIP/Crawler/etc/teniron.json', 'r') as file:
    teniron = json.load(file)
url = teniron["Ipqualityscore"]["url"]["ip"]["look"]
key = teniron["Ipqualityscore"]["key"]

# IPQS의 검색 옵션 초기값 설정
strictness="0"
allow_public_access_points="true"
fast="true"
lighter_penalties="true"
mobile="true"
option = "&".join([f'strictness={strictness}',f'allow_public_access_points={allow_public_access_points}',
                   f'fast={fast}',f'lighter_penalties={lighter_penalties}',f'mobile={mobile}'])

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
        

        query=url+key+'/'+ip+"?"+option
        res_raw = requests.get(query)
        

        # 데이터 추출
        data = json.loads(res_raw.text)

        seccess = int(data['success'])
        message = data['message']
        fraud_score = data['fraud_score']
        country_code = data['country_code']
        region = data['region']
        city = data['city']
        ISP = data['ISP']
        ASN = data['ASN']
        organization = data['organization']
        is_crawler = int(data['is_crawler'])
        timezone = data['timezone']
        mobile = int(data['mobile'])
        host = data['host']
        proxy = int(data['proxy'])
        vpn = int(data['vpn'])
        tor = int(data['tor'])
        active_vpn = int(data['active_vpn'])
        active_tor = int(data['active_tor'])
        recent_abuse = int(data['recent_abuse'])
        latitude = data['latitude']
        request_id = data['request_id']
        

        # DB에 저장
        query = f'INSERT INTO Ipqualityscore_Crawl (ip,success,message,fraud_score,country_code,region,city,ISP,ASN,organization,is_crawler,timezone,mobile,host,proxy,vpn,tor,active_vpn,active_tor,recent_abuse,latitude,request_id) VALUES ("{i["ip"]}", "{seccess}", "{message}", "{fraud_score}", "{country_code}", "{region}", "{city}", "{ISP}", "{ASN}", "{organization}", "{is_crawler}", "{timezone}", "{mobile}", "{host}", "{proxy}", "{vpn}", "{tor}", "{active_vpn}", "{active_tor}", "{recent_abuse}", "{latitude}", "{request_id}")'

        db_class.execute(query)

except Exception as e:
    print(f"Error: {e}")

# MariaDB 연결 종료
db_class.commit()
