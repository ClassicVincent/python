# -*- coding=utf-8 -*-
# file:stringUtils.py
# time:2019/9/14{17:32}
# author:Vincent

import time
import base64
import hmac

def generateToken(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

def checkToken(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return ['2001', 'TOKEN长度不足2']
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return ['2002', 'TOKEN已过期']
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return ['2003', 'TOKEN��֤ʧ��']
    # token certification success
    return ['0000', 'TOKEN验证成功']
