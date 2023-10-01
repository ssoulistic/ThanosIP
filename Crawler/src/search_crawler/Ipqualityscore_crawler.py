import json
import requests
from tqdm import tqdm

# url 과 privatekey 가져오기
file_path="./etc/teniron.json"
with open(file_path,'r',encoding='utf-8') as file:
        data =json.load(file)
        url,private_key = data["Ipqualityscore"].values()

# 샘플 ip 파일.
ip_list_name="laBel_sample0001_ppd.txt"
ip_list_path=f'./data/preprocessed/{ip_list_name}'

# IPQS의 검색 옵션 초기값 설정
strictness="0"
allow_public_access_points="true"
fast="true"
lighter_penalties="true"
mobile="true"
option = "&".join([f'strictness={strictness}',f'allow_public_access_points={allow_public_access_points}',
                   f'fast={fast}',f'lighter_penalties={lighter_penalties}',f'mobile={mobile}'])

# 에러시 처리를 위한 재 시도 목록.
retry_list=[]
error_log=[]
# IPQS 결과 파일 기록 시작.
new=open(f'./data/responses/IPQS_result_{ip_list_name}','w')

#크롤링 시작.
with open(ip_list_path,'r',encoding='utf-8') as ips:
        for line in tqdm(ips.readlines(),desc='1차 크롤링'):
                if line[0]=="#":
                        continue
                else:
                        ip = line.strip()
                        try:
                                query=url+private_key+'/'+ip+"?"+option
                                res_raw = requests.get(query)
                                res_json = json.loads(res_raw.text)
                                new.write(res_raw.text+"\n")
                        except Exception as e:
                                retry_list.append(ip)
                                error_log.append(e)

        # 에러가 났던 ip들 재시도.
        pending=[]
        for ret in tqdm(range(len(retry_list)),desc="재시도 1차"):
                ip=retry_list[ret]
                try:
                        res_raw = requests.get(query)
                        res_json = json.loads(res_raw.text)
                        new.write(res_raw.text+"\n")
                except Exception as e:
                        pending.append(ip)
                        error_log.append(e)
        # 에러이유별 분류.
        new.write(f"http 500+ : {pending}"+"\n")
        new.write(f"internal error_log : {error_log}"+"\n")
new.close()