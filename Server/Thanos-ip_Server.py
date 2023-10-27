from flask import Flask, request, jsonify
from flasgger import Swagger
import sys
sys.path.append('/home/teamlab/ThanosIP/Module/')
from DB_Module import dataB

app = Flask(__name__)
swagger = Swagger(app)

db = dataB()

@app.route('/')
def index():

    return '''
    <form method="post" action="/check_ip">
        IP 주소 입력: <input type="text" name="ip"><br>
        Option:
        <input type="radio" name="option" value="simple" checked> 간단 검사
        <input type="radio" name="option" value="detail"> 상세 정보 조회<br>
        <input type="submit" value="검색">
    </form>
    '''

@app.route('/check_ip', methods=['GET'])
def check_ip():
    """
    API endpoint to check an IP address.

    ---
    tags:
      - IP Checker
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
        requested_ip = request.form.get('ip')
        option = request.form.get('option')

        if requested_ip is None or not requested_ip.strip():
            return jsonify({'error': 'Invalid input. Please provide a valid IP address.'})

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
                return jsonify({
                    requested_ip: 'malicious',
                    'site_id': additional_info[0],
                    'update_time': additional_info[1]
                })
            else:
                return jsonify({
                    requested_ip: 'safe',
                    'site_id': 'NULL',
                    'update_time': 'NULL'
                })

        return jsonify({'error': 'Invalid option. Please choose either simple or detail.'})

    except Exception as e:
        print(e)
        return jsonify({'Error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)    

    # MariaDB 연결 종료
    db.close()
