# -*- coding:gbk -*-
"""
@date   : 2019/8/27
@file   : spider_dytt
@author : Vincent
@note   : 电影天堂爬虫
"""

import requests
from bs4 import BeautifulSoup

import os
import sys

sys.path.append(os.getenv('VPYTHON'))
import pymysql
import urllib
import gzip

from vVincent.utils.mysql_utils import mysql
from vVincent.utils.string_utils import stringUtils


class MOVIE:
    def __init__(self, name="", nameTag="", source="DYTT", downloadUrl="", pageUrl="", movieDate="", isMain=""):
        self.name = name
        self.nameTag = nameTag
        self.source = source
        self.downloadUrl = downloadUrl
        self.pageUrl = pageUrl
        self.movieDate = movieDate
        self.isMain = isMain

    def saveMovie(self, database):
        insertSql = "insert into movie_info values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            pymysql.escape_string(self.name), pymysql.escape_string(self.nameTag),
            pymysql.escape_string(self.source), pymysql.escape_string(self.downloadUrl),
            pymysql.escape_string(self.pageUrl), pymysql.escape_string(self.movieDate),
            pymysql.escape_string(self.isMain))
        database.executeSql(insertSql)


class DYTT:
    def __init__(self):
        self.base_url = "https://www.dytt8.net"
        self.search_base_url = "https://www.ygdy8.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

        self.latest = []

    def getMainPage(self):
        print("获取电影天堂首页信息...")
        response = requests.get(self.base_url, headers=self.headers)

        soup = BeautifulSoup(response.content.decode('gbk', 'ignore'), 'html.parser')
        a = soup.select('div.co_content8')
        latest_div = a[0]
        aList = latest_div.select('a')
        # print(aList)

        for a in aList:
            href = a['href']
            if href.endswith('app.html') or href.endswith('index.html'):
                continue
            else:
                self.latest.append([a.string, href])

    def getMovieInfo(self, movieUrl):
        print("url:", movieUrl)
        response = requests.get(movieUrl, headers=self.headers)
        content = response.content.decode('gbk', 'ignore')

        title = str.strip(content.split("◎片　　名")[1].split("<br />")[0])
        soup = BeautifulSoup(content, 'html.parser')
        tbodyList = soup.select('tbody')
        downloadUrl = tbodyList[0].select('a')[0].string
        return [title, downloadUrl]

    def search(self, content, database):
        search_result_list = []

        self.headers['Accept-Encoding'] = 'gzip, deflate'
        encoded = urllib.parse.quote(content, encoding="gbk")

        search_url = "http://s.ygdy8.com/plus/so.php?typeid=1&keyword=" + encoded
        print("搜索url:", search_url)

        response = requests.get(search_url, headers=self.headers)
        # fp = open("./html/index.html", "w")
        # fp.write(response.text.encode('utf-8').decode('gbk'))
        # fp.close()

        # 使用ignore参数，避免乱码
        soup = BeautifulSoup(response.content.decode('gbk', 'ignore'), 'html.parser')
        a = soup.select('div.co_content8')
        latest_div = a[0]
        aList = latest_div.select('a')
        # print(aList)

        for a in aList:
            # print(a.get_text())
            # print(a)
            href = a['href']
            if href.endswith('app.html') or href.endswith('index.html') or href.startswith('https://www.ygdy8.com/'):
                continue
            else:
                movie = MOVIE()
                [movie.nameTag, movie.pageUrl] = [a.get_text(), a['href']]
                movie.pageUrl = self.search_base_url + movie.pageUrl
                sql = "select count(*) from movie_info where movie_source = 'DYTT' and movie_page_url = '%s'" % (pymysql.escape_string(movie.pageUrl))
                results = database.executeSql(sql)
                if 0 == results[0][0]:
                    print("电影[", movie.nameTag, ']的信息在数据库中不存在,需要爬取')
                    [movie.name, movie.downloadUrl] = self.getMovieInfo(movie.pageUrl)
                    movie.source = 'DYTT'
                    movie.isMain = '0'
                    util = stringUtils()
                    movie.movieDate = util.formatTime("%Y%m%d")

                    movie.saveMovie(database)
                else:
                    print("电影[", movie.nameTag, ']的信息在数据库中已存在')
                    sql = "select * from movie_info where movie_source = 'DYTT' and movie_page_url = '%s'" % (pymysql.escape_string(movie.pageUrl))
                    results = database.selectSql(sql)
                    result = results[0]
                    movie.source = result['movie_source']
                    movie.name = result['movie_name']
                    movie.movieDate = result['movie_date']
                    movie.isMain = result['is_main_page']
                    movie.downloadUrl = result['movie_download_url']
                search_result_list.append(movie)

        return search_result_list
if __name__ == "__main__":

    config = {}
    config['host'] = 'localhost'
    config['user'] = 'vincent'
    config['passwd'] = 'chenwenqiang'
    config['db'] = 'vincent'
    config['charset'] = 'utf8'

    database = mysql(config)
    dytt = DYTT()
    # dytt.search("生化危机", database)
    dytt.getMainPage()
    movies = []
    for namgTag, pageUrl in dytt.latest:
        movie = MOVIE()
        movie.nameTag = namgTag
        movie.pageUrl = dytt.base_url + pageUrl
        movie.isMain = '1'
        utils = stringUtils()
        movie.movieDate = utils.formatTime('%Y%m%d')

        # check if movie already in database
        sql = "select count(*) from movie_info where movie_source = '%s' and movie_name_tag = '%s' and movie_page_url='%s'" % (
            pymysql.escape_string(movie.source), pymysql.escape_string(movie.nameTag),
            pymysql.escape_string(movie.pageUrl))
        results = database.executeSql(sql)
        if 0 == results[0][0]:
            print("数据库中没有电影:[", movie.nameTag, "]的信息,需要爬取")
            [movie.name, movie.downloadUrl] = dytt.getMovieInfo(movie.pageUrl)

            print(movie.__dict__)
            movie.saveMovie(database)
        else:
            print("数据库中已存在电影:[", movie.nameTag, "]的信息.")
            sql = "update movie_info set movie_date = '%s' where movie_name_tag = '%s' and movie_page_url = '%s' and movie_source = 'DYTT'" % (
                pymysql.escape_string(movie.movieDate), pymysql.escape_string(movie.nameTag),
                pymysql.escape_string(movie.pageUrl))
            database.executeSql(sql)
