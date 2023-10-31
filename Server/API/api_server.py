from flask import Flask, request, make_response, jsonify
import sys
# sys.path.append('/home/teamlab/Thanos/IP/Module/')
# import dbModule
# from IPmaster import ip_shredder
sys.path.append('D:/laBelup/ThanosIP/Module/')
from Module import dbModule
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
                cursor.execute("SELECT site_id, update_time FROM bad_ip_list WHERE ip = %s ORDER BY site_id ASC", (requested_ip))
				additional_info = cursor.fetchone()
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
		# 검색 조회 counting
		# cursor.execute('select ip,count(ip) from bad_ip_list group by ip order by count(ip) desc;')
		# cursor.fetchmany(10)



        return jsonify({'error': 'Invalid option. Please choose either simple or detail.'})

    except Exception as e:
        print(e)
        return jsonify({'Error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)    

    # MariaDB 연결 종료
    db.close()
