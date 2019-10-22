# -*- coding=utf-8 -*-
# file:biquge.py.py
# time:2019/10/4{21:48}
# author:Vincent

'''
笔趣阁爬虫程序
'''

import os
import sys

import requests
from bs4 import BeautifulSoup
from config import DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME
import pymysql
from libs.logUtils import mylog

import json

class BIQUGE():
    def __init__(self):
        self.base_url = "https://www.biquge.info/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

        self.logger = mylog("biquge").getlog()

        self.hot_tag = "html > body > div#wrapper > div#main > div#hotcontent > div.l > div.item"

    '''
    根据小说章节对应的URL，爬取小说章节内容
    '''
    def getNovelContent(self, url):
        result = {}
        self.logger.info("获取小说章节内容的URL:" + url)
        response = requests.get(url, headers=self.headers)
        if 200 != response.status_code:
            self.logger.info("GET小说章节内容失败!" + str(response.status_code))
            return ""
        else:
            self.save_html(response.content.decode('utf-8'))

            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
            content = soup.select("div#content")[0].text.replace("\xa0", "\n")
            content = content.replace("\n\n", "\n")
            # self.logger.info(content)
            result['data'] = content
            result['code'] = '0000'
            result['msg'] = "查询成功!"

            return json.dumps(result, ensure_ascii=False, indent=4)

    '''
    爬取笔趣阁首页，从首页内容中截取推荐小说信息
    '''
    def getRecormmend(self):
        self.logger.info("开始获取首页信息...")
        response = requests.get(self.base_url, headers=self.headers)
        self.logger.info("获取结果:" + str(response.status_code))
        if 200 != response.status_code:
            self.logger.info("获取网页信息失败,错误码:" + str(response.status_code))

            return ""
        else:
            self.save_html(response.text)
            # 解析
            soup = BeautifulSoup(response.text, "html.parser")
            # hot_contents = soup.select("html > body > div#wrapper > div#main > div#hotcontent > div.l > div.item")
            hot_content = soup.select("div#hotcontent")
            hot_contents = hot_content[0].select("div.item")
            # self.logger.info(hot_contents)
            result_list = []
            
            for content in hot_contents:
                novel = {}
                novel['author'] = content.select("dl > dt > span")[0].string
                novel['url'] = content.select("dl > dt > a")[0]['href']
                novel['title'] = content.select("dl > dt > a")[0].string
                novel['image'] = content.select("img")[0]['src']
                novel['brief'] = content.select("dl > dd")[0].string
                self.logger.info(novel)
                result_list.append(novel)
                
            result = json.dumps(result_list, ensure_ascii=False, indent=4)
            self.logger.info(result)

            return result
    
    '''
    根据小说的url信息，获取小说的整体信息
    '''
    def getNovelBrief(self, url):
        self.logger.info("get novel brief start...")
        self.logger.info("url" + url)

        response = requests.get(url, headers=self.headers)
        if 200 != response.status_code:
            self.logger.info("获取网页信息失败:" + str(response.status_code))
            return ''
        else:
            self.logger.info("获取网页信息成功...")
            self.save_html(response.content.decode("UTF-8"))

            novel = {}
            self.logger.info("截取明细信息...")
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

            # 获取需要的作者、类别、最后更新时间信息
            main_info = soup.select("div#info")
            info_list = main_info[0].select("p")
            novel_info = {}
            for info in info_list:
                if info.string is None:
                    break
                else:
                    string = info.string.replace("\xa0", '')

                    index = string.index(':')
                    name = string[:index]
                    value = string[index + 1:]
                    self.logger.info(name)
                    if "作" in name:
                        novel_info['author'] = value
                    elif '最' in  name and '后' in name and '更' in name and '新' in name:
                        novel_info['latest'] = value
                    elif '类' in name:
                        novel_info['type'] = value

                novel['novel_info'] = novel_info

            # 获取小说章节目录
            div = soup.select("div#list")
            lists = div[0].select("a")
            id = 0
            contents = []
            for list in lists:
                content = {}
                id = id + 1
                # self.logger.info(url + list['href'])
                content['id'] = id
                content['title'] = list['title']
                content['url'] = url +list['href']
                contents.append(content)                
            
            novel['catalog'] = contents
            self.logger.info("目录数:" + str(len(novel['catalog'])))
            result = json.dumps(novel, ensure_ascii=False, indent=4)
            # self.logger.info(result)
            return result
    

    def save_html(self, content):
        current_dir = sys.path[0]

        self.logger.info("当前目录:" + current_dir)
        
        file_dir = os.path.join(current_dir, "html")
        file_name = os.path.join(file_dir, "biquge.html")
        self.logger.info("保存文件:" + file_name)

        fp = open(file_name, "w", encoding="utf-8")
        fp.write(content)
        fp.close()

if __name__ == "__main__":
    spider = BIQUGE()
    result = spider.getRecormmend()

    json_result = json.loads(result)
    
    spider.logger.info("*" * 80)
    result = spider.getNovelBrief(json_result[0]['url'])
    spider.logger.info(result)

    json_result = json.loads(result)
    content = json_result['catalog'][1]
    spider.logger.info(content)

    result = spider.getNovelContent(content['url'])
    spider.logger.info(result)