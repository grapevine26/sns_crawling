# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chrome_driver import ChromeDriver, auto_scroll
from bs4 import BeautifulSoup
from database import insert, update, select


def start():
    # 드라이버
    chrome_driver = ChromeDriver()
    # chrome_driver.headless()
    driver = chrome_driver.ready()

    # SNS 페이지 접속
    driver.get('https://accounts.kakao.com/login/kakaostory')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
    # time.sleep(10)
    # SNS 로그인
    # driver.find_element_by_class_name('recaptcha-checkbox-border').click()
    driver.find_element_by_id('loginKey--1').send_keys('yifi1004@gmail.com')
    # driver.find_element_by_name('email').send_keys('kimtheho@hanmail.net')
    driver.find_element_by_id('password--2').send_keys('4109121zZ#!')
    # driver.find_element_by_name('password').send_keys('77882e2e')
    driver.find_element_by_css_selector('.confirm_btn > .btn_g').click()
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#kakaoContent")))
        return driver
    except Exception as e:
        try:
            error = driver.find_element_by_css_selector('div#errorAlert').text
            print('*[KakaoStory] error :', error, e)
        except Exception as e:
            print('kakao', e)
        driver.quit()
        return 'err'


def kakao_story_crawler_start(driver, page_id, return_dict):
    if page_id and page_id != '0':
        try:
            start_time_all = time.time()
            try:
                driver.get('https://story.kakao.com/' + page_id)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed")))
            except Exception as e:
                error = driver.find_element_by_css_selector('.desc_error').text
                print('*[kakaostroy] error2 :', error, e)
                return
            post_soup = auto_scroll(driver, scroll_count=5)

            # 게시글
            post_list = post_soup.select('div.section._activity')
            comment_href_list = list()
            post_list_ = []
            for i in post_list:
                post_date = i.select_one('div > .add_top > p > a')

                # 리플 페이지 리스트
                comment_href_list.append(post_date['href'])
                # 본문
                try:
                    post_text = i.select_one('.txt_wrap').text
                    post_text = post_text.replace('\xa0', '')
                    return_dict.append(post_text)
                except Exception as e:
                    print('kakao', e)

            reply_cnt = 0
            # 댓글
            for i in comment_href_list:
                driver.get('https://story.kakao.com' + i)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.detail_desc")))
                try:
                    comment_count = int(driver.find_element_by_class_name('_commentCount').text)
                    if comment_count != 0:
                        comment_more_click = 4
                        for j in range(0, comment_more_click):
                            try:
                                driver.find_element_by_class_name('_btnShowPrevComment').click()
                                time.sleep(1)
                                style = driver.find_element_by_class_name('_showPrevCommentContainer').get_attribute(
                                    'style')
                                if style == 'display: none;':
                                    break
                            except Exception as e:
                                break

                    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    comment_list = html_soup.select('ul._listContainer > li')
                    reply_cnt += len(comment_list)
                except Exception as e:
                    print('댓글 없음', e)
            print('카카오 댓글 수', reply_cnt)
            print('카카오 게시글 수 ', len(post_list))
            print('KakaoStory 크롤링 총 구동 시간 :', time.time() - start_time_all)
            driver.quit()
        except Exception as e:
            return_dict.append('kakaostory_error')
            print('kakaostory_error', e)
            driver.quit()

if __name__ == '__main__':
    driver = start()
    kakao_story_crawler_start(driver, '092kiss', {})
