# -*-coding:utf-8 -*-
# @Time  : 2021/9/25 0025 17:10
# @File  :test_execution_service.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试 执行服务

import requests


def test_query_execution():
    # res = requests.get('http://127.0.0.1:5000/execution').json()
    pass


def test_exec_execution():
    """测试执行任务"""
    data = {'task_id': 5}
    res = requests.post('http://127.0.0.1:5000/execution', json=data).json()
    print(res)
    assert res['code'] == '000000'
