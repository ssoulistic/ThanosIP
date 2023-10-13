import hashlib
#test1=test2, test3 +word , test4 -word

# 1. read json file
# 2. json file to data and uses sha256
# 3. save result in db
# file_name="bad_ips.txt"
test_list=["test1.txt","test2.txt","test3.txt","test4.txt"]
data=[]
for file_name in test_list:
	f=open(f'/home/teamlab/ThanosIP/Crawler/data/resources/{file_name}',encoding='utf-8')
	data.append(hashlib.sha256(f.read().encode()).hexdigest())
	f.close()
for idx,hs in enumerate(data):
	print(f"test{idx+1} : {hs}")
