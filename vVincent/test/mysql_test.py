#!/usr/bin/python

import pymysql
import sys

db = pymysql.connect(user="vincent", passwd="chenwenqiang", db="vincent", charset="utf8")

cursor = db.cursor()

sql='select * from vincent_user'

cursor.execute(sql)
#print(cursor.description)
count=len(cursor.description)
#print(cursor.description[0][0])
result=cursor.fetchall()

result_mem=[]
for i in range(len(result)):
	member={}
	for j in range(count):
		member[cursor.description[j][0]]=result[i][j]
	print(member)
	result_mem.append(member)

print(result_mem)
print(result_mem[0]['user_name'])

#result=cursor.fetchall()
#print(result)
#print(len(result))
db.close()
