# -*-coding:utf-8 -*-
# @Time  : 2021/9/23 0023 22:40
# @File  :test_testcase_server.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: server

from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from backend.settings import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
api = Api(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    passwd = db.Column(db.String(16))

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class TestCase(db.Model):
    """测试用例表"""
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    steps = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class Task(db.Model):
    """测试任务表"""
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    testcases = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024), nullable=True)


class TestCaseService(Resource):
    """
    测试用例服务
    状态码：
        {'msg': 'success', 'code': '000000'}
        {'msg': '添加用例失败', 'code': '100001'}
        {'msg': '删除用例失败', 'code': '100002'}
        {'msg': '未找到该用例id', 'code': '100003'}
    """

    @staticmethod
    def get():
        """查询用例"""
        case_id = request.args.get('case_id', None)
        name = request.args.get('name', None)

        if case_id:
            cases = TestCase.query.filter_by(id=case_id)
        elif name:
            cases = TestCase.query.filter_by(name=name)
        else:
            cases = TestCase.query.all()

        case_list = [{'id': case.id, 'name': case.name, 'steps': case.steps, 'description': case.description} for case
                     in cases]
        return {'msg': 'success', 'code': '000000', 'testcase': case_list}

    @staticmethod
    def post():
        """新增测试用例"""
        name = request.json.get('name')
        steps = request.json.get('steps')
        description = request.json.get('description')

        try:
            case = TestCase(name=name, steps=steps, description=description)
            db.session.add(case)
            db.session.commit()
        except Exception as e:
            print('添加失败')
            print(e)
            db.session.rollback()
            return {'msg': '用例添加失败', 'code': '100001'}
        return {'msg': 'success', 'code': '000000'}

    @staticmethod
    def delete():
        """删除指定测试用例"""
        case_id = request.json.get('case_id')

        case = TestCase.query.get(case_id)
        if case:
            try:
                TestCase.query.filter_by(id=case_id).delete()
                db.session.commit()
            except Exception as e:
                print('删除失败')
                print(e)
                db.session.rollback()
                return {'msg': '用例删除失败', 'code': '100002'}
        else:
            print(f'未找到该用例id:{case_id}')
            return {'msg': '未找到该用例id', 'code': '100003'}
        return {'msg': 'success', 'code': '000000'}


class TaskServer(Resource):
    """
    测试任务服务
        {'msg': 'success', 'code': '000000'}
        {'msg': '添加任务失败', 'code': '100001'}
        {'msg': '删除任务失败', 'code': '100002'}
        {'msg': '未找到该任务id', 'code': '100003'}
    """

    @staticmethod
    def get():
        task_id = request.args.get('task_id')
        task_name = request.args.get('task_name')

        if task_id:
            tasks = Task.query.filter_by(id='task_id')
        elif task_name:
            tasks = Task.query.filter_by(name='task_name')
        else:
            tasks = Task.query.all()

        tasks = [{'id': task.id, 'name': task.name, 'description': task.description} for task in tasks]
        return {'msg': 'success', 'code': '000000', 'tasks': tasks}

    @staticmethod
    def post():
        name = request.json.get('name')
        description = request.json.get('description')
        testcases = request.json.get('testcases')
        print(1, name, description, testcases)

        try:
            task = Task(name=name, description=description, testcases=testcases)
            db.session.add(task)
            db.session.commit()
        except Exception as e:
            print('添加任务失败')
            print(e)
            db.session.rollback()
            return {'msg': '添加任务失败', 'code': '100001'}
        return {'msg': 'success', 'code': '000000'}

    @staticmethod
    def delete():
        task_id = request.json.get('task_id')
        task = Task.query.get(task_id)
        if task:
            try:
                Task.query.filter_by(id=task_id).delete()
                db.session.commit()
            except Exception as e:
                print('删除任务失败')
                print(e)
                db.session.rollback()
                return {'msg': '删除任务失败', 'code': '100002'}
        else:
            return {'msg': '未找到该任务id', 'code': '100003'}
        return {'msg': 'success', 'code': '000000'}


api.add_resource(TestCaseService, '/testcase')
api.add_resource(TaskServer, '/task')

if __name__ == '__main__':
    app.run(debug=True)
