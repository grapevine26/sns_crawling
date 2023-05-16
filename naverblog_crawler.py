# -*- coding: utf-8 -*-
import time
import urllib.request as urls
from bs4 import BeautifulSoup
from chrome_driver import ChromeDriver
from database import insert
import datetime


def start():
    # 드라이버
    chrome_driver = ChromeDriver()
    chrome_driver.headless()
    driver = chrome_driver.ready()
    driver.get('https://blog.naver.com/')
    return driver


def naverblog_crawler_start(driver, page_id, return_dict):
    if page_id:
        try:
            start_time_all = time.time()
            db_insert = insert.Insert()

            try:
            # xml href 가져오기
                driver.get('https://blog.naver.com/' + page_id)
                time.sleep(2)
                blog_xml = driver.find_element_by_css_selector('link:nth-of-type(2)').get_attribute('href')
            except Exception as e:
                print('*[naver] error2 :', e)
                return
            response = urls.urlopen(blog_xml)
            soup = BeautifulSoup(response, "html.parser")
            ############################################################################################################
            # 게시물
            ############################################################################################################
            post_list = []
            # findAll로 해당되는 TAG를 검색
            for songElement in soup.findAll('item'):
                description = str(songElement.description.string)
                date = str(songElement.pubdate.string)
                if date:
                    date = date.split()[1:4]
                    month = datetime.datetime.strptime(date[1], "%b")
                    date = date[2] + '-' + str(month.month) + '-' + date[0]
                else:
                    date = None
                if description.replace(' ', ''):
                    print(description)
                    return_dict.append(description)
                    post_list.append(description)
            # return_dict.append(post_list)
            print('네이버 게시글 수 ', len(post_list))
            print('네이버 게시글 수 ', len(return_dict))
            print('NaverBlog 크롤링 총 구동 시간 :', time.time() - start_time_all)
            driver.quit()
        except Exception as e:
            return_dict.append('naver_error')
            print('naver_error', e)


if __name__ == '__main__':
    driver = start()
    naverblog_crawler_start(driver, 'ok3mam', {})
