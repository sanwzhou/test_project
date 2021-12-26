# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 21:04
# @File  :result_service.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试结果服务
from flask import request
from flask_restful import Resource

from backend.models.result_model import Result
from backend.server import db


class ResultService(Resource):
    """测试结果保存"""

    @staticmethod
    def get():
        testcase_id = request.args.get('testcase_id')
        if testcase_id:
            results = Result.query.filter_by(testcase_id=testcase_id)
        else:
            results = Result.query.all()

        return {'msg': 'success', 'code': '000000', 'results': [r.as_dict() for r in results]}

    @staticmethod
    def post():
        testcase_id = request.json.get('testcase_id')
        status = request.json.get('status')
        outpot = request.json.get('outpot')
        try:
            result = Result(testcase_id=testcase_id, status=status, outpot=outpot)
            db.session.add(result)
            db.session.commit()
        except Exception as e:
            print('保存用例执行结果失败')
            print(e)
            db.session.rollback()
            return {'msg': '保存用例执行结果失败', 'code': '100001'}
        return {'msg': 'success', 'code': '000000'}
