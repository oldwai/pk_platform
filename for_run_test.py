# encoding: utf-8
"""
@version: python3.5
@author: frank
@contact: frankandrew@163.com
@file: test_platform.py
@time: 2018/4/12 16:19
"""


import glob
import json
import random
import time
import datetime

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3


class Platform:
    def __init__(self, account, password, specified_gds=None):
        if specified_gds:
            self.gds = specified_gds
        else:
            self.gds = '1A'
        self.s = requests.Session()
        self.host = 'http://www.pkfare.com/platform-gateway'
        self.account = account
        self.password = password

        # requests库请求HTTPS时,因为忽略证书验证,会有警告，这里禁止警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        urllib3.disable_warnings()  
        
    @staticmethod  
    def random_generation_date():
        a1 = (1976, 1, 1, 0, 0, 0, 0, 0, 0)
        # 设置开始日期时间元组（1976-01-01 00：00：00）
        a2 = (2018, 4, 1, 23, 59, 59, 0, 0, 0)
        # #设置结束日期时间元组（1990-12-31 23：59：59）
        # 生成开始时间戳
        start = time.mktime(a1)
        # 生成结束时间戳
        end = time.mktime(a2)

        # 随机生成10个日期字符串
        for i in range(10):
            # 在开始和结束时间戳中随机取出一个
            t = random.randint(start, end)
            # 将时间戳生成时间元组
            date_touple = time.localtime(t)
            # 将时间元组转成格式化字符串（1976-05-21）
            birthday_date = time.strftime("%Y-%m-%d", date_touple)
        return birthday_date

    @staticmethod
    def random_generation_name():
        import string
        random_name = 'pkfare' + ''.join(random.choice(string.ascii_letters) for _ in range(4))
        # print('random_name...........',random_name)
        # random_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
        return random_name

    def get_url(self, endpoint):
        """
        接口地址拼接
        :param endpoint:接口path
        :return:
        """
        url = ''.join(self.host, endpoint)
        return url

    def post_response_json(self, url, **DataAll):
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
            resp = self.s.post(url, params=params, data=data, json=json_data, files=files, verify=False)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                resp = resp.json()
                return resp
            else:
                print(resp)
        except Exception as e:
            print("Post请求错误：%s" % e)

    def login_post_method(self, url, **DataAll):
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
            if resp.json()['code'] == 1:
                resp.encoding = 'utf-8'
                sessionid = resp.headers['Set-Cookie'].split(';')[0]
                sessionid = sessionid.split('=')[1]
                # cookie_rel = {'Cookie': 'sessionId=%s;currency=CNY' % sessionid,}
                self.s.headers.update({'Cookie': 'sessionId=%s;currency=CNY' % sessionid})
                # self.s.cookies.update('currency', 'CNY')
                # print(self.s.cookies.get_dict())
                # self.s.cookies.set('currency', 'CNY')
                self.s.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
                return sessionid
            else:
                print('登录失败了', resp.json())
        except Exception as e:
            print("login_post_method错误：%s" % e)

    def login(self):
        """
        登录函数，以字符串的形式返回user_id，方便其他操作调用user_id
        :return: 返回user_id
        """
        post_data = {"username": self.account,
                     "password": self.password,
                     }
        login_url = self.host + '/user/login'
        DataAll = {'json': post_data}
        r = self.login_post_method(login_url, **DataAll)
        if r:
            print('登录成功！')
        else:
            print(r)
        return None

    def shopping(self):
        print('正在shopping指定的{0}........'.format(self.gds))
        delay_day = random.randint(30,60)
        NOWDATE = (datetime.datetime.now() + datetime.timedelta(days=delay_day)).strftime('%Y-%m-%d')
        body_data3 = {'queryType': 1,
                      'childCount': 0,
                      'adultCount': 1,
                      'airline': None,
                      'tripList': [{'departureCode': 'SIN',
                                    'departureCodeAsAirport': 0,
                                    'arrivalCode': 'HEL',
                                    'arrivalCodeAsAirport': 0,
                                    'departureDate': NOWDATE}],
                      'cabinClass': '1'}
        shopping_url = 'http://buyer.pkfare.com/purchase/shopping'
        DataAll = {'json': body_data3}
        flag = True
        for i in range(1, 30):
            # print(self.s.headers)
            res = self.post_response_json(shopping_url, **DataAll)
            # 传入gbp的货币单位
            # self.s.headers.update({'Cookie': 'sessionId=%s' % sessionid})
            # print(res.headers)
            journeys = len(res['data']['journeys'])
            if journeys:
                print('已查询到结果，正在验价和下单，请耐心等待.........')
                with open('./shopping_journeys.txt', 'wb') as f:
                    f.write(json.dumps(res).encode())
                flag = False
                break
            else:
                print('第 %d 次' % i)
                time.sleep(0.5)
        return res

    def res_pricing_para(self):
        '''
        将shopping返回的结果进行组合作为pricing的入参，暂未做参数化
        :return:
        '''
        res_body = self.shopping()
        solutions = res_body['data']['solutions']
        segments_id_list = []
        bookingCodes = []
        # 获取gds
        for journeyId in res_body['data']['journeys']:
            # 在每个行程下查询指定GDS的 journeyId，默认获取匹配到的第一个值
            # 因为是字典类型，所以是随机获取到的journeyId
            if res_body['data']['journeys'][journeyId]['gds'] == self.gds:
                journeys_journeyId = journeyId
                gds = res_body['data']['journeys'][journeyId].get('gds')
                # 存下subSegments list，在通过其他方法获取到segmentId
                subSegments = res_body['data']['journeys'][journeyId]['subSegments']
                break
        # 获取bookingCodes
        for i in iter(subSegments):
            bookingCode = i.get('bookingCode')
            segmentId = i.get('segmentId')
            segments_id_list.append(segmentId)
            bookingCodes.append(bookingCode)
        # 获取了行程信息还没有封装好，有时间记得哈
        # 获取segments_info_list里的行程信息传递给pricing
        seg_tuple = ('airline', 'arrival', 'arrivalDate',
                     'arrivalTime', 'departure', 'departureDate',
                     'departureTime', 'flightNum')
        segments_order = {}.fromkeys(seg_tuple, None)
        segments_list = []
        for i in iter(segments_id_list):
            segments_dict = {}
            segments_info = res_body['data']['segments'][i]
            segments_dict['airline'] = segments_info.get('airlineCode')
            segments_dict['arrival'] = segments_info.get('arrivalCode')
            segments_dict['arrivalDate'] = segments_info.get('arrivalDate')
            segments_dict['arrivalTime'] = segments_info.get('arrivalTime')
            segments_dict['departure'] = segments_info.get('departureCode')
            segments_dict['departureDate'] = segments_info.get('departureDate')
            segments_dict['flightNum'] = segments_info.get('flightNumber')
            segments_list.append(segments_dict)

        solutions_num = len(solutions)
        # 获取查询行程的类型queryType
        journey_type_dict = {'OW': "onewaySubJourney", 'RT': "roundSubJourney", 'MT': "multiSubJourney"}
        for journey_type in journey_type_dict:
            # 行程类型分为三种，判断属于哪一个行程,如果存在journeyId，则是正确的行程类型
            is_exist_journeyId = solutions[1][journey_type_dict.get(journey_type)]
            if is_exist_journeyId:
                queryType = journey_type
                break

        # 获取solutionKey
        for i in range(solutions_num):
            # 通过上面的for循环判断行程类型后
            # 如果ID和指定GDS查询到的ID一样，如果匹配则返回solutionKey
            if journeys_journeyId == solutions[i][journey_type_dict.get(journey_type)].get('journeyId'):
                solutionKey = solutions[i].get('solutionKey')
                break

        pricing_para = {'adultNum': 1,
                        'childNum': 0,
                        'gds': gds,
                        'queryType': queryType,
                        'bookingCodes': bookingCodes,
                        'solutionKey': solutionKey,
                        'flights': [{"segments": segments_list}]}
        if gds:
            return pricing_para
        else:
            return None

    def pricing(self):
        pricing_url = 'http://buyer.pkfare.com/pf-direct/platform-gateway/purchase/pricing'
        pricing_data = self.res_pricing_para()
        if pricing_data:
            DataAll = {'json': pricing_data}
            res = self.post_response_json(pricing_url, **DataAll)
            return res['data']['price']
        else:
            print('未指定gds进行验价，请检查脚本是否获取到gds')

    def res_booking_para_gds(self):
        res = self.pricing()
        tagPrices_list = res['haveCabin']['tagPrices']
        for i in tagPrices_list:
            solutionKey = i.get('solutionKey')
            # print(solutionKey)
            break
        return solutionKey

    def res_booking_para_ndc(self):
        res = self.pricing()
        tagPrices_list = res['ndc']['tagPrices']
        for i in tagPrices_list:
            solutionKey = i.get('solutionKey')
            # print(solutionKey)
            break
        return solutionKey

    def booking(self):
        booking_solutionKey = self.res_booking_para_gds()
        booking_url = 'http://buyer.pkfare.com/pf-direct/platform-gateway/order/booking'
        name = Platform.random_generation_name()
        birthday = Platform.random_generation_date()
        booking_data = {'passengers':
                            [{'sex': 'M',
                              'cardExpiredDate': '2024-03-17',
                              'cardNum': 'E07700466',
                              'cardType': 'PASSPORT',
                              'psgType': 'ADT',
                              'lastName': name,
                              'nationality': 'CN',
                              'firstName': name,
                              'birthday': birthday}],
                        'seat': {'seatKey': []},
                        'solutionKey': booking_solutionKey,
                        'baggage': {'baggageKey': []},
                        'gds': 'AMADEUS',
                        'contact':
                            {'contactTelPhone': '',
                             'contactName': 'frank',
                             'contactTelPhoneCountry': '',
                             'contactTelPhoneHead': '',
                             'contactEmail': 'frank@qq.com'},
                        'couponKey': ''}
        DataAll = {'json': booking_data}
        res = self.post_response_json(booking_url, **DataAll)
        print('已完成下单，订单号为:',res['data']['orderNum'])
        return res

    def booking_ndc(self):
        booking_solutionKey = self.res_booking_para_ndc()
        booking_url = 'http://buyer.pkfare.com/pf-direct/platform-gateway/order/booking'
        name = Platform.random_generation_name()
        birthday = Platform.random_generation_date()
        booking_data = {'passengers':
                            [{'sex': 'M',
                              'cardExpiredDate': '2024-03-17',
                              'cardNum': 'E07700466',
                              'cardType': 'PASSPORT',
                              'psgType': 'ADT',
                              'lastName': name,
                              'nationality': 'CN',
                              'firstName': name,
                              'birthday': birthday}],
                        'seat': {'seatKey': []},
                        'solutionKey': booking_solutionKey,
                        'baggage': {'baggageKey': []},
                        'gds': 'NDC',
                        'contact':
                            {'contactTelPhone': '',
                             'contactName': 'frank',
                             'contactTelPhoneCountry': '',
                             'contactTelPhoneHead': '',
                             'contactEmail': 'frank@qq.com'},
                        'couponKey': ''}
        DataAll = {'json': booking_data}
        res = self.post_response_json(booking_url, **DataAll)
        print('已完成下单，订单号为:', res['data']['orderNum'])
        return res

    def cancel_order(self):
        '''
        测试生成的订单用脚本取消，待完成
        :return:
        '''

if __name__ == '__main__':
    login_acc = '12499029@qq.com'
    login_pass = 'a123456'
    promt = ('''
    ------------------------------------------
    请输入正确的选项：
    1、指定 1A 查询下单请输入
    2、指定 NDC 查询下单
    请选择您要指定的GDS，不指定默认使用1A.........
    ------------------------------------------
    ''')
    print(promt)
    flag = True
    while flag:
        num = input('请输入序号：')
        if num.isdigit() and (int(num) in [1,2]):
            if num == '1':
                specified_gds = '1A'
            if num == '2':
                specified_gds = 'HK-AY-NDC'
            flag = False
        else:
            print(promt)
    #specified_gds表示指定gds查询
    test = Platform(login_acc, login_pass, specified_gds=specified_gds)
    test.login()
    # test.res_pricing_para()
    #booking_ndc暂时无法使用，返回为None时没做判断，生gds订单一样有问题
    if num == '1':
        test.booking()
    if num == '2':
        test.booking_ndc()

    input("\n\nPress the enter key to exit.")