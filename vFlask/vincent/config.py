# -*- coding=utf-8 -*-
# file:config.py.py
# time:2019/9/14{10:05}
# author:Vincent
# note:

# 系统相关配置
SERVER_HOST     = "0.0.0.0"
SERVER_PORT     = 8103
USE_DEBUGGER    = True
USE_RELOADER    = True

# 数据库相关配置
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_USERNAME = "vincent"
DB_PASSWORD = "chenwenqiang"
DB_NAME = "vincent"

# 小程序相关配置
APP_ID = "wx151773ecee2db6e8"
APP_SECRETKEY = "1b21cd5328df78acfb1d62fe2459447b"

WEIXIN_LOGIN_URL = "https://api.weixin.qq.com/sns/jscode2session"

# DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" %(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLACHEMY_ECHO          = True
# SQLALCHEMY_TRACK_MODIFICATIONS = False