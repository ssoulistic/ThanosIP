import json
with open("/home/teamlab/ThanosIP/Crawler/etc/teniron.json") as file:
	options=json.load(file)
ip_list = options.keys()
exclude=["MariaDB","AwsEC2","AbuseAPI"]
for name in ip_list:
	if name not in exclude:
		url=options[name]["url"]["ip"]["down"]
		if url:
			print(url)

		
