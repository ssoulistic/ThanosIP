# IPmaster
# ! IPv4를 추출, 서브넷 처리하는 전처리기

# 현재 방식
# 1. 숫자와 점을 제외한 것들을 모두 제거하여 공백화 한다.
# 2. 공백 기준 split
# 3. 각각이 ipv4인지 체크하기 ipv4 정규식을 돌린다.

import re

class ip_shredder:
    
    def __init__(self):

        self.all='^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\/?([0-9]|[1-2][0-9]|3[0-2])$'
        self.alpha_clear='[^0-9\./]'
        self.ip_only='^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
        self.subnet_only='^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\/([0-9]|[1-2][0-9]|3[0-2])$'
        self.sub_border=[int(2**i) for i in range(7,-1,-1)]
    
    def ip_extractor(self,text,mode=0): # 텍스트에서 ip만 뽑아오기. 0 -> 서브넷 전부 1 -> 서브넷 제외. 2 -> 서브넷만

        self.mode=[self.all,self.ip_only,self.subnet_only][mode]
        self.noalpha=re.sub(self.alpha_clear," ",text).split()
        self.get_ip=re.compile(self.mode)
        self.response=[]
        for candi in self.noalpha:
            matcher=self.get_ip.match(candi)
            if matcher:
                self.response.append(matcher.group())
        return self.response
    
    def ip_spreader(self,subnet): # 서브넷 펼쳐보기. 리스트로 반환?

        ip,sub=subnet.split('/');sub=int(sub)
        ids=ip.split(".")
        spread_list=[]
        host_id, network_id = ids[sub // 8 :], ids[: (sub // 8)]
        start=sum(self.sub_border[:(sub % 8)])
        single=".".join(network_id)
        i=len(host_id)
        if i == 4:
            spread_list.append('NOT ACCEPTED')
        elif i ==3:
            for x in range(start,256):
                for y in range(0,256):
                    for z in range(0,256):
                        spread_list.append(single+"."+str(x)+"."+str(y)+"."+str(z))
        elif i ==2:
            for x in range(start,256):
                for y in range(0,256):
                    spread_list.append(single+"."+str(x)+"."+str(y))
        elif i ==1:
            for x in range(start,256):
                spread_list.append(single+"."+str(x))
        return spread_list
    
    def in_subnet(self,ip,subnet): #서브넷 포함 확인하기.
        
        spread=self.ip_spreader(subnet)
        if ip in spread:
            return True
        else:
            return False