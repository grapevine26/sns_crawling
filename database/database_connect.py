"""
데이터 베이스 연결
"""
import pymysql
import os


class DatabaseConnection:
    def __init__(self, app_name=None):
        self.app_name = app_name
        port = 3306
        charset = 'utf8mb4'
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        db_name = 'sns_crawling'

        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                db=db_name,
                charset=charset
            )

            self.connection.autocommit = True
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            print('Cannot connect to Database: ', e)

    def close(self):
        self.cursor.close()
        self.connection.close()
