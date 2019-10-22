# -*- coding=utf-8 -*-

from flask import Blueprint, request
import pymysql


from spiders.biquge import BIQUGE
from application import logger, db

from libs.mysqlUtils import mysql
import json

route_novel = Blueprint("novel", __name__)

def createResultString(code, message):
    result = {}
    result['code'] = code
    result['message'] = message
    result_string = json.dumps(result, indent=4, ensure_ascii=False)
    logger.info(result_string)
    return result_string

def checkRequestData(request_data, check_list):
    for check_tag in check_list:
        if check_tag not in request_data.keys():
            return createResultString("1001", "请求数据中未找到[%s]字段" % (check_tag))
    return "TRUE"

# 书架功能 包括查询是否已经加入书架、加入书架的功能
@route_novel.route("/bookShelf", methods=['POST'])
def novel_bookshelf():
    '''
    书架模块 包括书架查询 书架新增
    区别参数:
        method: 'SELECT' --查询
                'INSERT' --新增
        openid
        novelInfo
    '''
    result = {}
    db.connect()
    logger.info("书架模块...")
    logger.info("请求数据:" + request.data.decode("utf-8"))

    request_data = json.loads(request.data.decode('utf-8'))

    openid = request_data['openid'] 
    logger.info("openid:" + openid)
    
    if 0 == len(openid):
        db.close()
        return createResultString("1001", "请求数据中没有获取到openid信息")

    method = request_data['method']
    logger.info("method:" + method)
    if 0 == len(method):
        db.close()
        return createResultString("1001", "请求数据中没有找到method信息")
    elif str.upper(method) not in ['SELECT', 'INSERT']:
        db.close()
        return createResultString("1001", "METHOD字段[%s]不合法" % (method))

    novelInfo = request_data['novelInfo']
    logger.info("小说信息:" + str(novelInfo))
    if 0 == len(novelInfo):
        db.close()
        return createResultString("1001", "请求数据中没有找到novelInfo信息")
    
    if 'novelUrl' not in novelInfo.keys():
        db.close()
        return createResultString("1001", "novelInfo中没有novelUrl")

    logger.info(str.upper(method))
    logger.info("SELECT" == str.upper(method))
    if "SELECT" == str.upper(method):
        logger.info("查询用户的书架信息...")
        sql = "select count(*) from novel_bookshelf where openid = '%s' and novel_url = '%s'" % (openid, novelInfo['novelUrl'])
        logger.info("查询书架SQL:" + sql)

        db_result = db.executeSql(sql)
        logger.info("数据库查询结果:" + str(db_result))
        if 0 == db_result[0][0]:
            db.close()
            return createResultString("1000", "用户[%s]书架上没有[%s]信息!" % (openid, novelInfo['novelUrl']))
        else:
            db.close()
            return createResultString("0000", "该用户[%s]书架上已有[%s]的信息" % (openid, novelInfo['novelUrl']))
    elif "INSERT" == str.upper(method):
        logger.info("加入书架操作...")
        # 首先需要查询是否在书架中，如果不在再进行插入操作
        sql = "select count(*) from novel_bookshelf where openid = '%s' and novel_url = '%s'" % (openid, novelInfo['novelUrl'])
        logger.info("查询书架SQL:" + str(sql))

        db_result = db.executeSql(sql)
        logger.info("数据库查询结果:" + str(db_result))
        if 1 == db_result[0][0]:
            logger.info("该小说[%s]已在书架中" % (novelInfo['novelUrl']))
            db.close()
            return createResultString("1111", "该小说[%s]已在书架中" % (novelInfo['novelUrl']))
        else:
            sql = "INSERT INTO NOVEL_BOOKSHELF(openid, novel_name, novel_url, novel_author, novel_image, novel_brief) \
                 VALUES('%s', '%s', '%s', '%s', '%s', '%s')" %  \
                 (pymysql.escape_string(openid),                \
                 pymysql.escape_string(novelInfo['novelName']), \
                 pymysql.escape_string(novelInfo['novelUrl']),  \
                 pymysql.escape_string(novelInfo['novelAuthor']),   \
                 pymysql.escape_string(novelInfo['novelImage']),    \
                 pymysql.escape_string(novelInfo['novelBrief']))
            logger.info("执行SQL语句:")
            logger.info(sql)
            db.executeSql(sql)
            db.close()
            return createResultString("0000", "加入书架成功.")

# 获取推荐小说
@route_novel.route("/recormmend", methods=["POST", "GET"])
def novel_recormmend():
    logger.info("从笔趣阁获取推荐数据...")
    result = {}

    spider = BIQUGE()
    logger.info("准备爬虫程序，开始爬取数据...")
    result = spider.getRecormmend()
    logger.info("获取推荐数据完成...")
    return result

# 获取小说目录
@route_novel.route("/catalog", methods=["POST"])
def novel_catalog():
    result = {}
    logger.info("从笔趣阁获取章节目录")
    logger.info("请求数据:" + request.data.decode('utf-8'))

    request_data = json.loads(request.data.decode("utf-8"))

    novel_url = request_data['novel_url']
    if None == novel_url or len(novel_url) == 0:
        logger.info("没有获取到小说的链接地址")
        result['code'] = '1001'
        result['msg'] = '没有获取到小说的链接地址'
        return json.dumps(result, ensure_ascii=False, indent=4)
    
    spider = BIQUGE()
    logger.info("准备爬虫程序，开始爬取数据...")
    spider_result = spider.getNovelBrief(novel_url)
    return spider_result 

