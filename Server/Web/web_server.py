from flask import Flask,render_template
import sys
sys.path.append('/home/teamlab/ThanosIP/Module/')
import IPmaster
from flask_cors import CORS
# import requests
import logging


### 추가 부분 ###

app = Flask(__name__,static_url_path='/static')
CORS(app)
ip_test=IPmaster.ip_shredder()

app.debug=False
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler # logging 핸들러 이름을 적어줌
    file_handler = RotatingFileHandler('test.log', maxBytes=2000, backupCount=10) 
    file_handler.setLevel(logging.WARNING) # 어느 단계까지 로깅을 할지를 적어줌
    app.logger.addHandler(file_handler) # app.logger.addHandler() 에 등록시켜줘야 app.logger 로 사용 가능


# from logging.handlers import SysLogHandler 유닉스 계열 시스템의 syslog 남김.


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('/error-page.html') 


@app.route("/")
def home():
    return render_template('/home.html')

@app.route("/ip-search")
def search_home():
    return render_template('/search-home.html')

@app.route("/ip-search/<ip>")
def seek(ip):
    if ip_test.isip(ip):
        return render_template('/ip-search.html',search=ip)
    else:
        return error_page()

@app.route("/error-page")
def error_page():
    return render_template('/error-page.html')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5100, debug=True)
