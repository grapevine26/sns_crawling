import re
import csv
from konlpy.tag import Okt
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
REPLACE_ALL = re.compile("[^a-zA-Z가-힣 ]")

dirname = os.path.dirname(__file__)
ko_file_path = os.path.join(dirname, 'kor_stop_words.txt')
en_file_path = os.path.join(dirname, 'eng_stop_words.txt')

with open(ko_file_path, 'r', encoding='utf-8') as f:
    KOR_STOP_WORDS = f.read()
with open(en_file_path, 'r', encoding='utf-8') as f:
    ENG_STOP_WORDS = f.read()


def word_clear(words):
    words = REPLACE_NO_SPACE.sub(" ", words)
    words = REPLACE_WITH_SPACE.sub(" ", words)
    return words


def noun_extract(words, i18n):
    if i18n == 'EN':
        s = LancasterStemmer()
        # 소문자 변환, 토큰화, 불용어 제외, 명사 추출
        word_list = [s.stem(word) for word in word_tokenize(words.lower()) if word not in ENG_STOP_WORDS]
        print('stem :', word_list)  # 어간추출
    else:
        o = Okt()
        # 토큰화, 불용어 제외, 명사 추출
        word_list = ' '.join(word for word in words.split() if word not in KOR_STOP_WORDS)
        word_list = o.nouns(word_list)
        print('noun :', word_list)
    return word_list


def sentiment_analysis(words):
    analyser = SentimentIntensityAnalyzer()
    positive_word_list = []
    negative_word_list = []
    for word in words.split():
        score = analyser.polarity_scores(word)
        if score['pos'] > score['neg']:
            positive_word_list.append(word)
        elif score['pos'] < score['neg']:
            negative_word_list.append(word)
    print('positive :', positive_word_list)
    print('negative :', negative_word_list)
    return positive_word_list, negative_word_list


def racism_analysis(words):
    racism_words = []
    racism_list = []
    racism_path = os.path.join(dirname, 'racism_word.csv')
    with open(racism_path, 'r', encoding='utf-8-sig') as rf:
        rdr = csv.reader(rf)
        for line in rdr:
            racism_words.append(line[0])

    for i in words.split():
        if i in racism_words:
            racism_list.append(i)
    return racism_list

# from collections import Counter
#
# racism_words = ''
# racism_list = []
#
# f = open('test.txt', 'r', encoding='utf-8')
# rdr = csv.reader(f)
# for line in rdr:
#     try:
#         print(line[0])
#         racism_words += line[0]
#     except Exception as e:
#         print('')
# f.close()
# racism_words = word_clear(racism_words)
# aa = Okt().nouns(racism_words)
# print(aa)
# a = Counter(aa).most_common()
# print(a)
