# -*- coding:utf-8 -*-
"""
@date   : 2019/8/12
@file   : mysql_utils.py
@author : Vincent
@note   :
"""

import os
import sys

print(sys.path)

for path in os.environ['PYTHONPATH'].split(';'):
	print(path)
	if path not in sys.path:
		sys.path.append(path)

print("当前系统路径:")
print(sys.path)

import pymysql
from libs.logUtils import mylog

class mysql:
	def __init__(self, host='', port='', user='', passwd='', db=''):
		self.config = {}
		self.config['host'] = host
		self.config['port'] = int(port)
		self.config['user'] = user
		self.config['passwd'] = passwd
		self.config['db'] = db
		self.connection = None
		self.cursor = None
		# self.connect(self.config)
		self.logger = mylog("mysql").getlog()

	def connect(self):
		try:
			self.connection = pymysql.connect(**self.config)
			self.connection.autocommit(1)
			# 所有的查询,都在连接con的一个模块cursor上面运行的
			self.cursor = self.connection.cursor()
		except pymysql.Error as e:
			error = "链接数据库失败,请检查数据库配置!"
			self.logger.info(error)
			self.logger.info(e)

	def close(self):
		'''
		关闭数据库
		'''
		if None != self.connection:
			self.connection.close()
		else:
			self.logger.info("关闭数据库失败:数据库未连接")	

	def getVersion(self):
		'''
		获取数据库版本号
		'''
		# 检查数据库连接,如果连接不对,再次建立连接
		if self.connection._sock is None:
			self.logger.info("sock is none")

		self.connection.ping(True)

		self.cursor.execute("select version()")
		version = self.getOneData()[0]
#		version = self.getOneData()
		return version

	def getOneData(self):
		'''
		取得上个查询的单个结果
		'''
		# 检查数据库连接,如果连接不对,再次建立连接
		if self.connection._sock is None:
			self.logger.info("sock is none")
		self.connection.ping(True)
		
		data = self.cursor.fetchone()
		return data

	def selectDatabase(self, db):
		'''
		选择数据库
		'''
		# 检查数据库连接,如果连接不对,再次建立连接
		if self.connection._sock is None:
			self.logger.info("sock is none")

		self.connection.ping(True)
		
		self.connection.select_db(db)

	def executeSql(self, sql=''):
		'''
		执行SQL语句
		'''
		try:
			# 检查数据库连接,如果连接不对,再次建立连接
			self.logger.info(type(self.connection))
			if self.connection._sock is None:
				self.logger.info("sock is none")
			
			# if None == self.connection:
			# 	self.logger.info("重新连接数据库")
			# 	self.connect(self.config)
			self.cursor.execute(sql)
			records = self.cursor.fetchall()
			return records
		except pymysql.Error as e:
			# error = "执行SQL语句(%s)失败!\n(%s):(%s)" % (sql, e.args[0], e.args[1])
			error = "执行SQL语句(%s)失败!" % (sql)
			self.logger.info(error)
			self.logger.info(e)

	def selectSql(self, sql=''):
		'''
		执行查询语句,并返回字典数组
		'''
		result_array = []
		try:
			# 检查数据库连接,如果连接不对,再次建立连接
			self.logger.info(type(self.connection))
			if self.connection._sock is None:
				self.logger.info("sock is none")
			self.connection.ping(True)
			
			self.cursor.execute(sql)
			records = self.cursor.fetchall()
			descriptions = self.cursor.description
			
			for i in range(len(records)):
				single_record_dict = {}
				for j in range(len(descriptions)):
					single_record_dict[descriptions[j][0]] = records[i][j]	
				result_array.append(single_record_dict)

		except pymysql.Error as e:
			# error = "执行SQL语句(%s)失败!\n(%s):(%s)" % (sql, e.args[0], e.args[1])
			error = "执行SQL语句(%s)失败!" % (sql)
			self.logger.info(error)
			self.logger.info(e)
		return result_array

	def executeSqlFile(self, filename=''):
		'''
		执行SQL文件
		'''
		try:
			# 检查数据库连接,如果连接不对,再次建立连接
			if self.connection._sock is None:
				self.logger.info("sock is none")
			self.connection.ping(True)
			
			fp = open(filename, "r")
			content = fp.read()
			fp.close()
			for sql in content.split(';'):
				if 0 != len(sql.strip()):
					self.cursor.execute(sql)
		except pymysql.Error as e:
			# error = "执行SQL语句(%s)失败!\n(%s):(%s)" % (sql, e.args[0], e.args[1])
			error = "执行SQL语句(%s)失败!" % (sql)
			self.logger.info(error)
		except BaseException as e:
			# error = "打开文件[%s]失败!\n(%s):(%s)" % (filename, e.args[0], e.args[1])
			error = "执行SQL语句(%s)失败!" % (sql)
			self.logger.info(error)
			self.logger.info(e)
	
	def commitSql(self, sql=''):
		'''
		执行SQL并提交
		'''
		error = ''
		try:
			# 检查数据库连接,如果连接不对,再次建立连接
			if self.connection._sock is None:
				self.logger.info("sock is none")
			self.connection.ping(True)
			
			self.cursor.execute(sql)
			self.connection.commit()
		except pymysql.Error as e:
			self.connection.rollback()
			# error = "执行SQL语句(%s)失败!\n(%s):(%s)" % (sql, e.args[0], e.args[1])
			error = "执行SQL语句(%s)失败!" % (sql)
			self.logger.info(error)
			self.logger.info(e)
		return error

if __name__ == "__main__":
	config = {}
	config['host'] = 'localhost'
	config['port'] = '3306'
	config['user'] = 'vincent'
	config['passwd'] = 'chenwenqiang'
	config['db'] = 'vincent'
	config['charset'] = 'utf8'
	
	db = mysql(host=config['host'], port=config['port'], user=config['user'], passwd=config['passwd'], db=config['db'])
	db.connect()
	db.logger.info("数据库版本:" + db.getVersion())

	result = db.executeSql("select * from vincent_user")
	if None == result:
		db.logger.info("查询数据库语句失败")	
	elif 0 != len(result):
		db.logger.info("查询结果:" + str(result))
		db.logger.info("查询结果:" + str(result[0]))
		db.logger.info("查询结果:" + str(result[0][0]))

	result = db.selectSql("select * from vincent_user where user_name = ''")
	db.logger.info("查询结果:" + str(result))
	
#	mysql.executeSqlFile("a.sql")
	db.close()
	

