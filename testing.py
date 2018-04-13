# encoding: utf-8
"""
@version: python3.5
@author: frank
@contact: frankandrew@163.com
@file: testing.py
@time: 2018/4/13 2:52
"""

# encoding: utf-8
"""
@version: python3.5
@author: frank
@contact: frankandrew@163.com
@file: test_platform.py
@time: 2018/4/12 16:19
"""


# -*- coding:utf-8 -*-
'''
@author:oldwai
'''
# email: frankandrew@163.com


import glob
import json
import random
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3


class Platform:
    def __init__(self, account, passwd):
        self.s = requests.Session()
        self.host = 'http://www.pkfare.com/platform-gateway'
        self.account = account
        self.passwd = passwd
        # requests库请求HTTPS时,因为忽略证书验证,会有警告，这里禁止警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        urllib3.disable_warnings()

    def get_url(self, endpoint):
        """
        接口地址拼接
        :param endpoint:接口path
        :return:
        """
        url = ''.join(self.host, endpoint)
        return url

    def post_response(self, url, **DataAll):
        """
        封装post请求的方法
        DataAll为一个字典，如json=data，files=files，传入的形式为{"json":data,"files":files}
        目前只用到部分参数，如headers和cookie也可以添加传入params
        :param url: 接口的地址
        :param DataAll: 传入的数据封装
        :return: 返回值为json格式，
        """
        params = DataAll.get('params')
        data = DataAll.get('data')
        json_data = DataAll.get('json')
        files = DataAll.get('files')
        try:
            resp = self.s.post(url, params=params, data=data,
                               json=json_data, files=files, verify=False)
            resp.encoding = 'utf-8'
            resp = resp.json()
            return resp
        except Exception as e:
            print("Post请求错误：%s" % e)

    def post_response2(self, url, **DataAll):
        """
        封装post请求的方法
        DataAll为一个字典，如json=data，files=files，传入的形式为{"json":data,"files":files}
        目前只用到部分参数，如headers和cookie也可以添加传入params
        :param url: 接口的地址
        :param DataAll: 传入的数据封装
        :return: 返回值为json格式，
        """
        params = DataAll.get('params')
        data = DataAll.get('data')
        json_data = DataAll.get('json')
        files = DataAll.get('files')
        try:
            resp = self.s.post(url, params=params, data=data, json=json_data, files=files)
            print(resp.status_code)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                resp = resp.json()
                return resp
            else:
                print(resp)
        except Exception as e:
            print("post_response2：%s" % e)

    def login_post(self, url, **DataAll):
        """
        封装post请求的方法
        DataAll为一个字典，如json=data，files=files，传入的形式为{"json":data,"files":files}
        目前只用到部分参数，如headers和cookie也可以添加传入params
        :param url: 接口的地址
        :param DataAll: 传入的数据封装
        :return: 返回值为json格式，
        """
        params = DataAll.get('params')
        data = DataAll.get('data')
        json = DataAll.get('json')
        files = DataAll.get('files')
        try:
            resp = self.s.post(url, params=params, data=data,
                               json=json, files=files, verify=False)
            if resp.json()['code'] == 1:
                resp.encoding = 'utf-8'
                sessionid = resp.headers['Set-Cookie'].split(';')[0]
                sessionid = sessionid.split('=')[1]
                self.s.headers.update({'Cookie': 'sessionId=%s' % sessionid})
                self.s.headers.update({'Content-Type':'application/json;charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36','Accept':'application/json, text/javascript, */*; q=0.01'})
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.8','X-Requested-With':'XMLHttpRequest'})
                return sessionid
            else:
                print('登录失败了',resp.content)
        except Exception as e:
            print("login_post错误：%s" % e)

    def login(self):
        """
        登录函数，以字符串的形式返回user_id，方便其他操作调用user_id
        :return: 返回user_id
        """
        post_data = {"username": self.account,
                     "password": self.passwd,
                     }
        login_url = self.host + '/user/login'
        DataAll = {'json': post_data}
        r = self.login_post(login_url, **DataAll)
        shopping_url = 'http://buyer.pkfare.com/purchase/shopping'
        body_data3 = {'queryType': 1, 'childCount': 0, 'adultCount': 1, 'airline': None, 'tripList': [{'departureCode': 'SIN', 'departureCodeAsAirport': 0, 'arrivalCode': 'HEL', 'arrivalCodeAsAirport': 0, 'departureDate': '2018-09-28'}], 'cabinClass': '1'}
        print(self.s.headers)
        res = self.s.post(shopping_url, json=body_data3)
        print(res.request.headers)
        print(res.json())
        print(res.status_code)

        if r:
            print('登录成功！')
        else:
            print(r)
        # 登录会返回一个user_id,和一个session, seesion会作为Cookie在后面的头信息用到,下面将Cookie添加到会话中
        #
        # self.s.headers.update({'Cookie': 'sessionId=%s' % r['status']['session']})
        return None

    def shopping(self):
        body_data = {'childCount': 0,
                     'queryType': 1,
                     'airline': '',
                     'cabinClass': '1',
                     'adultCount': 1,
                     'tripList': [
                         {'departureDate': '2018-07-25',
                          'departureCode': 'HEL',
                          'arrivalDate': '',
                          'arrivalCodeAsAirport': 0,
                          'departureCodeAsAirport': 0,
                          'arrivalCode': 'SIN'
                          }]}
        shopping_url = 'http://buyer.pkfare.com/purchase/shopping'
        DataAll = {'json': body_data}
        for i in range(1, 30):
            print(self.s.headers)
            res = self.s.post_response(shopping_url, **DataAll)
            print(res.headers)
            journeys = len(res['data']['journeys'])
            print(res['data']['journeys'])
            if journeys:
                break
            else:
                print('第 %d 次' % i)
                time.sleep(0.5)

if __name__ =='__main__':
    login_acc = '12499029@qq.com'
    login_pass = 'a123456'
    test = Platform(login_acc, login_pass)
    test.login()
    # body_data = {'cabinClass': '1', 'queryType': 1, 'adultCount': 1, 'tripList': [{'departureCode': 'SIN', 'arrivalCode': 'HEL', 'arrivalCodeAsAirport': 0, 'departureCodeAsAirport': 0, 'arrivalDate': None, 'departureDate': '2018-09-28'}], 'airline': None, 'childCount': 0}
    # body_data2 = {"cabinClass": "1", "queryType": 1, "adultCount": 1, "tripList": [{"departureCode": "SIN", "arrivalCode": "HEL", "arrivalCodeAsAirport": 0, "departureCodeAsAirport": 0, "arrivalDate": None, "departureDate": "2018-09-28"}], "airline": None, "childCount": 0}
    # #
    # # # print(json.dumps(body_data))
    # # # print(type(json.dumps(body_data)))
    # shopping_url = 'http://buyer.pkfare.com/purchase/shopping'
    # DataAll = {'json': body_data2}
    # res = test.post_response2(shopping_url, **DataAll)
    # for i in range(1, 30):
    #     res = test.post_response(shopping_url, **DataAll)
    #     journeys = len(res['data']['journeys'])
    #     if journeys:
    #         break
    #     else:
    #         print('第 %d 次' % i)
    #         time.sleep(0.5)
