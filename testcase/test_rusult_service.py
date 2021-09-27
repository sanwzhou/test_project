# -*-coding:utf-8 -*-
# @Time  : 2021/9/25 0025 21:34
# @File  :test_rusult_service.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试 测试结果服务

import requests

from backend.server import db, Result


def test_db():
    # db.drop_all()
    # db.create_all()

    result1 = Result(testcase_id=1, status='success', outpot='123')
    result2 = Result(testcase_id=2, status='fail', outpot='123')
    db.session.add_all([result1,result2])
    db.session.commit()


def test_query_result():
    res = requests.get('http://127.0.0.1:5000/result').json()
    print(res)
    assert res['code'] == '000000'


def test_query_result_by_case_id():
    res = requests.get('http://127.0.0.1:5000/result',params={'testcase_id': 1}).json()
    print(res)
    assert res['code'] == '000000'


def test_addy_result():
    data = {'testcase_id': 1, 'status': 'success', 'outpot':'out1'}
    res = requests.post('http://127.0.0.1:5000/result',json=data).json()
    print(res)
    assert res['code'] == '000000'

