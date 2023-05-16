# -*- coding: utf-8 -*-
"""
크롬 드라이버 설정
"""
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

class ChromeDriver:
    def __init__(self):
        """
        Option
        user-agent : 사용자 정보 설정
        --window-size : 브라우저 사이즈 설정 ex) "1920, 1080", "1280, 1024", "800, 600"
        --lang : 브라우저 언어 설정 ex) "ko", "eu-us", "jp"
        """

        # ua = UserAgent(verify_ssl=False)
        self.options = Options()
        # self.options.add_argument('user-agent='+ua.random)
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        )
        # self.options.add_argument(
        #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        # )
        self.options.add_argument("--window-size=1920, 1080")
        self.options.add_argument("--lang=eu-us")
        # self.options.add_argument("--auto-open-devtools-for-tabs")
        self.options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    def headless(self):
        """
        --headless : 브라우저(창) 숨김
        --disable-gpu : 그래픽카드 사용 안함
        """
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')

    def mobile_emulation(self):
        """
        모바일 버전으로 설정
        """
        mobile_emulation = {"deviceName": "iPhone 8 Plus"}
        self.options.add_experimental_option("mobileEmulation", mobile_emulation)

    def ready(self):
        """
        크롬 브라우저 준비
        :return: 웹을 실행시킬 크롬 드라이버 리턴
        """
        # driver = webdriver.Remote('http://localhost:4444/wd/hub', DesiredCapabilities.CHROME, options=self.options)
        driver = webdriver.Chrome(options=self.options, executable_path=ChromeDriverManager().install())
        return driver


def auto_scroll(driver, scroll_count):
    """
    :param driver: 크롬 브라우저가 켜져있는 상태에서 드라이버를 인자 값으로 받음
    :param scroll_count: 스크롤 횟수
    :return: BeautifulSoup 객체를 리턴
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")

        # 스크롤이 더 이상 내려가지 않을 경우 브레이크
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return soup
