# -*- coding: utf-8 -*-
import multiprocessing.dummy as mp
import facebook_crawler
import instagram_crawler
import kakaostory_crawler
import naverblog_crawler
import sys
import time
import unicodedata
from database import update, select
from analysis import word_analysis
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
import os
import re
from openpyxl import load_workbook
#
# load_wb = load_workbook(os.getcwd() + '\\tenspace.xlsx')
# load_ws = load_wb['SNS_제출']
#
# xls_list = []
# for i, row in enumerate(load_ws.rows):
#     temp = {}
#     if i > 3 and row[4].value is not None:
#         for j, cell in enumerate(row):
#             if j == 3: # 이름
#                 temp["name"] = cell.value
#             if j == 12: # 페북
#                 print(re.findall("/https?:\/\/(?:youtu\.be\/|(?:[a-z]{2,3}\.)?youtube\.com\/watch(?:\?|#\!)v=)([\w-]{11}).*/gi", cell.value))
#                 temp["fb_id"] = cell.value
#             if j == 13: # 인스타
#                 temp["in_id"] = cell.value
#             if j == 14: # 카카오
#                 temp["ka_id"] = cell.value
#             if j == 15: # 네이버
#                 temp["na_id"] = cell.value
#         xls_list.append(temp)
# print(xls_list)

if __name__ == '__main__':
    fb_id = 'hyunah.cho.9484'
    in_id = ''
    ka_id = 'icdcha'
    na_id = ''

    re_ = re.compile("com\/([a-zA-Z0-9._]\w+)[_/]?")
    print(re_.findall('https://www.facebook.com/sunnyroomc'))
    print(re_.findall('https://www.facebook.com/sunnyroomc/'))
    print(re_.findall('https://instagram.com/ariel_hanna_?igshid=YmMyMTA2M2Y='))
    print(re_.findall('https://www.facebook.com/profile.php?id=100003519587176&mibextid=LQQJ4d'))
    re_ = re.compile('#([가-힣ㄱ-ㅎa-zA-Z0-9]?\w+)')
    post_text = """healing.zip 넘 착한데 또 박력해ㅋㅋㅋㅋㅋㅋㅋ
1일 1힐링은 약속드립니다🤙🏻🫶🏻
힐링이 되셨으면 팔로우🙆‍♂️좋아요🙆
더 많은 힐링모음집은
👉🏻@healing.zip
🎥 Credit: unknown
Dm For Removel Or #Credit#asd 🙏
#웃긴영상 #웃긴동영상 #오늘의유머 #웃긴짤 #좋반 #좋아요 #좋아요반사 #맞팔해요 #맞팔환영#예능 #웃긴 #유머 #유머스타그램 #예능 #ㅋㅋㅋ #놀아줘 #자"""
    tags = re_.findall(post_text)
    a = re_.sub('', post_text)
    print(a)
    print(tags)

    # manager = mp.Manager()
    # return_list = manager.list()
    # process = []
    # print(type(return_list))
    #
    # if fb_id:
    #     fb_driver = facebook_crawler.start()
    #     process.append(
    #         mp.Process(target=facebook_crawler.facebook_crawler_start,
    #                    args=(fb_driver, fb_id, return_list,)),
    #     )
    # if in_id:
    #     in_driver = instagram_crawler.start()
    #     process.append(
    #         mp.Process(target=instagram_crawler.instagram_crawler_start,
    #                    args=(in_driver, in_id, return_list,)),
    #     )
    # if ka_id:
    #     ka_driver = kakaostory_crawler.start()
    #     process.append(
    #         mp.Process(target=kakaostory_crawler.kakao_story_crawler_start,
    #                    args=(ka_driver, ka_id, return_list,)),
    #     )
    # if na_id:
    #     na_driver = naverblog_crawler.start()
    #     process.append(
    #         mp.Process(target=naverblog_crawler.naverblog_crawler_start,
    #                    args=(na_driver, na_id, return_list,))
    #     )
    #
    # for j in process:
    #     j.start()
    # for j in process:
    #     j.join()
    # print(return_list)
    #
    # posts = ' '.join(i.replace('#', ' ') for i in return_list)
    # print(posts)
    #
    # posts = word_analysis.word_clear(posts)
    # posts = posts.replace('.', '').replace(',', '').replace("'", '').replace('/', '').strip()
    # print(posts)
    #
    # nouns = Okt().nouns(posts)
    # result = Counter(nouns).most_common()
    # print(result)
