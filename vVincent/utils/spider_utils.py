# -*- coding=utf-8 -*-
# file:spider_utils.py.py
# time:2019/8/25{10:49}
# author:Vincent
# note:

import requests
from bs4 import BeautifulSoup

class spider:
    def __init__(self, url, headers):
        self.base_url = url
        self.headers = headers
        self.soup = ""

    def get(self, url, headers):
        response = requests.get(url, headers=headers)
        return response

    def post(selfs, url, headers, data):
        response = requests.post(url, data=data, headers=headers)
        return response

    def readToSoup(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def save_html(self, filename, html):
        '''
        保存html到文件中
        :param filename:保存文件名
        :param html:需要保存的html内容
        :return:
        '''
        fp = open(filename, "w", encoding="utf-8")
        fp.write(html)
        fp.close()

    def save_image(self, imageName, imageUrl):
        image_content = self.get(imageUrl, self.headers)
        fp = open(imageName, "wb")
        fp.write(image_content.content)
        fp.close()

    def getSingleValue(self, nodeTag):
        '''
        从BeautifulSoup中获取单个数据节点value,获取到的是结果节点中的第一个节点value
        :param nodeTag:
        :return:
        '''
        node = self.soup.select(nodeTag)
        return node[0].string

    def getSingleHref(self, nodeTag, hrefName):
        '''
        从BeautifulSoup中获取单个数据节点value,获取到的是结果节点中的第一个节点的hrefName
        :param nodeTag:
        :param hrefName:
        :return:
        '''
        node = self.soup.select(nodeTag)
        return node[0][hrefName]

