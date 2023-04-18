from datetime import datetime

# db 계정
# db_id = 'root'
db_id = 'yush0123'
# db ip
db_ip = 'localhost'
# db 패스워드
# db_passwd = 'yu9517'
db_passwd = 'yu3290587873!'
# db_passwd = ''

# db port.
db_port = '3306'

timeout_ms = 1000
time_sleep_collecting = 1
time_sleep_trading = 0.1

# 크롤링 시작 시간, UTC ms integer
start_time_timestamp_ms = int(datetime.strptime('2020_01_01_00_00_00+0000', '%Y_%m_%d_%H_%M_%S%z').timestamp() * 1000)
# BUSD 용
# start_time_timestamp_ms = int(datetime.strptime('2021_07_01_00_00_00+0000', '%Y_%m_%d_%H_%M_%S%z').timestamp() * 1000)

# OLD
# start_time_timestamp_ms = int(datetime.strptime('2018_08_01_00_00_00+0000', '%Y_%m_%d_%H_%M_%S%z').timestamp() * 1000)
# start_time_timestamp_ms = int(datetime.strptime('2022_02_03_00_00_00+0000', '%Y_%m_%d_%H_%M_%S%z').timestamp() * 1000)





# openapi 1회 조회 시 대기 시간(0.2 보다-> 0.3이 안정적)
TR_REQ_TIME_INTERVAL = 0.25

# n회 조회를 1번 발생시킨 경우 대기 시간
TR_REQ_TIME_INTERVAL_LONG = 15

# api를 최대 몇 번까지 호출 하고 봇을 끌지 설정 하는 옵션
max_api_call = 999

