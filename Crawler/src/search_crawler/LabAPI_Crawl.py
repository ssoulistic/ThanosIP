import requests
import json
from tqdm import tqdm
import datetime
# import winsound as sd

url = ('https://github.com/monitorapp-aicc/feed/blob/main/ip.txt')

t = 0
timecode = datetime.datetime.now().strftime('%y%m%d_%H%M%S')

ip_output = open("../../data/LabAPI_output"+timecode+".txt", 'w')

for t in tqdm(range(1), desc='Processing'):
    response = requests.request(method='GET', url=url)

    # Formatted output
    decodedResponse = json.loads(response.text)
    #print(json.dumps(decodedResponse, sort_keys=True, indent=4))

    #print(decodedResponse)

    ip_output.writelines(response.text)

ip_output.close()


## 비프음 발생 함수
#def beepsound() :
#    fr = 555
#    du = 1000
#    sd.Beep(fr, du)

## 작업 완료시 비프음 발생
#beepsound()
