# -*- coding=gbk -*-
# file:index.py
# time:2019/9/14{10:34}
# author:Vincent

from flask import Blueprint
from application import logger

route_index = Blueprint("index_page", __name__)

@route_index.route("/")
def index():
    logger.info("hello")
    return "hello, world"