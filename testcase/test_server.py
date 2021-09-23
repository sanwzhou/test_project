# -*-coding:utf-8 -*-
# @Time  : 2021/9/23 0023 22:40
# @File  :test_server.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试服务
import requests

from backend.server import db, User, TestCase, TestCaseService


def test_db():
    db.drop_all()
    db.create_all()

    user1 = User(name='zs', passwd='123')
    db.session.add(user1)
    db.session.commit()

    testcase1 = TestCase(name='1', description='d1', steps='1,2,3')
    testcase2 = TestCase(name='2', description='d2', steps='1,2,3,4')
    db.session.add_all([testcase1, testcase2])
    db.session.commit()
    print(TestCase.query.all())


def test_query_testcase():
    """测试查询所有用例"""
    res = requests.get('http://127.0.0.1:5000/testcase')
    print(res.text)
    assert res.json()['code'] == '000000'


def test_query_testcase_by_id():
    """测试查询所有用例"""
    # todo:参数查询不可用
    par = {'case_id': 1}
    res = requests.get('http://127.0.0.1:5000/testcase', params=par)
    print(res.text)
    assert res.json()['code'] == '000000'


def test_add_testcase():
    """测试添加用例"""
    # todo:修改传参
    case = TestCaseService()
    res = case.post(name='3', steps='1,2,3,4,5')
    print(res)
    assert res['code'] == '000000'
    print(case.get())


def test_del_testcase():
    """测试删除用例"""
    # todo:修改传参
    case = TestCaseService()
    res = case.post(name='4', steps='1,2,3,4,5,6')
    print(res)
    print(case.get())
