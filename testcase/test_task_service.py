# -*-coding:utf-8 -*-
# @Time  : 2021/9/25 0025 10:16
# @File  :test_task_server.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe:测试 测试任务服务

import requests

from backend.server import db, Task


def test_db():
    # db.drop_all()
    # db.create_all()

    task1 = Task(id='1', name='task1', description='1task', testcases='[1,2,3]')
    task2 = Task(id='2', name='task2', description='2task', testcases='[1,2,3,4]')
    db.session.add_all([task1, task2])
    db.session.commit()


def test_query_task():
    res = requests.get('http://127.0.0.1:5000/task').json()
    print(res)
    assert res['code'] == '000000'


def test_query_task_by_id():
    par = {'task_id': 1}
    res = requests.get('http://127.0.0.1:5000/task', params=par).json()
    print(res)
    assert res['code'] == '000000'


def test_query_task_by_name():
    par = {'task_name': 2}
    res = requests.get('http://127.0.0.1:5000/task', params=par).json()
    print(res)
    assert res['code'] == '000000'


def test_add_task():
    data = {'name': 3, 'description': '3task', 'testcases': '[27,28,29]'}
    res = requests.post('http://127.0.0.1:5000/task', json=data).json()
    print(res)
    assert res['code'] == '000000'


def test_del_task():
    data = {'name': 4, 'description': '4task', 'testcases': '[1,2,3,4]'}
    requests.post('http://127.0.0.1:5000/task', json=data).json()

    res = requests.delete('http://127.0.0.1:5000/task', json={'task_id': 4}).json()
    print(res)
    assert res['code'] == '000000'

    res = requests.get('http://127.0.0.1:5000/task').json()
    print(res)
