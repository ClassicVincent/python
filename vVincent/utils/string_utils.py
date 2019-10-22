# -*- coding:utf-8 -*-
"""
@date   : 2019/8/15
@file   : string_utils.py
@author : Vincent
@note   : string utils
"""

import os
import sys
import hashlib
import time

import base64

class stringUtils:
	def __init__(self):
		self.weekName = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']

	def MD5(src='', encoding='gbk'):
		m=hashlib.md5()
		m.update(src.encode(encoding))
		dst=m.hexdigest()
		return dst.upper()

	def formatTime(self, format):
		'''
		%y 两位数的年份表示（00-99）
		%Y 四位数的年份表示（000-9999）
		%m 月份（01-12）
		%d 月内中的一天（0-31）
		%H 24小时制小时数（0-23）
		%I 12小时制小时数（01-12）
		%M 分钟数（00=59）
		%S 秒（00-59）
		%a 本地简化星期名称
		%A 本地完整星期名称
		%b 本地简化的月份名称
		%B 本地完整的月份名称
		%c 本地相应的日期表示和时间表示
		%j 年内的一天（001-366）
		%p 本地A.M.或P.M.的等价符
		%U 一年中的星期数（00-53）星期天为星期的开始
		%w 星期（0-6），星期天为星期的开始
		%W 一年中的星期数（00-53）星期一为星期的开始
		%x 本地相应的日期表示
		%X 本地相应的时间表示
		%Z 当前时区的名称
		%% %号本身
		'''
		return time.strftime(format, time.localtime())

if __name__ == "__main__":
	tm = time.localtime();
	print(tm)
	utils = stringUtils()
	dateNow = "%s %s" % (utils.formatTime("%Y.%m.%d"), utils.weekName[tm[6]])
	print(dateNow)

	base64.decode
