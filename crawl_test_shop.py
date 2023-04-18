# from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 주소 이동
driver.implicitly_wait(0.7)
driver.maximize_window()

keyword = "아이폰13"
driver.get(f"https://search.shopping.naver.com/search/all?query={keyword}&cat_id=&frm=NVSHATC")

# 스크롤 끝까지 내려서 데이터 로드
before_h = driver.execute_script("return window.scrollY")
while True:
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

    time.sleep(1)

    after_h = driver.execute_script("return window.scrollY")

    if after_h == before_h:
        break
    before_h = after_h
    
