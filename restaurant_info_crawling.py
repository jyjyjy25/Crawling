from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
from tqdm import tqdm
import csv
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

rest_url_list = pd.read_csv("./restaurant_url.csv")
for r in tqdm(rest_url_list['url']):
    print(r)
    driver.get(r)
    time.sleep(3)

    # 식당 이름 #
    r_name = driver.find_element(
        By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/span[1]').text

    # 식당 별점 #
    try:
        r_rank_report = driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/div[2]/span[1]/em').text
        # r_rank_report = float(out[0].split('\n')[1].split('/')[0]) # 별점을 실수형으로 바꿔서 담아둔다
    except:
        r_rank_report = 0

    # 식당 주소 #
    r_address = driver.find_element(By.CLASS_NAME, 'LDgIH').text

    # 식당 전화번호 #
    r_phone_num = driver.find_element(By.CLASS_NAME, 'xlx7Q').text

    # 식당 영업시간 #
    r_opening_hours = ''
    more_btn = driver.find_element(
        By.CLASS_NAME, 'gKP9i.RMgN0')
    driver.execute_script("arguments[0].click();", more_btn)
    weeks = driver.find_elements(
        By.CLASS_NAME, 'A_cdD')[1:]
    for w in weeks:
        r_opening_hours = r_opening_hours + w.text + '\n'

    # 식당 메뉴 #
    r_menus = []
    try:  # 메뉴 더보기 버튼이 존재하는 경우
        menu_btn = driver.find_element(By.CLASS_NAME, 'fvwqf')
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", menu_btn)
        menu_btn.click()
        time.sleep(3)
        # if:  # 네이버 주문이 존재하는 경우

        # else:  # 네이버 주문이 존재하지 않는 경우
        menus = driver.find_elements(
            By.XPATH, '/html/body/div[3]/div/div/div/div[7]/div[2]/div[1]/div/ul/li')
        for i in range(len(menus)):
            r_menu_name = driver.find_element(
                By.XPATH, f'/html/body/div[3]/div/div/div/div[7]/div[2]/div[1]/div/ul/li[{str(i+1)}]/a/div[2]/div[1]/div/span[1]').text

            divs = driver.find_elements(
                By.XPATH, f'/html/body/div[3]/div/div/div/div[7]/div[2]/div[1]/div/ul/li[{str(i+1)}]/a/div[2]/div')
            if len(divs) == 2:  # 메뉴 설명이 없는 경우
                r_menu_description = ''
                r_menu_price = driver.find_element(
                    By.XPATH, f'/html/body/div[3]/div/div/div/div[7]/div[2]/div[1]/div/ul/li[{str(i+1)}]/a/div[2]/div[2]').text
            else:  # 메뉴 설명이 있는 경우
                r_menu_description = driver.find_element(
                    By.XPATH, f'/html/body/div[3]/div/div/div/div[7]/div[2]/div[1]/div/ul/li[{str(i+1)}]/a/div[2]/div[2]').text
                r_menu_price = driver.find_element(
                    By.XPATH, f'/html/body/div[3]/div/div/div/div[7]/div[2]/div[1]/div/ul/li[{str(i+1)}]/a/div[2]/div[3]').text
            r_menus.append([r_menu_name, r_menu_description, r_menu_price])
    except:  # 메뉴 더보기 버튼이 존재하지 않는 경우
        menus = driver.find_elements(By.CLASS_NAME, 'gHmZ_')
        for _ in range(len(menus)):  # 메뉴 개수만큼 리스트 생성
            r_menus.append([])

        r_menus_name = driver.find_elements(
            By.CLASS_NAME, 'place_bluelink.ihmWt')
        for i, m in enumerate(r_menus_name):
            r_menus[i].append(m.text)

        for i in range(len(menus)):
            r_menus[i].append('')

        r_menus_price = driver.find_elements(By.CLASS_NAME, 'awlpp')
        for i, m in enumerate(r_menus_price):
            r_menus[i].append(m.text)
        # exit()

    print(r_name, r_address, r_phone_num,
          r_opening_hours, r_rank_report, r_menus)
    # exit()
