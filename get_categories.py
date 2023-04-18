from lib2to3.refactor import MultiprocessRefactoringTool
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

from data_loader import *

import time
import pyautogui
import pyperclip

import pandas as pd
import numpy as np
import pprint

data_loader = Data_Loader()

## 자자, 이제 시작할 때 DB 쭉 확인해서 마지막 꺼부터 해야함
def get_last_data():
    # DB 있는지 확인
    table_name = "categories_naver"

    insp = sa.inspect(data_loader.engine_bridge_data)
    if insp.has_table(table_name, schema="bridge_data"):
        sql = f"select * from `{table_name}` order by `index` desc limit 1"
        temp_data = data_loader.engine_bridge_data.execute(sql).fetchall()
        last_idx = list(temp_data[0])[0] if list(temp_data[0])[1] != "" else -1
        last_data = list(temp_data[0])[1:5]
        last_warning = list(temp_data[0])[5]

        pprint.pprint(temp_data)
        return last_idx, last_data, last_warning
    else:
        temp_df = pd.DataFrame([['', '', '', '', "", ""]], columns=['level_1', 'level_2', 'level_3', 'level_4', 'warning', 'etc'])
        temp_df.to_sql(name = table_name, con=data_loader.engine_bridge_data, if_exists='append')
        # print("없음!")
        return 0, None, None

def handle_modal(driver):
    text = ""
    is_modal = False
    # is_reset = False
    # modal 뜨면 죽여야됨
    ## modal msg 종료 버튼이 두가지 경우로 나옴
    try:
        btn_modal_close = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/button')
        is_modal = True
    except:
        pass
    try:
        btn_modal_close = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div/button')
        is_modal = True
    except:
        pass

    if is_modal:
        time.sleep(0.3)
        for i in range(1, 7):
            try:
                text = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/div[{i}]').text #.text.replace("\n", "")
                if text != "":
                    text = text.replace("\n", "")
                    btn_modal_close.click()
                    time.sleep(0.2)
                    return text
                # print(type(text), text, text == "")
            except:
                pass
    


def handle_modal_auth(driver):
    # ㅈ같은 거 나오면 그걸 밖에다 알려줘야 함
    try:
        # print("이상한거 클릭 전")
        btn_reset_close = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/span[1]/button')
        # is_reset = True
        btn_reset_close.click()
        # print("이상한거 클릭 후")
        return "reset"
    except:
        return ""



def select_text(msg_list):
    text = ''
    for msg in msg_list:
        if msg != '':
            text = msg
    return text

def default_setting():
    # 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # 불필요한 에러 메시지 없애기
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 주소 이동
    driver.implicitly_wait(0.2)
    # driver.maximize_window()
    # driver.get("https://www.naver.com")
    driver.get("https://sell.smartstore.naver.com/#/products/create")

    # 로그인 페이지로 넘어가는 시간
    driver.implicitly_wait(2)

    # 팝업창 대비
    main_page = driver.current_window_handle

    # 네이버 ID로 로그인 버튼 누르기
    btn_naver_id = driver.find_element(By.CSS_SELECTOR, ".Login_btn_more__1pQwH")
    # print(btn_naver_id)
    btn_naver_id.click()
    driver.implicitly_wait(0.2)

    # changing the handles to access login page
    for handle in driver.window_handles:
        if handle != main_page:
            login_page = handle
            
    # change the control to signin page        
    driver.switch_to.window(login_page)

    # 로그인
    id = driver.find_element(By.CSS_SELECTOR, "#id.input_text")
    id.click()
    pyperclip.copy("bridgers")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.56)

    pw = driver.find_element(By.CSS_SELECTOR, "#pw.input_text")
    pw.click()
    pyperclip.copy("ehsqjftlrks1!")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.34)

    btn_login = driver.find_element(By.CSS_SELECTOR, ".btn_login")
    btn_login.click()

    # 로그인 완료 대기
    time.sleep(3)

    # 로그인 완료 후 판매자 센터 등록 페이지로 넘어옴, driver 거기에 맞춰주기
    # main_page 재설정
    main_page = driver.window_handles[0]
    driver.switch_to.window(main_page)

    return driver

