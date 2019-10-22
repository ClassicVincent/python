#!/usr/bin/python

import pymysql
import sys

db = pymysql.connect(user="vincent", passwd="chenwenqiang", db="vincent", charset="utf8")

cursor = db.cursor()

sql='select * from vincent_user'

print("查询语句:", sql)

cursor.execute(sql)
result=cursor.fetchall()

#print(cursor.description)
#print(result)

result_array=[]
for i in range(len(result)):
	single_result_dict = {}
	for j in range(len(cursor.description)):
#		print('==========')
#		print(result[i][j])
#		print(cursor.description[j][0])
		single_result_dict[cursor.description[j][0]] = result[i][j]
#		print('==========')

	result_array.append(single_result_dict)

print(result_array)

db.close()
