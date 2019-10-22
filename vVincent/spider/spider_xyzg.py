# -*- coding:gbk -*-
"""
@date   : 2019/7/24
@file   : spider_xyzg
@author : Vincent
@note   :
"""
import requests

url = "https://www.creditchina.gov.cn/openAPI/getPubPenalty?entname=%E6%98%9F%E6%9C%88%E7%BD%91%E5%90%A7&user=test"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
result = requests.get(url, headers=headers)
print("status:" + str(result.status_code))
print("msg:" + result.content.decode('gbk'))
