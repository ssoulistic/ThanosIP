# GraphTestServer.py

from flask import Flask, request, jsonify, send_file,render_template
from flasgger import Swagger
import sys
sys.path.append('/home/teamlab/ThanosIP/Module/')
from DB_Module import dataB
import dbModule
from IPmaster import ip_shredder
## graph
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from io import BytesIO, StringIO
import numpy as np
## about date
from datetime import datetime
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
swagger = Swagger(app)

DB_name = "laBelup"

db = dataB()
db_class = dbModule.Database(DB_name)
ip_test = ip_shredder()
# drawGraph = daily_ipcount_graph.drawG()

@app.route('/')
def index():

    return '''
    <form method="get" action="/search_ip">
        IP 주소 입력: <input type="text" name="ip"><br>
        Option:
        <input type="radio" name="option" value="simple" checked> 간단 검사
        <input type="radio" name="option" value="detail"> 상세 정보 조회<br>
        <input type="submit" value="검색">
    </form>
    '''

@app.route('/search_ip', methods=['GET'])
def search_ip():
    """
    API endpoint to check an IP address.

    ---
    tags:
      - IP Search
    parameters:
      - name: ip
        in: query
        type: string
        required: true
        description: The IP address to check.
      - name: option
        in: query
        type: string
        enum: ['simple', 'detail']
        description: The option for IP checking.

    responses:
      200:
        description: The result of IP checking.
        schema:
          type: object
          properties:
            result:
              type: string
              description: The result of IP checking.
    """

    try:
        requested_ip = request.args.get('ip')
        option = request.args.get('option')

        # 유효한 IPv4 주소만 추출
        if not ip_test.isip(requested_ip):
            return jsonify({'error': 'Invalid input. Please provide a valid IPv4 address.'})

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM bad_ip_list WHERE ip = %s", (requested_ip))
        result = cursor.fetchone()

        if option == 'simple':
            if result and result[0] >= 1:
                return jsonify({requested_ip: 'malicious'})
            else:
                return jsonify({requested_ip: 'safe'})

        
        elif option == 'detail':
            if result and result[0] >= 1:
                cursor.execute("SELECT site_id, update_time FROM bad_ip_list WHERE ip = %s", (requested_ip))
                additional_info = cursor.fetchone()
                response_data = {
                    'reputation_result': 'malicious',
                    'site_id': additional_info[0],
                    'update_time': additional_info[1],
                    'reputation_score': 'NULL',
                    'country': 'NULL',
                    'search_count': 'NULL',
                    'domain': 'NULL',
                }
                return jsonify({requested_ip: response_data})
            else:
                response_data = {
                    'reputation_result': 'safe',
                    'site_id': 'NULL',
                    'update_time': 'NULL',
                    'reputation_score': 'NULL',
                    'country': 'NULL',
                    'search_count': 'NULL',
                    'domain': 'NULL',
                }
                return jsonify({requested_ip: response_data})

        return jsonify({'error': 'Invalid option. Please choose either simple or detail.'})

    except Exception as e:
        return jsonify({'Error': str(e)})


@app.route('/get_iplist', methods=['GET'])
def get_iplist():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT ip FROM bad_ip_list")
        ips = [row[0] for row in cursor.fetchall()]

        return jsonify({'ip_list': ips})

    except Exception as e:
        return jsonify({'Error': str(e)})


@app.route('/chart')
def chart1():
	sql="select DATE_FORMAT(update_time,'%%Y-%%M-%%D') m,count(update_time) from bad_ip_list  where ip not like '%%/%%' group by m order by update_time asc;"
	data1=db_class.executeAll(sql)
	sql="select d,count(sub1.d)  from (select distinct ip,DATE_FORMAT(update_time,'%%Y-%%M-%%D') d from bad_ip_list where ip not like '%%/%%' group by ip) sub1 group by d order by STR_TO_DATE(d,'%%Y-%%M-%%D');"
	data2=db_class.executeAll(sql)
	return render_template('graph.html',data1=data1,data2=data2)


@app.route('/data_chart', methods=['GET'])
def draw_graph():
	try:
		sql = "SELECT * FROM ip_count"
		df = db_class.executeAll(sql)
		db_class.commit()

		new_df = df[0]
		date = new_df.get("date")
		count = new_df.get("count")

#		before_one_month = date - relativedelta(months=1)
#		times = np.arange(np.datetime64(before_one_month), np.datetime64(date))


		img = BytesIO()

		plt.figure()
		# times 변수로 x축 -1달전~현재날짜 범위 지정해주기
		plt.plot(date, int(count))
		plt.xticks(rotation=45)
		ax = plt.gca()
		days = mdates.DayLocator()
		ax.xaxis.set_major_locator(days)
		plt.legend(loc="lower left")
		plt.grid(True)
		plt.tight_layout()
		plt.savefig(img, format='png', dpi=300)
		img.seek(0)
		
		return send_file(img, mimetype='image/png')


	except Exception as e:
		return jsonify({'Error': str(e), 'df': df})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)    

    # MariaDB 연결 종료
    db.close()
