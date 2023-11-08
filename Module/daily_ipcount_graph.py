# daily_ipcount_graph

import requests
from datetime import datetime
from tqdm import tqdm
import sys, os
sys.path.append('/home/teamlab/ThanosIP/Module/')
import IPmaster
import dbModule

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates

# db 정보 입력
table_name = "ip_count"
DB_name = "laBelup"
db_class = dbModule.Database(DB_name)
update_time = datetime.now()

# ip_count.py 의 데이터를 x축, y축으로 그래프 그리기
# dash 모듈? matplotlib 모듈?

# x축 시간 간격 (하루) 최근 며칠/일주일/한달/1년/전체 구분

# class 형태로 만들어서 서버 코드에서 모듈로 사용가능하도록
# 입력값 = 테이블이름, x축, y축, x축 시간 간격

class drawG():

	def draw_graph(inputSql):
		sql = inputSql
		df = db_class.executeAll(sql)
		db_class.commit()

		ipdict = df[0]
		datedict = df[1]

		count = ipdict.get("count")
		count.index = datedict.get("date")

		plt.figure()
		plt.plot(label="Malicious IP", title="Number of malicious ip data from Thanos IP")
		plt.legent(loc='lower left')
		plt.grid(True)
		plt.show()
