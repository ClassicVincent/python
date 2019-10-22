# -*- coding:gbk -*-
"""
@date   : 2019/9/2
@file   : log_test
@author : Vincent
@note   : logt_test.py
"""

from vVincent.utils.log_utils import mylog
import sys

logger = mylog("test").getlog()

logger.info("hello")
print(sys.path)

