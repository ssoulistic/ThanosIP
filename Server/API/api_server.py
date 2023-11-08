from flask import Flask, request, make_response, jsonify,send_file
from flasgger import Swagger
from datetime import datetime
import sys
sys.path.append('/home/teamlab/ThanosIP/Module/')
import dbModule
from IPmaster import ip_shredder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_class=dbModule.Database('laBelup')
ip_test = ip_shredder()

@app.route('/')
def index():
    return make_response(jsonify("connection success",200))


@app.route('/search_ip', methods=['GET'])
def search_ip():

    # client ip 및 검색대상 ip , 시간
    client_ip=request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
    current_time=datetime.now()
    requested_ip = request.args.get('ip')

    # 검색 기록 저장
    insert_data=f'"{client_ip}","{requested_ip}","{current_time}"'
    table_name="search_log"
    db_class.execute(f"insert into {table_name} values({insert_data})")
    db_class.commit()
    option = request.args.get('option')

    # 유효한 IPv4 주소만 추출
    if not ip_test.isip(requested_ip):
        return jsonify({'error': 'Invalid input. Please provide a valid IPv4 address.'})
    
    # DB에 존재여부에 따른 malicious 판별
    result=db_class.executeAll("SELECT COUNT(*) FROM bad_ip_list WHERE ip = %s", (requested_ip))
  
    if option == 'simple':
    
        if result and result[0]['COUNT(*)'] >= 1:
           return jsonify({requested_ip: 'malicious'})
        
        else:
            return jsonify({requested_ip: 'safe'})
    
    elif option == 'detail':
        if result and result[0]['COUNT(*)'] >= 1:
            additional_info=db_class.executeAll("SELECT site_id, update_time FROM bad_ip_list WHERE ip = %s ORDER BY site_id ASC", (requested_ip))
            return jsonify({
                requested_ip: 
                {
                'reputation_result': 'malicious',
                'site_id': additional_info[0],
                'update_time': additional_info[1],
                'reputation_score' : 'NULL',
                'country' : 'NULL',
                'search_count' : 'NULL',
                'domain' : 'NULL',
               }
            })
        else:
            return jsonify({
                requested_ip:
                { 
                'reputation_result':'safe',
                'site_id': 'NULL',
                'update_time': 'NULL',
                'reputation_score' : 'NULL',
                'country' : 'NULL',
                'search_count' : 'NULL',
                'domain' : 'NULL',
                }
            })
    else:
        return jsonify({'error': 'Invalid option. Please choose either simple or detail.'})

@app.route('/worst-ip/<int:num>')
def worst(num):
    result=db_class.executeMany('select ip,count(ip) from bad_ip_list group by ip order by count(ip) desc;',num)
    ranking={}
    for idx,ip in enumerate(result):
        ranking[idx+1]=ip["ip"]
    return jsonify(ranking)

@app.route('/search_rank/<int:num>')
def popular(num):
    result=db_class.executeMany('select target_ip ,count(target_ip) from search_log group by target_ip ORDER BY count(target_ip) DESC;',num)
    ranking={}
    for idx,ip in enumerate(result):
        ranking[idx+1]=ip["target_ip"]
    return jsonify(ranking)

@app.route('/download-ip-list')
def download_ip():
    return send_file("/home/teamlab/ThanosIP/Server/API/data/suspicious_ip_list.txt",mimetype="text/plain",as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)    

