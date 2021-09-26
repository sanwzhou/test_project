# -*- coding: utf-8 -*-
# @Time : 2021/9/26 12:43
# @Author : swzhou
# @FileName: conftest.py
# @Email   : zhou_sanwang@163.com
# @Software: PyCharm
# @describe:

import pytest
import requests


# def pytest_collection_modifyitems(session: "Session", config: "Config", items) -> None:
#     """打印用例nodeid + 插入到testcase表"""
#
#     res = requests.get('http://127.0.0.1:5000/testcase').json()
#     case_name = []
#     for case in res['testcase']:
#         case_name.append(case['name'])
#     print('case_name:', case_name)
#
#     for item in items:
#         print({"nodeid": item.nodeid, "name": item.name})
#
#         if item.nodeid not in case_name:
#             data = {'name': item.nodeid, 'description': item.name}
#             print('data:', data)
#             res = requests.request('post', url='http://127.0.0.1:5000/testcase', json=data)
#             assert res.json()['code'] == '000000'
