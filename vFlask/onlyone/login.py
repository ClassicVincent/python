#!/usr/bin/python
"""
@date	: 20190722
@file	: onlyone_login.py
@author	: onlyone
"""

import os
import sys

sys.path.append(os.getenv("VPYTHON"))

import time
from flask import render_template, request, url_for, redirect

from vFlask.onlyone import onlyone_app
from vFlask.onlyone import mysql, logger
from vVincent.spider.spider_one import ONE
from vVincent.utils.string_utils import stringUtils

from flask import session, Response

@onlyone_app.route('/')
@onlyone_app.route('/login', methods=['POST', 'GET'])
def onlyone_login():
	print("访问方法:", request.method)
	# 从ONE网站爬取首页图片和一句话

	strUtils = stringUtils()
	tm = time.localtime()
	dateNow = "%s %s" % (strUtils.formatTime("%Y.%m.%d"), strUtils.weekName[tm[6]])

	sql = "select * from session where name = 'ONEWORD'"
	oneLine = ""
	results = mysql.selectSql(sql)
	logger.info("每日一句结果:" + str(results))
	if 0 == len(results):
		one = ONE()
		oneLine = one.word
		logger.info(dateNow)
		logger.info(one.word)
		sql = "insert into SESSION values('ONEWORD', '%s%s')" % (dateNow, one.word)
		logger.info(sql)
		mysql.executeSql(sql)
	else:
		result = results[0]['value']
		logger.info(result)
		oneLineDate = result[:10]
		logger.info("每日一句数据库日期:[" + oneLineDate + "]")
		if oneLineDate != dateNow:
			one = ONE()
			oneLine = one.word
			sql = "update session set value = '%s%s' where name = 'ONEWORD'" % (dateNow, one.word)
			logger.info(sql)
			mysql.executeSql(sql)
		else:
			oneLine = result[10:]

	if request.method == 'GET':
		return render_template('login_1.html', hidden="hidden", title="login", oneLine=oneLine, dateNow=dateNow, username="未登录", visibility="hidden")
	elif request.method == 'POST':
		print("访问参数:", request.args)
		# 验证登录参数
		print("请求数据:", request.form)

		username = str(request.form.get('username'))
		password = str(request.form.get('password'))

		print("user_name:", username)
		print("pass_word:", password)

		error_message = ""
		if 0 == len(username):
			error_message = "输入的用户名为空"
			return render_template("login_1.html", errormsg=error_message, if_success="登录失败:", oneLine=oneLine, dateNow=dateNow)
		if 0 == len(password):
			error_message = "输入的密码为空"
			return render_template("login_1.html", errormsg=error_message, if_success="登录失败:", oneLine=oneLine, dateNow=dateNow)

		print("基础数据格式校验完成...")
		sql = "select user_pswd from onlyone_user where user_name = '%s'" % (username)
		print(sql);
		result = mysql.executeSql(sql)
		if None == result:
			error_message = "用户[%s]不存在" % (username)
		elif 0 == len(result):
			error_message = "用户[%s]不存在" % (username)
		else:
			print("数据库内密码:", result, result[0], result[0][0])
			if password.strip().upper() != result[0][0].strip().upper():
				error_message = "密码错误!"
			else:
				session['login'] = request.form
				# response = Response()
				# response.set_cookie('username', username)
				session.permanent = True
				return redirect('/index')

		if len(error_message) != 0:
			return render_template("login_1.html", hidden="visible", errormsg=error_message, if_success="登录失败:", oneLine=oneLine, dateNow=dateNow)


@onlyone_app.route('/register', methods=['POST', 'GET'])
def onlyone_register():
	if request.method == 'GET':
		return render_template('register.html', title="注册")


