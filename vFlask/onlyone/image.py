# -*- coding:gbk -*-
"""
@date   : 2019/9/9
@file   : image
@author : Vincent
@note   :
"""

import sys
import os

from vFlask.onlyone import logger
from vFlask.onlyone import onlyone_app
from flask import Response

@onlyone_app.route("/image/<imagename>")
def getImage(imagename):
    path = os.path.join(sys.path[0], 'static')
    logger.info(path)
    logger.info(imagename)

    imageFile = os.path.join(path, imagename)
    resp = Response(imageFile, mimetype="image/jpeg")
    return resp