def category_search_loop(driver):
    # DB 상의 마지막 데이터 확인
    last_idx, last_data, last_warning = get_last_data()
    print(f"last_data: {last_data}")
    warning_msg = ['', '', '', '']
    start_check = False if last_data[0] != '' else True

    # 카테고리명 선택 버튼 클릭
    btn_select_cat = driver.find_element(By.XPATH, '//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div/div/category-search/div[1]/div[1]/div/label[2]')
    btn_select_cat.click()

    # 1단계 카테고리 리스트 수집
    cat1_list_elements = driver.find_elements(By.XPATH, '//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div/div/category-search/div[3]/div[1]/ul/li')
    cat1_list = [element.text for element in cat1_list_elements]
    # print(cat1_list)

    # 버튼 하나하나 클릭해보기
    for element1 in cat1_list_elements:
        el1_text = element1.text
        if not start_check:
            if last_data[0] != '' and last_data[0] != element1.text:
                continue
        
        warning_msg[0] = ''
        element1.click()
        time.sleep(0.3)
        # driver.implicitly_wait(5)

        modal_msg = handle_modal(driver)
        # handle_modal_auth(driver)
        if modal_msg:
            warning_msg[0] = modal_msg
            print(modal_msg)

        cat2_list_elements = driver.find_elements(By.XPATH, '//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div[2]/ul/li')
        for element2 in cat2_list_elements:
            el2_text = element2.text
            if element2.text == "":
                continue
            if not start_check:
                if last_data[1] != '' and last_data[1] != element2.text:
                    continue
            print(element2.text)

            warning_msg[1] = ''

            # print(element2.get_attribute('innerHTML'))
            element2.click()
            time.sleep(0.3)

            # modal 뜨면 죽여야됨
            modal_msg = handle_modal(driver)
            modal_msg_auth = handle_modal_auth(driver)
            if modal_msg:
                warning_msg[1] = modal_msg
                print(modal_msg)
                if modal_msg_auth == "reset":
                    last_idx = last_idx + 1
                    temp_df = pd.DataFrame([[el1_text, el2_text, el2_text, el2_text, modal_msg_auth, ""]],
                                            columns=['level_1', 'level_2', 'level_3', 'level_4', 'warning', 'etc'],
                                            index=[last_idx])
                    temp_df.to_sql(name = "categories_naver", con=data_loader.engine_bridge_data, if_exists='append')
                    return "reset"


            cat3_list_elements = driver.find_elements(By.XPATH, '//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div[3]/ul/li')
            for element3 in cat3_list_elements:
                el3_text = element3.text
                if el3_text == "비타민제":
                    print()
                if element3.text == "":
                    continue
                if not start_check:
                    if last_data[2] != '' and last_data[2] != element3.text:
                        continue
                    elif last_warning == "reset" and last_data[2] == last_data[3]:
                        start_check = True
                        last_warning = ""
                        continue
                # if element3.text in ["", "수지침", "파라핀용품", "심박계", "청진기", "혈압계"] or not start:
                #     continue
                print(element3.text)

                warning_msg[2] = ''

                element3.click()
                time.sleep(0.3)

                # modal 뜨면 죽여야됨
                modal_msg = handle_modal(driver)
                modal_msg_auth = handle_modal_auth(driver)
                # print(f"modal_msg_auth: {modal_msg_auth}")
                if modal_msg:
                    warning_msg[2] = modal_msg
                    print(modal_msg)
                if modal_msg_auth == "reset":
                    last_idx = last_idx + 1
                    temp_df = pd.DataFrame([[el1_text, el2_text, el3_text, el3_text, modal_msg_auth, ""]],
                                            columns=['level_1', 'level_2', 'level_3', 'level_4', 'warning', 'etc'],
                                            index=[last_idx])
                    temp_df.to_sql(name = "categories_naver", con=data_loader.engine_bridge_data, if_exists='append')
                    pprint.pprint(temp_df)

                    return "reset"

                cat4_list_elements = driver.find_elements(By.XPATH, '//*[@id="productForm"]/ng-include/ui-view[3]/div/div[2]/div/div[1]/div/category-search/div[3]/div[4]/ul/li')
                for element4 in cat4_list_elements:
                    if element4.text == "":
                        continue
                    
                    if element4.text == "세분류":
                        el4_text = element3.text
                    else:
                        el4_text = element4.text
                    
                    if el4_text == "기타비타민":
                        print()

                    if not start_check:
                        if last_data[3] != '' and last_data[3] != el4_text:
                            continue
                        elif last_warning == "reset":
                            start_check = True
                            last_warning = ""
                            continue
                    print(f"element4.text: {element4.text}")

                    if element4.text == "":
                        continue



                    warning_msg[3] = ''

                    element4.click()
                    time.sleep(0.1)
                    # modal 뜨면 죽여야됨
                    modal_msg = handle_modal(driver)
                    # modal_msg = handle_modal(driver)
                    modal_msg_auth = handle_modal_auth(driver)
                    if modal_msg:
                        warning_msg[3] = modal_msg
                        print(modal_msg)
                    
                    warning_msg_final = select_text(warning_msg)
                    if modal_msg_auth == "reset":
                        warning_msg_final = modal_msg_auth

                    # 맨 처음 왔을 때는 중복 못 잡았음, 한 턴 쉬고
                    if start_check:
                        last_idx = last_idx + 1
                        temp_df = pd.DataFrame([[el1_text, el2_text, el3_text, el4_text, warning_msg_final, ""]],
                        columns=['level_1', 'level_2', 'level_3', 'level_4', 'warning', 'etc'],
                        index=[last_idx])
                        temp_df.to_sql(name = "categories_naver", con=data_loader.engine_bridge_data, if_exists='append')
                        # print(warning_msg)
                    start_check = True

                    # pprint.pprint(temp_df)

                    if modal_msg_auth == "reset":
                        return "reset"




            #     print(element3.text)


driver = default_setting()
while True:
    category_search_loop(driver)