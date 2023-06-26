from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
from bs4 import BeautifulSoup
import csv


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    keyword = '마라탕'

    restaurant_url_list = []  # 식당 url을 저장할 리스트
    try:
        # keyword를 검색한 상태의 네이버 플레이스 url
        naver_map_search_url = f'https://map.naver.com/v5/search/{keyword}/place'
        driver.get(naver_map_search_url)
        time.sleep(5)

        driver.switch_to.frame("searchIframe")  # 페이지 내의 페이지로 driver 이동시키기
        time.sleep(1)

        # while True:
        for _ in range(6):
            try:
                for i in range(50):  # 한 페이지 당 존재하는 식당의 수는 50개로 픽스되어 있음
                    restaurant = driver.find_element(
                        By.XPATH, f'/html/body/div[3]/div/div[3]/div[1]/ul/li[{str(i+1)}]')  # url을 가져올 식당의 li 요소
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", restaurant)  # url을 가져올 식당의 li 요소로 스크롤 이동
                    restaurant.click()
                    time.sleep(3)

                    cu = driver.current_url  # 현재 url 가져오기
                    # 정규표현식을 이용하여 식당의 고유 id 가져오기
                    res_code = re.findall(r"place/(\d+)", cu)
                    final_url = 'https://pcmap.place.naver.com/restaurant/' + \
                        res_code[0] + '/home'  # 식당 url
                    restaurant_url_list.append([final_url])  # 식당 url 리스트에 추가
                    print(final_url)
                print("현재까지 수집된 데이터 개수: ", len(restaurant_url_list))

                next_btn = driver.find_element(
                    By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/a[7]')  # 다음 페이지로 이동하는 버튼 요소
                next_btn.click()
                time.sleep(10)
                print('moved to next page')

            except:
                print("데이터 수집 완료")
                print("전체 데이터 개수: ", len(restaurant_url_list))

                # 결과를 .csv 형태로 저장
                with open("restaurant_url.csv", "w") as f:
                    f.write("url\n")  # column명 지정

                    writer = csv.writer(f)
                    writer.writerows(restaurant_url_list)
                    print("저장 완료")
                break

    except IndexError:
        print('none')


if __name__ == '__main__':
    main()
