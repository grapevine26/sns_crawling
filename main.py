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


if __name__ == '__main__':
    fb_id = ''
    in_id = ''
    ka_id = ''
    na_id = 'jeonsim'

    manager = mp.Manager()
    return_list = manager.list()
    process = []
    print(type(return_list))
    if fb_id:
        fb_driver = facebook_crawler.start()
        process.append(
            mp.Process(target=facebook_crawler.facebook_crawler_start,
                       args=(fb_driver, fb_id, return_list,)),
        )
    if in_id:
        in_driver = instagram_crawler.start()
        process.append(
            mp.Process(target=instagram_crawler.instagram_crawler_start,
                       args=(in_driver, in_id, return_list,)),
        )
    if ka_id:
        ka_driver = kakaostory_crawler.start()
        process.append(
            mp.Process(target=kakaostory_crawler.kakao_story_crawler_start,
                       args=(ka_driver, ka_id, return_list,)),
        )
    if na_id:
        na_driver = naverblog_crawler.start()
        process.append(
            mp.Process(target=naverblog_crawler.naverblog_crawler_start,
                       args=(na_driver, na_id, return_list,))
        )

    for j in process:
        j.start()
    for j in process:
        j.join()
    print(return_list)

    posts = ' '.join(i.replace('#', ' ') for i in return_list)
    print(posts)

    posts = word_analysis.word_clear(posts)
    posts = posts.replace('.', '').replace(',', '').replace("'", '').replace('/', '').strip()
    print(posts)

    nouns = Okt().nouns(posts)
    result = Counter(nouns).most_common()
    print(result)
