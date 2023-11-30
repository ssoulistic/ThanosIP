from flask import Flask, request, make_response, jsonify,send_file, render_template
from flasgger import Swagger,swag_from
from datetime import datetime
from flask_cors import CORS
import sys
# 자체 제작 모듈 경로 추가
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule
from IPmaster import ip_shredder

app = Flask(__name__)
# Cross origin resources(프론트 문제 해결용)
CORS(app)

#명세서 설명 
app.config['SWAGGER']= {
'title':'ThanosIP',
'uiversion':3,
'version':"1.0.3",
'description':"API 명세서입니다.\n\nAPI document for ip_reputation",
}
swagger = Swagger(app)

# 자체 제작 모듈 - db 연동, ip 분별기.
db_class=dbModule.Database('laBelup')
ip_test = ip_shredder()


# 대문
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

# ip 검색 route
@app.route('/search_ip', methods=['GET'])
def search_ip():
    #API 명세서
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
    # client ip, 검색시간, 검색대상 ip 
    client_ip=request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
    current_time=datetime.now()
    requested_ip = request.args.get('ip')

    # 유효한 IPv4 주소만 추출
    if not ip_test.isip(requested_ip):
        return jsonify({'error': 'Invalid input. Please provide a valid IPv4 address.'})

    # 검색 기록 저장
    insert_data=f"'{client_ip}','{requested_ip}','{current_time}'"
    table_name="search_log"
    db_class.execute(f"insert into {table_name} values({insert_data})")
    db_class.commit()
    option = request.args.get('option')

    # DB에 존재여부에 따른 malicious 판별

    # 간단한 검색 - 결과가 존재하면 malicious 판정.
    if option == 'simple':

        result=db_class.executeAll(f"SELECT COUNT(*) FROM bad_ip_list WHERE ip = '{requested_ip}'")
        if result and result[0]['COUNT(*)'] >= 1:
           return jsonify({requested_ip: 'malicious'})

        else:
            return jsonify({requested_ip: 'safe'})

    # 디테일 검색 - 사이트 별로 검색한 기록이 있을 경우 결과를 보여줌.
    elif option == 'detail':
		# 검색할 사이트 목록
    	detail_table=['Abuse_Crawl','BarracudaCentral_Crawl','Criminalip_Crawl','Ipqualityscore_Crawl','Nerd_Crawl','VirusTotal_Crawl']
    	result_all={}
    	count_available=0
		# 사이트 별 결과 존재 여부 확인 
    	for dtable in detail_table:
    		result=db_class.executeAll(f"SELECT * FROM {dtable}  WHERE ip = '{requested_ip}'")
    		if result:
    			result_all[dtable]=result
    		else:
    			count_available+=1

    			result_all[dtable]='No data from Website'
		# 검색 기록모두 없을 시 다른 안내 문구로 전환
    	if count_available==len(detail_table):
    		result_all={f'Submitted':f'{requested_ip} is now on queue for Monthly update\n Thank you for Using our service :D'}
    		exist=db_class.executeAll(f"select * from Search_queue where ip='{requested_ip}'")
			# 검색 우선순위를 위해 검색된 횟수를 기록
    		if exist:	
    			db_class.execute(f"update Search_queue set request_count=request_count+1 where ip='{requested_ip}'")
    		else:
    			db_class.execute(f"insert into Search_queue values('{requested_ip}',1)")
    		db_class.commit()
    		return jsonify(result_all)
    	else:
    		return jsonify(result_all)
    else:
   		return jsonify({'error': 'Invalid option. Please choose either simple or detail.'})

@app.route('/worst-ip/<int:num>')
def worst(num):
    #API 명세서
    """
    API endpoint to get the top {num} worst IPs.

    ---
    tags:
      - IP Search
    parameters:
      - name: num 
        in: path 
        type: integer
        minimum: 1
        required: true
        description: The number of worst IPs to retrieve.

    responses:
      200:
        description: Worst IPs searched.
      

    """
    # ip 저장 횟수를  내림차순으로 ip  목록획득 
    result=db_class.executeMany('select ip,count(ip) from bad_ip_list where ip not like "%%/%%" group by ip order by count(ip) desc;',num)
    ranking={}
    for idx,ip in enumerate(result):
        ranking[idx+1]=ip["ip"]
    return jsonify(ranking)

@app.route('/worst-subnet/<int:num>')
def worst_sub(num):
	
    #API 명세서
    """
    API endpoint to get the top {num} worst subnets.

    ---
    tags:
      - Subnet Search
    parameters:
      - name: num 
        in: path 
        type: integer
        minimum: 1
        required: true
        description: The number of worst Subnets to retrieve.

    responses:
      200:
        description: Worst Subnets searched.
      
	"""

    # subnet 저장 횟수를  내림차순으로 subnet  목록획득 
    result=db_class.executeMany('select ip,count(ip) from bad_ip_list where ip like "%%/%%" group by ip order by count(ip) desc;',num)
    ranking={}
    for idx,ip in enumerate(result):
        ranking[idx+1]=ip["ip"]
    return jsonify(ranking)

@app.route('/search-rank/<int:num>')
def popular(num):
    #API 명세서 
    """
    API endpoint to get the top {num} popular IPs.

    ---
    tags:
      - IP Search
    parameters:
      - name: num
        in: path
        type: integer
        minimum: 1
        required: true
        description: The number of popular IPs to retrieve.

    responses:
      200:
        description: Popular IPs searched.
        
    """
    # ip 검색 수 내림차순 
    result=db_class.executeMany('select target_ip ,count(target_ip) from search_log where target_ip not like "%%/%%"  group by target_ip ORDER BY count(target_ip) DESC;',num)
    ranking={}
    for idx,ip in enumerate(result):
        ranking[idx+1]=ip["target_ip"]
    return jsonify(ranking)

@app.route('/search-rank-subnet/<int:num>')
def popular_subnet(num):
    #API 명세서 
    """
    API endpoint to get the top {num} popular Subnets.

    ---
    tags:
      - Subnet Search
    parameters:
      - name: num
        in: path
        type: integer
        minimum: 1
        required: true
        description: The number of popular Subnets to retrieve.

    responses:
      200:
        description: Popular Subnets searched.
        
    """
    # subnet 검색 수 내림차순 
    result=db_class.executeMany('select target_ip ,count(target_ip) from search_log where target_ip like "%%/%%" group by target_ip ORDER BY count(target_ip) DESC;',num)
    ranking={}
    for idx,ip in enumerate(result):
        ranking[idx+1]=ip["target_ip"]

    return jsonify(ranking)

# 모아둔 iplist를 txt 파일형태로 제공 
@app.route('/download-ip-list')
def download_ip():
    #API 명세서
    """
    API endpoint to download the list of suspicious IPs.

    ---
    tags:
      - IP Download

    responses:
      200:
        description: Download a file containing a suspicious IP list.
    """

    return send_file("/home/teamlab/ThanosIP/Server/API/data/suspicious_ip_list.txt",mimetype="text/plain",as_attachment=True)

@app.route('/chart')
def chart1():
    sql="select DATE_FORMAT(update_time,'%%m-%%d') m,count(update_time) from bad_ip_list  where ip not like '%%/%%' group by m order by update_time asc;"
    data1=db_class.executeAll(sql)
    sql="select d,count(sub1.d)  from (select distinct ip,DATE_FORMAT(update_time,'%%m-%%d') d from bad_ip_list where ip not like '%%/%%' group by ip) sub1 group by d order by STR_TO_DATE(d,'%%m-%%d');"
    data2=db_class.executeAll(sql)
    return render_template('graph.html',data1=data1,data2=data2)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
