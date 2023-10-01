# Abuse_Crawl.py
# API 결과값 txt 파일에 저장 + 진행률 bar 표시 + 크롤링 완료시 비프음 발생

import requests
import json
import time
from tqdm import tqdm
# import winsound as sd

import sys, os
sys.path.append('/home/teamlab/ThanosIP/Crawler/etc/')
from variableFile import AbuseAPI


# mariaDB 연결중..

# ip list 파일 열고 output 저장할 변수 선언
ip_file = open("/home/teamlab/ThanosIP/Crawler/data/preprocessed/laBel_sample0001.txt", 'r')
ip_output = open("../../data/Abuse_output.txt", 'w')

# 16째 줄부터 (ip 부분만) 읽기
ip_line = ip_file.readlines()[15:]

# while문으로 한줄씩 ip 뒤에 줄바꿈 문자 제거
i = 0
only_ip = []
while i < len(ip_line) :
    only_ip.append(ip_line[i].rstrip())
    i += 1

# 정제된 ip 리스트 확인 출력
# print(only_ip)

# while문으로 ip 한줄씩 반복 검색하기
t = 0
for t in tqdm(range(len(only_ip)), desc='Processing', total=len(only_ip)):
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        
        'ipAddress': only_ip[t],
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': AbuseAPI
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    # Formatted output
    decodedResponse = json.loads(response.text)

    # if문으로 정상 결과값이면 output 파일에 쓰기
    ip_output.write(json.dumps(decodedResponse, sort_keys=True, indent=4))

    # elif문으로 error 결과값이면,
    # 서버 오류 (500번대)라면 error_ip txt 파일에 쓰기
    # 그 외 오류라면 ip 검색 재시도
    # 몇 번 시도해도 안되면 error_ip txt 파일에 쓰기

    
# ip list 파일 닫기
ip_file.close()
ip_output.close()

# # 비프음 발생 함수
# def beepsound() :
#     fr = 555
#     du = 1000
#     sd.Beep(fr, du)

# # 작업 완료시 비프음 발생
# beepsound()

