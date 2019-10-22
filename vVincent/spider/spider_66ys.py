# -*- coding:utf-8 -*-
"""
@date   : 2019/8/28
@file   : spider_66ys
@author : Vincent
@note   : 66影视网站爬虫
"""

import requests
from bs4 import BeautifulSoup

import pymysql
import urllib
import http
import os
import sys

sys.path.append(os.getenv('VPYTHON'))

from vVincent.spider.spider_dytt import MOVIE
from vVincent.utils.mysql_utils import mysql
from vVincent.utils.string_utils import stringUtils


class MOVIE_66YS:
    def __init__(self):
        self.name = ""
        self.nameTag = []
        self.source = "66YS"
        self.pageUrl = ""
        self.downloadUrl = []


class YS66:
    def __init__(self):
        self.url = "https://www.66e.cc/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.latest = []

    def getMainPage(self):
        print("开始获取首页信息...")
        response = requests.get(self.url, headers=self.headers)
        print(response.status_code)
        if 200 == response.status_code:
            # fp = open("./html/index.html", "w", encoding='utf-8')
            # fp.write(response.content.decode('gbk'))
            # fp.close()
            soup = BeautifulSoup(response.content.decode('gbk', 'ignore'), 'html.parser')
            aList = soup.select('html > body > div.wrap > div.tjlist > ul > li > p > a')
            # print(aList)
            for a in aList:
                self.latest.append([a['title'], a['href']])

    def getMovieInfo(self, movieUrl):
        resultList = []
        response = requests.get(movieUrl, headers=self.headers)
        # print(response.status_code)
        if 200 == response.status_code:
            # fp = open("./html/index.html", "w", encoding="utf-8")
            # fp.write(response.content.decode('gbk'))
            # fp.close()
            soup = BeautifulSoup(response.content.decode('gbk', 'ignore'), 'html.parser')
            linkList = soup.select('tbody > tr > td > a')
            # print(linkList)
            for link in linkList:
                if False == link.has_attr('target'):
                    resultList.append([link.string, link['href']])

        return resultList

    def search(self, content, database):
        search_result_list = []

        search_url = self.url + "/e/search/index.php"
        print("开始搜索:[", content, "]...")
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        # print('headers', self.headers)
        post_dict = {
            "show": "title,smalltext",
            "tempid": "1",
            "tbname": "Article",
            "keyboard": content,
            "submit": ""
        }

        # print(post_dict)
        data = urllib.parse.urlencode(post_dict, encoding='gbk')
        print(data)

        response = requests.post(search_url, data=data, headers=self.headers)
        # print(response.content.decode('gbk'))
        # fp = open("./html/index.html", "w")
        # fp.write(response.content.decode('gbk'))
        # fp.close()

        soup = BeautifulSoup(response.content.decode('gbk', 'ignore'), 'html.parser')

        result_list = soup.select(
            "html > body > div > div.wrap > div.mainleft > div.channellist > div.listBox > ul > li > div.listInfo > h3 > a")

        for result in result_list:
            movie = MOVIE_66YS()
            movie.name = result['title']
            movie.pageUrl = result['href']

            sql = "select count(*) from movie_info where movie_source = '66YS' and movie_page_url = '%s'" % (
            movie.pageUrl)
            sql_results = database.executeSql(sql)
            if 0 == sql_results[0][0]:
                print("数据库中不存在:[", movie.name, "]的记录需要爬取")

                page_infos = self.getMovieInfo(movie.pageUrl)
                for name_tag, download_url in page_infos:
                    movie.nameTag.append([name_tag, download_url])
                    movie.downloadUrl.append(download_url)

                    m = MOVIE()
                    m.downloadUrl = download_url
                    m.nameTag = name_tag
                    m.source = '66YS'
                    m.name = movie.name
                    m.pageUrl = movie.pageUrl
                    m.isMain = '0'
                    util = stringUtils()
                    m.movieDate = util.formatTime("%Y%m%d")

                    m.saveMovie(database)
                search_result_list.append(movie.__dict__)
            else:
                print("数据库中电影:[", movie.name, "]的记录.")
                sql = "select movie_name_tag, movie_download_url from movie_info where movie_source = '66YS' and movie_page_url = '%s'" % (
                pymysql.escape_string(movie.pageUrl))
                results1 = database.selectSql(sql)
                # print(results1)
                for result1 in results1:
                    movie.nameTag.append([result1.get('movie_name_tag'), result1.get('movie_download_url')])
                search_result_list.append(movie.__dict__)
        return search_result_list

if __name__ == "__main__":
    config = {}
    config['host'] = 'localhost'
    config['user'] = 'vincent'
    config['passwd'] = 'chenwenqiang'
    config['db'] = 'vincent'
    config['charset'] = 'utf8'

    database = mysql(config)

    movieList = []
    ys66 = YS66()
    # print(ys66.search("冰与火", database))

    ys66.getMainPage()
    for name, pageUrl in ys66.latest:
        movie = MOVIE()
        movie.name = name
        movie.source = '66YS'
        movie.pageUrl = pageUrl
        util = stringUtils()
        movie.movieDate = util.formatTime("%Y%m%d")

        sql = "select count(*) from movie_info where movie_source = '66YS' and movie_page_url = '%s'" % (
        pymysql.escape_string(movie.pageUrl))
        results = database.executeSql(sql)
        if 0 == results[0][0]:
            print("数据库中不存在电影:[", movie.name, "]不存在,需要爬取...")
            resultList = ys66.getMovieInfo(pageUrl)
            for nameTag, downloadUrl in resultList:
                print(nameTag, downloadUrl)
                m = MOVIE()
                m.name = movie.name
                m.pageUrl = movie.pageUrl
                m.nameTag = nameTag
                m.downloadUrl = downloadUrl
                m.source = '66YS'
                util = stringUtils()
                m.movieDate = movie.movieDate
                m.isMain = '1'

                m.saveMovie(database)
        else:
            print("数据库中已存在电影:[", movie.name, "]的信息.")
            sql = "update movie_info set movie_date = '%s' where movie_name = '%s' and movie_page_url = '%s' and movie_source = '66YS'" % (
                pymysql.escape_string(movie.movieDate), pymysql.escape_string(movie.movie_name),
                pymysql.escape_string(movie.pageUrl))
            database.executeSql(sql)
            # print(resultList)