# 根据小说url获取小说章节内容
@route_novel.route("/content", methods=["POST"])
def novel_content():
    result = {}
    logger.info("开始获取小说章节内容...")
    logger.info("请求数据:" + request.data.decode("utf-8"))

    request_data = json.loads(request.data.decode('utf-8'))

    novel_content_url = request_data['url']

    if None == novel_content_url or len(novel_content_url) == 0:
        logger.info("请求接口中没有获取到小说章节内容的URL")
        result['code'] = "1001"
        result['msg'] = "请求接口中没有获取到小说章节内容的URL"

    spider = BIQUGE()
    logger.info("准备爬虫程序，开始爬取数据...")
    spider_result = spider.getNovelContent(novel_content_url)
    return spider_result

# 保存、获取小说当前阅读进度(目前只保留阅读章节)
@route_novel.route("/currentChapter", methods=["POST"])
def novel_current_chapter():
    '''
    当前小说阅读章节模块
    包括查询、更新、插入的功能
    method:
        UPDATE --更新，如果没有数据就插入
        SELECT --查询
    '''
    db.connect()
    logger.info("书架模块...")
    logger.info("请求数据:" + request.data.decode("utf-8"))

    request_data = json.loads(request.data.decode('utf-8'))

    # 检查请求的必要数据
    check_result = checkRequestData(request_data, ['openid', 'method', 'chapterInfo'])
    if "TRUE" != check_result:
        db.close()
        return check_result

    method = request_data['method']
    openid = request_data['openid']
    chapterInfo = request_data['chapterInfo']
    logger.info("请求方法:" + method)
    logger.info("OPENID:" + openid)
    logger.info("小说信息:" + str(chapterInfo))

    if "SELECT" == str.upper(method):
        # 查询用户当前小说的阅读章节
        check_result = checkRequestData(chapterInfo, ['novelInfo'])
        if "TRUE" != check_result:
            db.close()
            return check_result

        novelInfo = chapterInfo['novelInfo']
        sql = "select count(*) from novel_current_chapter where openid = '%s' and novel_url = '%s'" % ( \
            openid, novelInfo['novelUrl'] \
        )
        logger.info(sql)
        db_result = db.executeSql(sql)
        logger.info("查询当前小说阅读章节结果:" + str(db_result))
        if 1 != db_result[0][0]:
            logger.info("该用户[%s]没有该小说的阅读记录" % (openid))
            db.close()
            return createResultString("1001", "该用户[%s]没有该小说的阅读记录" % (openid))
        else:
            sql = "select chapter_id from novel_current_chapter where openid = '%s' and novel_url = '%s'" % ( \
                openid, novelInfo['novelUrl'] \
            )
            logger.info(sql)
            db_result = db.executeSql(sql)
            logger.info("查询阅读章节ID结果:" + str(db_result))
            chapterId = db_result[0][0]
            result = {}
            result['code'] = "0000"
            result["message"] = "查询成功"
            result["chapterId"] = chapterId
            db.close()

            return json.dumps(result, indent=4, ensure_ascii=False)
    elif "UPDATE" == str.upper(method):
        # 查询用户当前小说的阅读章节
        check_result = checkRequestData(chapterInfo, ['novelInfo'])
        if "TRUE" != check_result:
            db.close()
            return check_result

        novelInfo = chapterInfo['novelInfo']
        sql = "select count(*) from novel_current_chapter where openid = '%s' and novel_url = '%s'" % ( \
            openid, novelInfo['novelUrl'] \
        )
        logger.info(sql)
        db_result = db.executeSql(sql)
        logger.info("查询当前小说阅读章节结果:" + str(db_result))
        if 1 != db_result[0][0]:
            # 插入当前阅读进度
            logger.info("插入当前阅读进度...")
            sql = "insert into novel_current_chapter(openid, novel_name, novel_url, novel_author, chapter_id, chapter_title, chapter_url, novel_image) values \
                ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (       \
                    pymysql.escape_string(openid),                                         \
                    pymysql.escape_string(novelInfo['novelName']),                       \
                    pymysql.escape_string(novelInfo['novelUrl']),                        \
                    pymysql.escape_string(novelInfo['novelAuthor']),                     \
                    str(chapterInfo['id']),                       \
                    pymysql.escape_string(chapterInfo['title']),                    \
                    pymysql.escape_string(chapterInfo['url']),                      \
                    pymysql.escape_string(novelInfo['novelImage'])                       \
                )
            logger.info(sql)
            db_result = db.executeSql(sql)
            logger.info("插入当前阅读进度结果:" + str(db_result))
            db.close()

            return createResultString("0000", "插入当前阅读进度成功...")
        else:
            # 更新阅读进度
            logger.info("更新当前阅读进度...")
            sql = "update novel_current_chapter set chapter_id = '%s', chapter_title = '%s', chapter_url = '%s' \
                where openid = '%s' and novel_url = '%s'" % (   \
                    str(chapterInfo['id']),                   \
                    pymysql.escape_string(chapterInfo['title']),                \
                    pymysql.escape_string(chapterInfo['url']),                  \
                    pymysql.escape_string(openid),                              \
                    pymysql.escape_string(novelInfo['novelUrl'])                \
                )
            logger.info(sql)
            db_result = db.executeSql(sql)
            logger.info("更新当前阅读进度结果:" + str(db_result))
            db.close()

            return createResultString("0000", "更新当前阅读进度成功...")
    else:
        return createResultString("9999", "错误的METHOD请求[%s]" % (method))
    
    


