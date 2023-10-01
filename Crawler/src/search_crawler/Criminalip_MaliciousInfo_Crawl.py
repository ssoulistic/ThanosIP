import requests
import json
import apikey

file = open("laBel_sample0001.txt",'r')

line = file.readlines()

criminalip_malicious_info = open('criminalip_malicious_info.txt','w')

try :
        
    for i in line :
        i = i.strip()
        if '#' not in i :
            url = "https://api.criminalip.io/v1/feature/ip/malicious-info?ip={}".format(i)

            payload = {}
            headers = {
                "x-api-key": "{}".format(apikey.criminalip_apikey)
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.json()

            formatted_data = json.dumps(data, indent=3)
            criminalip_malicious_info.write(formatted_data)
            print(i)
except :
    print("Error")

criminalip_malicious_info.close()
file.close()    