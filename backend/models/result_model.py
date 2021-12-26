# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 21:00
# @File  :result_model.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试结果表结构

from backend.server import db


class Result(db.Model):
    """测试结果"""
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    testcase_id = db.Column(db.Integer, db.ForeignKey('testcases.id'))
    status = db.Column(db.String(120), nullable=True)
    outpot = db.Column(db.String(1024), nullable=True)

    def as_dict(self):
        return {'id': self.id, 'testcase_id': self.testcase_id, 'status': self.status, 'outpot': self.outpot}
