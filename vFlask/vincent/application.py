# -*- coding=gbk -*-
# file:application.py.py
# time:2019/9/14{10:07}
# author:Vincent
# note:

from flask import Flask
from flask_script import Manager

from libs.mysqlUtils import mysql
from libs.logUtils import mylog

class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('config.py')

app = Application(__name__)
db = mysql(host=app.config['DB_HOST'],
           user=app.config['DB_USERNAME'],
           passwd=app.config['DB_PASSWORD'],
           db=app.config['DB_NAME'],
           port=app.config['DB_PORT'])

logger = mylog(__name__).getlog()

manager = Manager(app)