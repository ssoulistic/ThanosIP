import requests
import sys
import json
from tqdm import tqdm
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule 

with open('/home/teamlab/ThanosIP/Crawler/etc/teniron.json', 'r') as file:
    teniron = json.load(file)
key = teniron["VirusTotal"]["key"]


db_class=dbModule.Database('laBelup')

result=db_class.executeMany('select ip,count(ip) from bad_ip_list where ip not like "%%/%%" group by ip order by count(ip) desc;',100) # not like : 서브넷 미 포함, like: 서브넷 포함

try:
    for i in tqdm(result, desc="progress"):
        if '/' in i["ip"]:
            ip, sub = i["ip"].split('/')
        else:
            ip = i["ip"]  
        
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"accept": "application/json", "x-apikey" : "{}".format(key)}
        response = requests.get(url, headers=headers)
        result = response.json()


        # 필요한 정보 추출
        attributes = result["data"]["attributes"]
        ip = result["data"]["id"]
        harmless = attributes["last_analysis_stats"]["harmless"]
        malicious = attributes["last_analysis_stats"]["malicious"]
        suspicious = attributes["last_analysis_stats"]["suspicious"]
        undetected = attributes["last_analysis_stats"]["undetected"]
        network = attributes.get("network")
        asn = attributes.get("asn", -1)
        whois_date = attributes["whois_date"]
        reputation = attributes["reputation"]

        # DB에 저장
        query = f'INSERT INTO VirusTotal_Crawl (ip,harmless,malicious,suspicious,undetected,network,asn,whois_date,reputation) VALUES ("{i["ip"]}", {harmless}, {malicious}, {suspicious}, {undetected}, "{network}", {asn}, {whois_date}, {reputation})'
        db_class.execute(query)


except Exception as e:
    print(f"Error: {e}")

# MariaDB 연결 종료
db_class.commit()

