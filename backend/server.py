# -*-coding:utf-8 -*-
# @Time  : 2021/9/23 0023 22:40
# @File  :test_server.py
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
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    steps = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


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


api.add_resource(TestCaseService, '/testcase')


if __name__ == '__main__':
    app.run(debug=True)
