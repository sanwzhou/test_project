# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 20:46
# @File  :testcase_mode.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试用例model

from backend.server import db


class TestCase(db.Model):
    """测试用例表"""
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    steps = db.Column(db.String(1024), nullable=True)
    description = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}>'

    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'steps': self.steps, 'description': self.description}
