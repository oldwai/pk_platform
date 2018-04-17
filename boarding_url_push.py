# encoding: utf-8
"""
@version: python3.5
@author: frank
@contact: frankandrew@163.com
@file: boarding_url_push.py
@time: 2018/4/13 10:58
"""
import json

import requests

url = "http://192.168.1.122:808/air/order/buyer/boardingPass"

payload = {'downloadLink': 'www.baidu.com',
           'boardingPassUrl': 'https://mailing-files-dropzone.s3-eu-west-1.amazonaws.com/'
                              '5049/Manila-Cebu_337246730_bed745fcd54834654fa7bf19a740adda.pdf?v=1513181037',
           'orderNum': '1015119876'}

payload2 = {'downloadLink': 'www.baidu.com', 'boardingPassUrl': None, 'orderNum': '1015119876'}

headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)


print(response.text)

