# -*- coding=utf-8 -*-
# file:onlyone.py
# time:2019/9/14{16:08}
# author:Vincent

import json
import requests
import time
import datetime

from flask import Blueprint, request
from application import logger, app, db
from libs.stringUtils import generateToken, checkToken
from spiders.one import ONE

route_onlyone = Blueprint("onlyone", __name__)
@route_onlyone.route("/login", methods=['POST', 'GET'])
def onlyone_login():
    result = {}
    data = json.loads(request.data.decode('utf-8'))
    logger.info(data['code'])

    db.connect()

    queryString = "appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
        app.config['APP_ID'], app.config['APP_SECRETKEY'], data['code'])
    requestUrl = app.config['WEIXIN_LOGIN_URL'] + "?" + queryString
    logger.info("访问url:" + requestUrl)

    response = requests.get(requestUrl)
    if 200 != response.status_code:
        result['status_code'] = "1001"
        result['status_msg'] = "访问ONE网页失败,code:[%d]" % response.status_code
    else:
        result['status_code'] = "0000"
        jsonObject = json.loads(response.text)
        openid = jsonObject['openid']
        session_key = jsonObject['session_key']
        logger.info("session_key:" + jsonObject['session_key'])
        logger.info("openid:" + jsonObject['openid'])

        # 根据session_key生成token
        token = generateToken(jsonObject['session_key'])

        # 保存token
        sql = "select count(*) from weixin_session where openid = '%s';" % (openid)
        logger.info(sql)
        db_result = db.executeSql(sql)
        # 数据库结果
        if 0 == db_result[0][0]:
            sql = "insert into weixin_session values ('%s', '%s');" % (openid, session_key)
            logger.info(sql)
            db.executeSql(sql)
        else:
            # 更新数据库结果
            sql = "update weixin_session set session_key = '%s' where openid = '%s';" % (session_key, openid)
            logger.info(sql)
            db.executeSql(sql)

        result['openid'] = openid
        result['token'] = token

    logger.info("结果:" + json.dumps(result, ensure_ascii=True))
    db.close()
    return json.dumps(result, ensure_ascii=True)

@route_onlyone.route('/checkToken', methods=['POST', 'GET'])
def onlyone_check():
    logger.info("开始验证token...")
    result ={}

    db.connect()

    if not request.headers.has_key('openid'):
        result['code'] = "1001"
        result['msg'] = "openid not found in headers"

    if not request.headers.has_key('token'):
        result['code'] = "1001"
        result['msg'] = "token not found in headers"

    logger.info(request.headers)

    openid = request.headers['openid']
    token = request.headers['token']

    sql = "select count(*) from weixin_session where openid = '%s';" % (openid)
    logger.info(sql)
    db_result = db.executeSql(sql)
    logger.info(db_result)
    if 0 == db_result[0][0]:
        logger.info("openid在数据库中不存在")
        result['code'] = "1002"
        result['msg'] = '没有找到该openid的登陆记录'
    else:
        sql = "select session_key from weixin_session where openid = '%s';" % (openid)
        logger.info(sql)
        db_result = db.executeSql(sql)
        logger.info(db_result)
        session_key = db_result[0][0]
        logger.info(session_key)

        [result['code'], result['msg']] = checkToken(session_key, token)
        logger.info("code:" + result['code'])
        logger.info("msg:" + result['msg'])

    db.close()
    return json.dumps(result, ensure_ascii=True)

@route_onlyone.route('/getOneMainData', methods=['POST', 'GET'])
def getOneMainData():
    result = {}
    db.connect()

    date_now = time.strftime("%Y-%m-%d", time.localtime())
    one = ONE()
    one.get_main_page(date_now)

    sql = "select count(*) from spider_one where spider_index = '%s' and spider_date = '%s'" % (
        one.MAIN_INDEX,
        date_now
    )
    logger.info(sql)
    db_result = db.executeSql(sql)
    logger.info("查询数据库结果:")
    logger.info(db_result)
    
    if 0 == db_result[0][0]:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        date_yesterday = yesterday.strftime("%Y-%m-%d")
        logger.info("昨天日期:" + date_yesterday)

        sql = "select spider_result from spider_one where spider_index = '%s' and spider_date = '%s';" % (
            one.MAIN_INDEX,
            date_yesterday
        )
        logger.info(sql)
        db_result = db.executeSql(sql)
        result = db_result[0][0]
    else:
        sql = "select spider_result from spider_one where spider_index = '%s' and spider_date = '%s';" % (
            one.MAIN_INDEX,
            date_now
        )
        logger.info(sql)
        db_result = db.executeSql(sql)
        result = db_result[0][0]

    db.close()

    return result


