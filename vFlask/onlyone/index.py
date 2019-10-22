# -*- coding:utf-8 -*-
"""
@date   : 2019/8/28
@file   : index.py
@author : Vincent
@note   :
"""

import os
import sys

sys.path.append(os.getenv("VPYTHON"))

from flask import render_template, request, url_for, redirect

from vFlask.onlyone import onlyone_app
from vFlask.onlyone import mysql
from vVincent.spider.spider_dytt import MOVIE, DYTT
from vVincent.spider.spider_66ys import YS66, MOVIE_66YS
from flask import session, Response

import pymysql

import base64

@onlyone_app.route('/index', methods=['POST', 'GET'])
def onlyone_index():
    loginform = session.get('login')
    if loginform is None:
        return redirect('/login')

    username = loginform.get('username')
    print("用户名:", username)
    # 电影天堂最新电影列表
    dytt_latest = []

    # 66 影视最新的电影列表
    ys66_latest = []

    if request.method == 'GET':
        print("开始获取电影天堂最新电影信息...")

        # 获取最新电影日期
        sql = "select max(movie_date) from movie_info where movie_source = 'DYTT' and is_main_page = '1'"
        results = mysql.executeSql(sql)
        maxDate = results[0][0]
        if None == maxDate:
            print("未获取到最新电影日期...")
            maxDate = " ";
        print("电影天堂最新日期:" + maxDate)

        sql = "select *  from movie_info where movie_source = '%s' and is_main_page = '1' and movie_date = '%s'" % (
            'DYTT', maxDate)
        results = mysql.selectSql(sql)
        # print(results)
        for result in results:
            # print(result)
            movie = MOVIE()
            movie.name = result['movie_name']
            movie.source = result['movie_source']
            movie.pageUrl = result['movie_page_url']
            movie.nameTag = result['movie_name_tag']
            movie.isMain = result['is_main_page']
            movie.downloadUrl = result['movie_download_url']
            # print(movie.__dict__)
            dytt_latest.append(movie.__dict__)
            # print((movie.__dict__))
        print("电影天堂电影信息获取完成.")

        # 66 影视最新电影
        print("开始获取66影视最新电影信息...")

        # 获取最新电影日期
        sql = "select max(movie_date) from movie_info where movie_source = '66YS' and is_main_page = '1'"
        results = mysql.executeSql(sql)
        maxDate = results[0][0]
        if None == maxDate:
            print("未获取到最新电影日期...")
            maxDate = " ";
        print("66影视最新日期:" + maxDate)

        # 66 影视一部影视可能有多个链接
        sql = "select DISTINCT movie_name, movie_page_url from movie_info where movie_source = '66YS' and is_main_page = '1' and movie_date = '%s'" % (
            maxDate)
        results = mysql.selectSql(sql)
        for result in results:
            m = MOVIE_66YS()
            # print(result)
            m.pageUrl = result.get('movie_page_url')
            m.name = result.get('movie_name')
            sql = "select movie_name_tag, movie_download_url from movie_info where movie_source = '66YS' and movie_date = '%s' and movie_page_url = '%s'" % (
                pymysql.escape_string(maxDate), pymysql.escape_string(m.pageUrl))
            results1 = mysql.selectSql(sql)
            # print(results1)
            for result1 in results1:
                m.nameTag.append([result1.get('movie_name_tag'), result1.get('movie_download_url')])

            print(m.__dict__)
            ys66_latest.append(m.__dict__)

        print("入库处理")
        sql = '''update session set value = "%s" where name = "66YS_LATEST"''' % (
            base64.encodebytes(str(ys66_latest).encode('gbk')))
        # print(sql)
        mysql.executeSql(sql)

        sql = '''update session set value = "%s" where name = "DYTT_LATEST"''' % (
            base64.encodebytes(str(dytt_latest).encode('gbk')))
        # print(sql)
        mysql.executeSql(sql)
        print("入库完成.")

        return render_template('index.html', title="OnlyOne", username=username, visibility="show",
                               DYTT_LATEST=dytt_latest, YS66_LATEST=ys66_latest, isLogin=username)

    elif request.method == "POST":
        print(request.form)
        search_content = str(request.form.get('searchContent'))

        if 0 == len(search_content):
            print("没有输入查询信息,直接返回")

            print("查询上次返回信息...")
            sql = """select value from session where name = 'DYTT_LATEST'"""
            results = mysql.executeSql(sql)
            # print(results)
            if 1 == len(results):
                result = base64.decodebytes(results[0][0][2:-1].encode('gbk')).decode('gbk')
                dytt_latest = eval(result)
                print(type(dytt_latest))

            sql = """select value from session where name = '66YS_LATEST'"""
            results = mysql.executeSql(sql)
            if 1 == len(results):
                result = base64.decodebytes(results[0][0][2:-1].encode('gbk')).decode('gbk')
                ys66_latest = eval(result)
                print(type(ys66_latest))
            # print(results)
            print("查询完成.")

            return render_template('index.html', title="OnlyOne", username=username, visibility="show",
                                   DYTT_LATEST=dytt_latest, YS66_LATEST=ys66_latest)
        else:
            print("查询电影:", search_content)
            dytt = DYTT()
            dytt_latest = dytt.search(search_content, mysql)
            print(dytt_latest)

            ys66 = YS66()
            ys66_latest = ys66.search(search_content, mysql)
            print(ys66_latest)
            return render_template('index.html', title="OnlyOne", username=username, visibility="show",
                                   DYTT_LATEST=dytt_latest, YS66_LATEST=ys66_latest)
