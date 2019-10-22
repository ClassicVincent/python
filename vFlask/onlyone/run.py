#!/usr/bin/python
'''
@date	: 20190722
@file	: onlyone_run.py
@author	: onlyone
'''

import sys
import os
sys.path.append(os.getenv('VPYTHON'))

from datetime import timedelta
from vFlask.onlyone import onlyone_app

from vFlask.onlyone.login import onlyone_login
from vFlask.onlyone.login import onlyone_register
from vFlask.onlyone.index import onlyone_index
from vFlask.onlyone.image import getImage

onlyone_app.config['SECRET_KEY'] = os.urandom(24)
#自定义设置session的有效期
onlyone_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
onlyone_app.run(host="0.0.0.0", port=8102, debug=True)
