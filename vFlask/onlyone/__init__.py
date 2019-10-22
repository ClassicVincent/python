#!/usr/bin/python
'''
@date	: 20190722
@file	: __init__.py
@author	: vincent
'''
from flask import Flask

import os
import sys

sys.path.append(os.getenv("VPYTHON"))

from vVincent.utils.mysql_utils import mysql
from vVincent.utils.log_utils import mylog

onlyone_app = Flask(__name__)

config = {}
config['host'] = 'localhost'
config['user'] = 'vincent'
config['passwd'] = 'chenwenqiang'
config['db'] = 'vincent'
config['charset'] = 'utf8'

mysql = mysql(config)
if None != mysql:
	print("连接数据库成功.")

logger = mylog("ONLYONE").getlog()

