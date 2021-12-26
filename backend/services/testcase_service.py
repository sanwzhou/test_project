# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 20:44
# @File  :testcase_service.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试用例服务

from flask import request
from flask_restful import Resource

from backend.models.testcase_model import TestCase
from backend.server import db


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

        return {'msg': 'success', 'code': '000000', 'testcase': [case.as_dict() for case in cases]}

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
    def put():
        """修改测试用例"""
        case_id = request.json.get('id')

        if case_id and TestCase.query.get(case_id):
            name = request.json.get('name')
            steps = request.json.get('steps')
            description = request.json.get('description')

            try:
                case = TestCase.query.filter_by(id=case_id).first()
                case.name = name
                case.steps = steps
                case.description = description
                db.session.add(case)
                db.session.commit()
            except Exception as e:
                print('修改失败')
                print(e)
                db.session.rollback()
                return {'msg': '用例修改失败', 'code': '100001'}
            return {'msg': 'success', 'code': '000000'}
        else:
            return {'msg': '未找到该用例id', 'code': '100003'}

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
