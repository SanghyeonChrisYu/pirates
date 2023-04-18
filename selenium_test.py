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
driver.implicitly_wait(2)
driver.maximize_window()
driver.get("https://www.naver.com")
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")

# 아이디 입력창
id = driver.find_element(By.CSS_SELECTOR, "#id")
id.click()
pyperclip.copy("yush0123")
pyautogui.hotkey('ctrl', 'v')
# id.send_keys("yush0123")
time.sleep(1.1)


# 비밀번호 입력창
pw = driver.find_element(By.CSS_SELECTOR, "#pw")
pw.click()
pyperclip.copy("yu3290587873!?")
pyautogui.hotkey('ctrl', 'v')
# pw.send_keys("yu3290587873!?")
time.sleep(0.7)

btn_login = driver.find_element(By.CSS_SELECTOR, "#log\.login")
btn_login.click()

id.send_keys(Keys.ENTER)

