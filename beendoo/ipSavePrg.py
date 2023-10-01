# ipSavePrg.py
# ip 리스트 파일을 불러와 악성 ip 여부를 DB에 저장하는 프로그램
# EC2 우분투 서버에서 실행될 코드

import os
import dbModule
import datetime


# MariaDB 연결
DB_name="testlab" # 사용할 Database 이름
table_name="ipSaveTable" # 사용할 Table 이름
db_class = dbModule.Database(DB_name) # db 인스턴스

# ipList 폴더의 파일들 리스트/변수화
fileList = os.listdir("./ipList/")
print(fileList)

# ipList 폴더의 파일들 하나씩 읽음
i = 0
# ip 리스트 파일 제목 참고하여 출처 파악
ip_from = '"'+fileList[i]+'"'
while i < len(fileList):
    # (정규화된) ip 리스트 파일 오픈
    f = open("./ipList/"+fileList[i], "r")
    print(fileList[i])

    while True :
        ipList = f.readlines()
        if not ipList : break

        # while문으로 ip 한줄씩 읽으면서 테이블 컬럼 양식에 맞게 저장
            # ip, 악성여부 True/False, ip 파일 출처(근거), DB에 저장되는 시간
            # ipList의 ip 한줄씩 가져와서 행 조합 후 DB에 저장
        p = 0
        while p < len(ipList):
            ip = ipList[p]
            reputation_score = "True"
            update_time = datetime.datetime.now()
            insert_data = f'"{ip}","{reputation_score}","{ip_from}","{update_time}"'
                
            searchSql = f'SELECT ip FROM {table_name}'
            db_class.execute(searchSql)
            print("중간확인")
            result = db_class.fetchall()
            print(result)

            if result == None:
                # ip가 존재하지 않으면 DB에 입력 INSERT
                sql = f'INSERT INTO {table_name} VALUES({insert_data})' # SQL 쿼리문 => select,insert 모두 가능한데 지금은 입력만
            else:
                if ip == result[0]:
                    # ip가 이미 존재한다면 뒤의 3데이터만 덮어쓰기 UPDATE
                    sql = f'UPDATE {table_name} SET reputation_score = {reputation_score}, ip_from = {ip_from}, update_time = {update_time}'
                else:
                    sql = f'INSERT INTO {table_name} VALUES({insert_data})' # SQL 쿼리문 => select,insert 모두 가능한데 지금은 입력만
            
            db_class.execute(sql) # db에 sql문 작성
            db_class.commit() #sql문 실행
        
            # while문 p값 증가
            p += 1
        
        # 안쪽 while문 i값 증가
        i += 1

    # 바깥쪽 while문 i값 증가
        i += 1


# ip 리스트 파일 닫기
f.close()

# MariaDB 연결 종료

