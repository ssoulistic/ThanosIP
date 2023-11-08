import sys
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule
from datetime import datetime
db_class=dbModule.Database('laBelup')

time=datetime.now()

# ip만 추출 
query1=f'select DISTINCT ip from bad_ip_list where ip not like "%%/%%" order by ip;'
ip_list=db_class.executeAll(query1)
query2=f'select DISTINCT ip from bad_ip_list where ip like "%%/%%" order by ip;'
subnet_list=db_class.executeAll(query2)


with open('/home/teamlab/ThanosIP/Server/API/data/suspicious_ip_list.txt','w') as file:
    file.write(f'List created by team laBelup (Project with Monitorapp)\nlast_update:{time}\nlist order : 1.ip 2.subnet\n\n\n')
    ips,subnets='',''
    for ip in ip_list:
        ips+=ip['ip']+'\n'
    for subnet in subnet_list:
        subnets+=subnet['ip']+'\n'
    file.write(f"ip\nnumber of ip:{len(ip_list)}\n{ips}\nsubnet\nnumber of subnet:{len(subnet_list)}\n{subnets}")


with open('/home/teamlab/ThanosIP/Server/API/log/suspicious_ip_list_updated.log','a') as file2:
    file2.write(f'[{time}] ***Success*** Successfully updated ip list\n')
