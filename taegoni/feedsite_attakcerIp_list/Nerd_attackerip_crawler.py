import requests
from datetime import datetime

url = 'https://nerd.cesnet.cz/nerd/data/bad_ips.txt'

response = requests.get(url)

if response.status_code == 200:  # '200'은 HTTP 상태 코드 중 하나로, 'OK'를 나타냄
    current_datetime = datetime.now().strftime('%y%m%d_%H%M%S') # 현재 날짜와 시간을 포맷팅하여 파일 이름에 넣기
    filename = f'./feedsite_attakcerIp_list/NerdIp_attackerip_{current_datetime}.txt' 
    with open(filename, 'wb') as file:
        file.write(response.content)
        print(f"파일이 성공적으로 저장되었습니다.")
        
else:
    print(f"파일을 다운로드하는 중에 오류가 발생했습니다. 응답 코드: {response.status_code}")
