# -*- coding=utf-8 -*-
# file:spider_one.py.py
# time:2019/8/25{10:47}
# author:Vincent
# note: http://wufazhuce.com/

import os
import sys

sys.path.append(os.getenv("VPYTHON"))

from vVincent.utils.spider_utils import spider

import os

class ONE:
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.base_url = "http://wufazhuce.com/"
        self.spider = spider(self.base_url, self.headers)
        self.html = "./html/index.html"
        self.word_tag = "html > body > div > div.row.frontpage > div.col-md-8 > div.fp-one > div > div.carousel-inner > div.item.active > div.fp-one-cita-wrapper > div.fp-one-cita > a"
        self.img_tag = "html > body > div > div.row.frontpage > div.col-md-8 > div.fp-one > div > div.carousel-inner > div.item.active > a > img.fp-one-imagen"

        '''
        主要获取一下两个数据,一个是首页图片,一个是每日一句
        '''
        self.word = ""
        self.imageFile = os.getenv('VPYTHON') + "/vFlask/onlyone/static/image/one.jpg"

        self.index()

    def index(self):
        index = self.spider.get(self.base_url, self.headers)
        #self.spider.save_html(self.html, index.content.decode("utf-8"))
        self.spider.readToSoup(index.content.decode("utf-8"))
        self.word = self.spider.getSingleValue(self.word_tag)
        # print(self.word)

        imageUrl = self.spider.getSingleHref(self.img_tag, "src")
        self.spider.save_image(self.imageFile, imageUrl)

if __name__ == "__main__":
    one = ONE()
    print(one.word)
