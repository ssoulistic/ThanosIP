import requests
import sys
from tqdm import tqdm
import json
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule 

with open('/home/teamlab/ThanosIP/Crawler/etc/teniron.json', 'r') as file:
    teniron = json.load(file)
key = teniron["AbuseAPI"]["key"]


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
         
        
        # Defining the api-endpoint
        url = 'https://api.abuseipdb.com/api/v2/check'

        querystring = {
            'ipAddress': ip,
            'maxAgeInDays': '90'
        }

        headers = {
            'Accept': 'application/json',
            'Key': key
        }
        
        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        result = response.json()

        
        # 데이터 추출
        data = result.get("data", {})


        abuseConfidenceScore = data.get("abuseConfidenceScore", -1)
        countryCode = data.get("countryCode", None)
        domain = data.get("domain", None)
        hostnames = data.get("hostnames", [])
        ip = data.get("ipAddress", None)
        ipVersion = data.get("ipVersion", -1)
        isPublic = data.get("isPublic", None)
        isTor = data.get("isTor", None)
        isWhitelisted = data.get("isWhitelisted", None)
        isp = data.get("isp", None)
        lastReportedAt = data.get("lastReportedAt", None)
        numDistinctUsers = data.get("numDistinctUsers", -1)
        totalReports = data.get("totalReports", -1)
        usageType = data.get("usageType", None)

        # DB에 저장
        query = f'INSERT INTO Abuse_Crawl (ip,abuseConfidenceScore,countryCode,domain,hostnames,ipVersion,isPublic,isTor,isWhitelisted,isp,lastReportedAt,numDistinctUsers,totalReports,usageType) VALUES ("{i["ip"]}",{abuseConfidenceScore}, "{countryCode}", "{domain}", "{",".join(hostnames)}", {ipVersion}, "{isPublic}", "{isTor}", "{isWhitelisted}", "{isp}", "{lastReportedAt}", {numDistinctUsers}, {totalReports}, "{usageType}")'
        db_class.execute(query)

except Exception as e:
    print(f"Error: {e}")

# MariaDB 연결 종료
db_class.commit()

