from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import json
# import time

# 검색 위치 url 및 privatekey 찾아오기.
file_path="./etc/teniron.json"
with open(file_path,'r',encoding='utf-8') as file:
    data = json.load(file)
    url,private_key = data["BarracudaCentral"].values()

# 크롤링할 ip 가져오기, 일시적 에러 + 서버 오류시 대응.
ip_list_name="laBel_sample0001_ppd.txt"
ip_list_path=f'./data/preprocessed/{ip_list_name}'
new = open(f'./data/responses/barracuda_result_{ip_list_name}','w')
retry_list=[]
error_log=[]
with open(ip_list_path,'r',encoding='utf-8') as ips:
        chrome_options = Options()
        chrome_options.add_argument("headless")
        chrome_options.add_argument('log-level=3')
        # chrome_options.add_experimental_option("detach", True) 
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(10)
        for line in tqdm(ips.readlines(),desc='1차 크롤링'):
            ip=line.strip()
            try:
                driver.find_element(By.CSS_SELECTOR,"#ir_entry").send_keys(ip)
                driver.find_element(By.CSS_SELECTOR,'#lookup-reputation > div > div.yui-u.first > form > fieldset > div:nth-last-child(1) > input[type=submit]:nth-child(2)').click()
                driver.find_element(By.CSS_SELECTOR,"#ir_entry").clear()
                new.write(driver.find_element(By.CSS_SELECTOR,"#lookup-reputation > div > div.yui-u.first > form > fieldset > p").text + "\n")
            except Exception as e:
                retry_list.append(ip)
                error_log.append(f"{ip}:{e}")

        pending=[]
        for ret in tqdm(range(len(retry_list)),desc="재시도 1차"):
            try:
                ip=retry_list[ret]
                driver.find_element(By.CSS_SELECTOR,"#ir_entry").send_keys(ip)
                driver.find_element(By.CSS_SELECTOR,'#lookup-reputation > div > div.yui-u.first > form > fieldset > div:nth-last-child(1) > input[type=submit]:nth-child(2)').click()
                new.write(driver.find_element(By.CSS_SELECTOR,"#lookup-reputation > div > div.yui-u.first > form > fieldset > p").text + "\n")
            except:
                 pending.append(ip)
                 error_log.append(f"{ip}:{e}")

driver.quit()
new.write(f"not working : {pending}"+"\n")
new.write(f"internal error_log : {error_log}"+"\n")
new.close()

# ? 해결중인 issue
# 크롬 창을 띄우지 않게 하려고 하면 뜨는 에러? 경고? 
# Uncaught TypeError: Cannot read properties of null (reading 'select') 
# 내지는
# A parser-blocking, cross site (i.e. different eTLD+1) script, https://ssl.google-analytics.com/ga.js,
# is invoked via document.write.
# The network request for this script MAY be blocked by the browser in this or a future page load
# due to poor network connectivity.
# If blocked in this page load, it will be confirmed in a subsequent console message.
# See https://www.chromestatus.com/feature/5718547946799104 for more details.
# 이런 에러가 뜬다. 

# ! loglevel을 3으로 올려 임시 해결 
# INFO = 0, 
# WARNING = 1, 
# LOG_ERROR = 2, 
# LOG_FATAL = 3.
