# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chrome_driver import ChromeDriver, auto_scroll
from bs4 import BeautifulSoup
import re
from database import insert, update, select
import datetime


def start():
    # 드라이버
    chrome_driver = ChromeDriver()
    # chrome_driver.mobile_emulation()
    # chrome_driver.headless()
    driver = chrome_driver.ready()

    # SNS 페이지 접속
    driver.get('https://facebook.com')
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))

    fb_acc = [
        {'id': 'yifi1004@gmail.com', 'pw': '4109121zZ#!'},
        {'id': 'idkimtheho@gmail.com', 'pw': '7788@E2e7'}
    ]

    driver.find_element_by_name('email').send_keys(fb_acc[0]['id'])
    driver.find_element_by_name('pass').send_keys(fb_acc[0]['pw'])
    driver.find_element_by_name('login').click()

    # try:
    #     WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#checkpointSubmitButton")))
    #     driver.find_element_by_css_selector('#checkpointSubmitButton > button').click()
    # except Exception as e:
    #     pass
    # time.sleep(500)
    # SNS 크롤링 시작
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ssrb_top_of_home_end")))
        return driver
    except Exception as e:
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._5yd0")))
            error = driver.find_element_by_css_selector('div._5yd0').text
            print('fb error1', error)
        except Exception as error:
            print('fb error2', error)
        print('*[Facebook] Login error :', e)
        return 'err'


def facebook_crawler_start(driver, page_id, return_dict):
    if page_id:
        try:
            start_time_all = time.time()
            driver.get('https://facebook.com/'+page_id)
            html_soup = auto_scroll(driver, scroll_count=5)
            articles = html_soup.find_all('div', {'role': 'article'})
            for article in articles:
                links = article.find_all('a', {'role': 'link'})
                for link in links:
                    print(link['href'])

            time.sleep(1200)
            # 친구수
            try:
                friends = html_soup.select('#screen-root > div > div:nth-child(2) > div:nth-child(6) > div:nth-child(2) > div:nth-child(2) > div').text
                print(friends)
                friend_cnt = re.sub('[A-Za-z가-힣, ]\w+', '', friends)
                if not friend_cnt:
                    friend_cnt = 0
            except Exception as e:
                print('친구 수 :', e)
                friend_cnt = 0
            print("친구 수 :", friend_cnt)
            # time.sleep(123)

            # 각 게시글 주소 가져오기
            article_list = html_soup.select('section > article')
            post_href_list = list()
            post_list = []
            for i in article_list:
                try:
                    post_href = i.select_one('div.story_body_container > div:nth-of-type(1) > a ')['href']
                    post_href_list.append(post_href)
                    print(1)
                except Exception as e:
                    print(2)
                    try:
                        post_href = i.select_one('div.story_body_container > div:nth-of-type(1) > div:nth-of-type(1) > a ')[
                            'href']
                        post_href_list.append(post_href)
                    except Exception as e:

                        print('article error :', e)
            print('게시글 수 :', len(post_href_list))
            post_like_cnt = 0
            reply_cnt = 0
            for i in post_href_list:
                driver.get('https://www.facebook.com/' + i)
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "footer")))
                    try:
                        date = driver.find_elements_by_tag_name('abbr')[0].text
                        if '년' in date:
                            date = date.replace('년 ', '-').replace('월 ', '-').replace('일', '').split()[0]
                        else:
                            date = date.replace('월 ', '-').replace('일', '').split()[0]
                            date = str(datetime.datetime.now().year) + '-' + date
                    except Exception as e:
                        date = None
                    # 본문
                    try:
                        post_text = driver.find_element_by_css_selector('div.story_body_container > div').text
                        return_dict.append(post_text)
                    except Exception as e:
                        post_text = ''

                    # 좋아요
                    try:
                        post_like = driver.find_element_by_css_selector(
                            'div#m_story_permalink_view > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(2)').text
                        post_like_cnt += int(re.search('[0-9]+', post_like).group())
                    except Exception as e:
                        print('좋아요 error', e)

                    # 댓글
                    try:
                        comment_list = driver.find_elements_by_css_selector('div._2a_i')
                        reply_cnt += len(comment_list)
                    except Exception as e:
                        print('댓글 error', e)

                except Exception as e:
                    print('facebook post error :', e)
            print('좋아요 수 :', post_like_cnt)
            print('댓글 수 :', reply_cnt)

            # 사진수
            photo_cnt = 0
            try:
                driver.get('https://m.facebook.com/profile.php?v=photos&id=' + page_id)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
                # 앨범 더 보기
                try:
                    driver.find_element_by_id('m_more_albums').click()
                except Exception as e:
                    pass

                html_soup = BeautifulSoup(driver.page_source, 'html.parser')

                albums = []
                try:
                    albums_list = html_soup.select('a.primary')
                    for i in albums_list:
                        albums.append(i['href'])
                    for j in albums:
                        driver.get('https://m.facebook.com' + j)
                        try:
                            WebDriverWait(driver, 2).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div._8brv")))
                            html_soup = auto_scroll(driver, scroll_count=5)
                            photo = html_soup.select('div#rootcontainer a img')
                            photo_cnt += len(photo)

                        except Exception as e:
                            html = driver.page_source
                            html_soup = BeautifulSoup(html, 'html.parser')
                            photo = html_soup.select('div#rootcontainer a img')
                            photo_cnt += len(photo)
                except Exception as e:
                    print('사진 없음', e)
            except Exception as e:
                photo_cnt = 0
            print("사진 수 :", photo_cnt)
            driver.quit()
        except Exception as e:
            return_dict.append('facebook_error')
            print('facebook_error', e)
            driver.quit()

if __name__ == '__main__':
    driver = start()
    facebook_crawler_start(driver, 'chon.seungil', {})
