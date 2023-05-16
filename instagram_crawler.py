# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chrome_driver import ChromeDriver
from database import insert, update, select
import unicodedata
import re


def start():
        # 드라이버
        chrome_driver = ChromeDriver()
        # chrome_driver.headless()
        chrome_driver.mobile_emulation()
        driver = chrome_driver.ready()

        # SNS 페이지 접속
        driver.get('https://m.instagram.com/accounts/login/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))

        # SNS 로그인
        driver.find_element_by_name('username').send_keys('01053474109')
        # driver.find_element_by_name('username').send_keys('kimtheho')
        time.sleep(1)
        driver.find_element_by_name('password').send_keys('4109121zZ#!')
        # driver.find_element_by_name('password').send_keys('7788@E2e')
        time.sleep(2)
        driver.find_element_by_css_selector('button[type="submit"]').click()
        driver.save_screenshot('insta1.png')
        # SNS 크롤링 시작
        time.sleep(5)
        return driver
        #
        # try:
        #     time.sleep(2)
        #     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'main[role="main"]')))
        #     return driver
        # except Exception as e:
        #     try:
        #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".PCQoG")))
        #         return driver
        #     except Exception as e:
        #         raise e


def instagram_crawler_start(driver, page_id, return_list):
    print(type(return_list))

    if page_id:
        try:
            print(123)
            start_time_all = time.time()
            # try:
            print(driver)
            driver.get('https://m.instagram.com/' + page_id)
            print(page_id)
            time.sleep(2)
            # except Exception as e:
            #     # 페이지없음
            #     try:
            #         error = driver.find_element_by_css_selector('div._7UhW9.vy6Bb.MMzan.KV-D4.uL8Hv.l4b0S').text
            #         print('*[Instagram] error2 :', error, e)
            #     except Exception as e:
            #         error = driver.find_element_by_css_selector('.error-container').text
            #         print('*[Instagram] error2 :', error, e)
            #     return

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                # 공개 비공개
                check = driver.find_element_by_css_selector('div[role="tablist"]').text
                opened = True
            except Exception as e:
                opened = None

            try:
                # 게시물 수
                post_cnt = int(soup.select_one("main > div > ul > li:nth-of-type(1) span > span").text.replace(',', ''))
            except Exception as e:
                try:
                    post_cnt = int(soup.select_one("li:nth-of-type(1) > span > span").text.replace(',', ''))
                except Exception as e:
                    post_cnt = 0
            print('인스타 게시글 수 :', post_cnt)

            try:
                # 팔로워 수
                follower_cnt = int(
                    soup.select_one("main > div > ul > li:nth-of-type(2) span")['title'].replace(',', ''))
            except Exception as e:
                try:
                    follower_cnt = int(soup.select_one("li:nth-of-type(2) > span > span")['title'].replace(',', ''))
                except Exception as e:
                    follower_cnt = 0
            print('인스타 팔로워 수 :', follower_cnt)

            post_list = []
            post_like_cnt = 0
            # time.sleep(500)
            if opened:
                # 스크롤내리는 횟수
                scroll_count = 5
                # 중복 href 카운트
                same_count = 0
                # 게시글마다 href 를 담을 리스트
                href = []
                try:
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    # print(last_height)
                    for i in range(0, scroll_count):
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        href_html = soup.select('article > div > div > div a')
                        for href_list in href_html:
                            if href_list['href'] in href:
                                same_count += 1
                            else:
                                href.append(href_list['href'])
                        print(
                            "Scrolling... " + str(i + 1) + "/" + str(scroll_count) + ", 현재: " + str(len(href)) + ", 중복: " + str(
                                same_count))

                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height
                    # print(str(len(href)) + "개의 결과를 찾았습니다.")
                except Exception as e:
                    print('스크롤', e)
                    href = None

                if href:
                    for i in href:
                        user_url = "https://www.instagram.com" + i
                        driver.get(user_url)
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._aaqw")))
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        try:
                            post_like_cnt += int(soup.select_one('section._ae5m span').text.replace(',', ''))
                        except Exception as e:
                            post_like_cnt = 0
                    print('인스타 좋아요 수', post_like_cnt)
                    re_ = re.compile('#([가-힣ㄱ-ㅎa-zA-Z0-9]?\w+)')
                    for i in href:
                        user_url = "https://www.instagram.com" + i + "comments"
                        driver.get(user_url)
                        time.sleep(2)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')

                        try:
                            # post_text = soup.select_one('main > div > ul > div:nth-of-type(1) span').text
                            post_text = soup.select_one('main > div > ul > div:nth-of-type(1) h1').text
                            print(post_text)
                            if post_text:
                                post_text = unicodedata.normalize('NFC', post_text)
                                tags = re_.findall(post_text)
                                post_text = re_.sub('', post_text)
                                return_list.append(post_text)
                        except Exception as e:
                            print('instagram', e)

                print('Instagram 크롤링 총 구동 시간 :', time.time() - start_time_all)
                driver.quit()
            else:
                driver.quit()
        except Exception as e:
            print('instagram_error', e)
            return_list.append('instagram_error')
            driver.quit()


if __name__ == '__main__':
    in_driver = start()
    if type(in_driver) is not str:
        instagram_crawler_start(in_driver, 'whitehouseboy', {})
        # instagram_crawler_start(in_driver, 'hoo_nie', {})
