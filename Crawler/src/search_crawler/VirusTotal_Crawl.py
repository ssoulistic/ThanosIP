import requests
import sys
import winsound as sd
from tqdm import tqdm
import apikey


# ip list 파일 열기
file = open("laBel_sample0001.txt",'r')

# 변수에 한줄 씩 저장
line = file.readlines()

# 파일저장 변수 생성
sys.VirusTotal = open('VirusTotal.txt','w')

# 반복
try :  
    for i in tqdm((line),desc="progress") : 
        i = i.strip()
        if '#' not in i  :
            url = "https://www.virustotal.com/api/v3/ip_addresses/{}".format(i)
            headers = {"accept": "application/json", "x-apikey" : "{}".format(apikey.virustotal_apikey)}
            response = requests.get(url, headers=headers)
            result = response.json()

            if result['data']['attributes']['last_analysis_stats']['harmless'] > 0 and result['data']['attributes']['last_analysis_stats']['malicious'] == 0 :
                sys.VirusTotal.write('\"harmless\" : {} '.format(response.text))
               
            elif result['data']['attributes']['last_analysis_stats']['malicious'] > 0 :
                sys.VirusTotal.write('\"malicious\" : {} '.format(response.text))

            elif result['data']['attributes']['last_analysis_stats']['undetected'] == result['data']['attributes']['last_analysis_stats']['harmless'] + result['data']['attributes']['last_analysis_stats']['malicious'] + result['data']['attributes']['last_analysis_stats']['suspicious'] + result['data']['attributes']['last_analysis_stats']['undetected'] :
                sys.VirusTotal.write('\"undetected\" : {} '.format(response.text))
except :
    print("Error")
sys.VirusTotal.close()

file.close()

#비프음
def beepsound() :
    fr = 2000
    du = 1000
    sd.Beep(fr,du)
beepsound()
