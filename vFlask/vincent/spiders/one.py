# -*- coding=gbk -*-
# file:one.py
# time:2019/9/14{23:17}
# author:Vincent
'''
??ONE ?? ????????????
'''

import requests
import time
import json

from libs.logUtils import mylog
from libs.mysqlUtils import mysql
from config import DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME
import pymysql

db = mysql(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_NAME)
logger = mylog("spider").getlog()

class ONE():
    def __init__(self):
        self.base_url = "http://v3.wufazhuce.com:8000/api/channel/one/%s/0"
        self.feeds_list_url = "http://v3.wufazhuce.com:8000/api/feeds/list/%s"  # YYYY-MM
        self.date_now = time.strftime("%Y%m%d", time.localtime())
        self.MAIN_INDEX = "MAIN"
        self.FEEDS_INDEX = "FEEDS"

    def get_main_page(self, spider_date):
        logger.info("??????????:" + spider_date)

        db.connect()
        sql = "select count(*) from spider_one where spider_index = '%s' and spider_date = '%s'" % (self.MAIN_INDEX, spider_date)
        db_result = db.executeSql(sql)
        if 0 == db_result[0][0]:
            main_page_url = self.base_url % (spider_date)
            logger.info(main_page_url)
            response = requests.get(main_page_url)
            logger.info("status code:" + str(response.status_code))
            if 200 == response.status_code:
                # logger.info(response.text)
                response_json = json.loads(response.text, encoding="gbk")
                response_string = json.dumps(response_json, indent=4, ensure_ascii=False)
                if 'data' in response_json:
                    sql = "insert into spider_one values('%s', '%s', '%s', '%s')" % \
                          (self.MAIN_INDEX,
                           spider_date,
                           pymysql.escape_string(response_string),
                           pymysql.escape_string(main_page_url))
                    db.executeSql(sql)
                else:
                    logger.info("δ?????[%s]??????" % (spider_date))
                    # logger.info(json.dumps(response_json, indent=4, ensure_ascii=False))

                    # fp = open("./html/one_index.json", "w", encoding="UTF-8")
                    # fp.write(json.dumps(response_json, indent=4, ensure_ascii=False))
                    # fp.close()
            else:
                logger.info("????[ONE]??????,CODE:" + str(response.status_code))
        else:
            logger.info("??????????????????????????????!")
            
        db.close()

    def get_feeds_list(self, spider_month):
        logger.info("?????·?:" + spider_month)

        db.connect()
        sql = "select count(*) from spider_one where spider_index = '%s' and spider_date = '%s'" % (self.FEEDS_INDEX, spider_month)
        db_result = db.executeSql(sql)
        if 0 == db_result[0][0]:
            list_url = self.feeds_list_url % (spider_month)
            logger.info("url:" + list_url)
            response = requests.get(list_url)
            logger.info("status code:" + str(response.status_code))
            if 200 == response.status_code:
                response_json = json.loads(response.text, encoding="gbk")

                if 0 != len(list(response_json['data'])):
                    sql = "insert into spider_one values('%s', '%s', '%s', '%s')" % \
                          (self.FEEDS_INDEX,
                           spider_month,
                           pymysql.escape_string(json.dumps(response_json, indent=4, ensure_ascii=False)),
                           pymysql.escape_string(list_url))
                    db.executeSql(sql)
                else:
                    logger.info("????[%s]?????????." % (spider_month))
            else:
                logger.info("????[ONE]??????,CODE:" + str(response.status_code))
        else:
            logger.info("??????????????????????????????!")

        db.close()

def main():
    one = ONE()
    one.get_main_page(time.strftime('%Y-%m-%d', time.localtime()))
    # one.get_main_page("2019-09-14")
    one.get_feeds_list(time.strftime('%Y-%m', time.localtime()))
    # one.get_feeds_list("2019-09")

if __name__ == "__main__":
    main()
