from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import json
import sys
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule 

# 검색 위치 url 및 privatekey 찾아오기.
file_path = "/home/teamlab/ThanosIP/Crawler/etc/teniron.json"
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    url = data["BarracudaCentral"]['url']['ip']['look']

# MariaDB 연결 설정
db_class = dbModule.Database('laBelup')

# db.executeMany로 상위 100개의 IP 주소를 가져온다.
result=db_class.executeMany('select ip,count(ip) from bad_ip_list where ip not like "%%/%%" group by ip order by count(ip) desc;',100) # not like : 서브넷 미 포함, like: 서브넷 포함

# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("headless")
chrome_options.add_argument('log-level=3')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
driver.implicitly_wait(10)


try:
    for i in tqdm(result, desc="progress"):
        if '/' in i["ip"]:
            ip, sub = i["ip"].split('/')
        else:
            ip = i["ip"]  
         
        
        driver.find_element(By.CSS_SELECTOR, "#ir_entry").send_keys(ip)
        driver.find_element(By.CSS_SELECTOR, '#lookup-reputation > div > div.yui-u.first > form > fieldset > div:nth-last-child(1) > input[type=submit]:nth-child(2)').click()
        driver.find_element(By.CSS_SELECTOR, "#ir_entry").clear()
        result_text = driver.find_element(By.CSS_SELECTOR, "#lookup-reputation > div > div.yui-u.first > form > fieldset > p").text

        # 데이터 추출
        if "please click here" in result_text :
            query = f'INSERT INTO BarracudaCentral_Crawl (ip,reputation) VALUES ("{i["ip"]}","malicious")'
            db_class.execute(query)
        else :
            query = f'INSERT INTO BarracudaCentral_Crawl (ip,reputation) VALUES ("{i["ip"]}","safe")'
            db_class.execute(query)
            

except Exception as e:
    print(f"Error: {e}")


driver.quit()
# MariaDB 연결 종료
db_class.commit()

